from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from config import TOKEN, MAX_TOKENS, TESTER_ID, SYSTEM_CONTENT
from gpt import GPT
import logging
import os

bot = TeleBot(TOKEN)
MAX_LETTERS = MAX_TOKENS
gpt = GPT()

logging.basicConfig(filename='bot.log', level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s'
                           ' - %(message)s')

users_history = {}


def create_keyboard(buttons_list):
    try:
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,
                                       one_time_keyboard=True)
        keyboard.add(*buttons_list)
        return keyboard
    except Exception as e:
        logging.error(f"Произошла ошибка в функции create_keyboard: {e}")


@bot.message_handler(commands=['start'])
def start(message):
    try:
        user_name = message.from_user.first_name
        bot.send_message(message.chat.id,
                         text=f"Приветствую, {user_name}! Введите команду"
                              f" /help для ознакомеления с функцианальностью",
                         reply_markup=create_keyboard(["/solve_task", '/help']))
    except Exception as e:
        logging.error(f"Произошла ошибка в обработчике сообщений start: {e}")


@bot.message_handler(commands=['help'])
def support(message):
    bot.send_message(message.from_user.id,
                     text="Введите команду /solve_task, а затем введите любую"
                          f" задачу на английском языке и нейросеть сгенирирует"
                          f" ответ.",
                     reply_markup=create_keyboard(["/solve_task"]))


@bot.message_handler(commands=['debug'])
def debug(message):
    try:
        user_id = message.from_user.id
        if user_id == TESTER_ID:
            if os.path.exists('bot.log'):
                with open('bot.log', 'rb') as f:
                    bot.send_document(user_id, f)
            else:
                bot.send_message(user_id, "Файл с логами не найден")
        else:
            bot.send_message(user_id, "Команда не найдена")
    except Exception as e:
        logging.error(f"Произошла ошибка в функции debug: {e}")


@bot.message_handler(commands=['solve_task'])
def solve_task(message):
    bot.send_message(message.chat.id, "Введите новый запрос для нейросети:")
    bot.register_next_step_handler(message, get_promt)


def continue_filter(message):
    button_text = 'Продолжить решение'
    return message.text == button_text


@bot.message_handler(func=continue_filter)
def get_promt(message):
    user_id = message.from_user.id

    if message.content_type != "text":
        bot.send_message(user_id,
                         "Необходимо отправить именно текстовое сообщение")
        bot.register_next_step_handler(message, get_promt)
        return

    user_request = message.text

    tokens = gpt.count_tokens(user_request)

    if tokens > MAX_TOKENS:
        msg = bot.send_message(user_id,
                               "Запрос слишком длинный, сократите запрос")
        bot.register_next_step_handler(msg, get_promt)
        return

    if user_id not in users_history or users_history[user_id] == {}:
        users_history[user_id] = {
            'system_content': SYSTEM_CONTENT,
            'user_content': user_request,
            'assistant_content': "Let's solve the task step by step: "
        }

    promt = gpt.make_promt(users_history[user_id])
    resp = gpt.send_request(promt)

    success, answer = gpt.process_resp(resp)
    if success:
        users_history[user_id]['assistant_content'] += answer
    else:
        users_history[user_id]['assistant_content'] += ("\nПроизошла ошибка: " +
                                                        answer)

    bot.send_message(user_id, text=users_history[user_id]['assistant_content'],
                     reply_markup=create_keyboard(
                         ["Продолжить решение", "Завершить решение"]))


def end_filter(message):
    button_text = 'Завершить решение'
    return message.text == button_text


@bot.message_handler(content_types=['text'], func=end_filter)
def end_task(message):
    try:
        user_id = message.from_user.id
        bot.send_message(user_id, "Текущие решение завершено")
        users_history[user_id] = {}
        solve_task(message)
    except Exception as e:
        logging.error(f"Произошла ошибка в функции end_task: {e}")


bot.polling(none_stop=True)
