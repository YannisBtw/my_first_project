from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, Message
import logging
import os

from config import (TOKEN, MAX_TOKENS, TESTER_ID, HELP_TEXT,
                    COMMAND_TO_SUBJECT, PROMPTS_TEMPLATES)
from gpt import GPT
from db import (prepare_db, insert_row, delete_user, update_row_value,
                get_data_for_user, is_value_in_table)

bot = TeleBot(TOKEN)
MAX_LETTERS = MAX_TOKENS
gpt = GPT()

user_request = {}

logging.basicConfig(filename='bot.log', level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s'
                           ' - %(message)s')


def create_keyboard(buttons_list):
    try:
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,
                                       one_time_keyboard=True)
        keyboard.add(*buttons_list)
        return keyboard
    except Exception as e:
        logging.error(f"Произошла ошибка в функции create_keyboard: {e}")


@bot.message_handler(commands=['start'])
def start(message: Message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     text=f"Приветствую, {user_name}! Введите команду"
                          f" /help для ознакомеления с функцианальностью",
                     reply_markup=create_keyboard(['/help_with_life',
                                                   '/help_with_knowledge',
                                                   '/help']))


@bot.message_handler(commands=['help'])
def support(message: Message):
    bot.send_message(message.chat.id,
                     text=HELP_TEXT,
                     reply_markup=create_keyboard(['/help_with_life',
                                                   '/help_with_knowledge']))


@bot.message_handler(commands=['debug'])
def debug(message: Message):
    try:
        user_id = message.chat.id

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


@bot.message_handler(commands=['help_with_life', "help_with_knowledge"])
def choose_subject(message: Message):
    try:
        user_id = message.from_user.id
        subject_from_user = message.text
        subject = COMMAND_TO_SUBJECT.get(subject_from_user)

        if subject is None:
            bot.send_message(message.chat.id,
                             "Некорректный запрос, повторите попытку:")

        if is_value_in_table('users', 'id', user_id):
            delete_user(user_id)

        insert_row((user_id, subject, None, None, None))
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите уровень сложности:",
                         reply_markup=create_keyboard(['beginner', 'advanced']))
        bot.register_next_step_handler(message, choose_level)
    except Exception as e:
        logging.error(f"Произошла ошибка в функции choose_subject: {e}")


def is_level_in_message(message: Message):
    text = message.text.lower()
    return 'beginner' in text or 'advanced' in text


@bot.message_handler(func=is_level_in_message)
def choose_level(message: Message):
    try:
        user_id = message.from_user.id
        user_level = message.text
        update_row_value(user_id, 'level', user_level)
        bot.send_message(message.chat.id, 'Пожалуйста, введите ваш запрос:')
        bot.register_next_step_handler(message, give_answer)
    except Exception as e:
        logging.error(f"Произошла ошибка в функции choose_subject: {e}")


def is_user_data_in_table(message: Message):
    user_id = message.from_user.id
    user_data = get_data_for_user(user_id)

    if user_data['subject'] and user_data['level']:
        return True

    else:
        bot.send_message(message.chat.id,
                         'Вы не выбрали предмет или уровень сложности,'
                         ' пожалуйста, повторите попытку:',
                         reply_markup=create_keyboard(['/help_with_life',
                                                       '/help_with_knowledge']))
        return False


@bot.message_handler(func=is_user_data_in_table)
def give_answer(message: Message):
    try:
        user_id = message.from_user.id
        user_task = message.text
        tokens = gpt.count_tokens(user_task)

        if tokens > MAX_TOKENS:
            msg = bot.send_message(message.chat.id,
                                   "Запрос слишком длинный, сократите"
                                   " запрос")
            bot.register_next_step_handler(msg, give_answer)
            return

        if not isinstance(message.content_type, str):
            bot.send_message(user_id,
                             "Необходимо отправить именно текстовое"
                             " сообщение")
            bot.register_next_step_handler(message, give_answer)
            return

        bot.send_message(message.chat.id, "Ваш запрос обрабатывается...")
        update_row_value(user_id, 'task', user_task)

        user_data = get_data_for_user(user_id)
        user_subject = user_data['subject']
        user_level = user_data['level']

        user_request[user_id] = {
            'system_content': PROMPTS_TEMPLATES[user_subject][user_level],
            'user_content': user_task,
            'assistant_content': "Let's solve the task step by step: "
        }

        promt = gpt.make_promt(user_request[user_id])
        resp = gpt.send_request(promt)
        success, answer = gpt.process_resp(resp)

        if success:
            update_row_value(user_id, 'answer', answer)
        else:
            logging.error("Произошла ошибка при создании промпта или ответа")

        bot.send_message(message.chat.id, text=answer,
                         reply_markup=create_keyboard(
                             ["/continue", '/help_with_life',
                              '/help_with_knowledge']))
    except Exception as e:
        logging.error(f"Произошла ошибка в функции choose_subject: {e}")


@bot.message_handler(commands=['continue'])
def continue_answer(message: Message):
    try:
        user_id = message.from_user.id
        user_data = get_data_for_user(user_id)
        last_answer = user_data['answer']
        user_request[user_id]['system_content'] += last_answer
        promt = gpt.make_promt(user_request[user_id])
        resp = gpt.send_request(promt)
        success, answer = gpt.process_resp(resp)

        if success:
            update_row_value(user_id, 'answer', answer)
        else:
            logging.error("Произошла ошибка при создании промпта или ответа")

        bot.send_message(message.chat.id, text=answer,
                         reply_markup=create_keyboard(
                             ["/continue", '/help_with_life',
                              '/help_with_knowledge']))
    except Exception as e:
        logging.error(f"Произошла ошибка в функции continue_answer: {e}")


prepare_db()
bot.polling(none_stop=True)
