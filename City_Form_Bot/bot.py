from dotenv import load_dotenv
import json
import os
import telebot
from PIL import Image
from telebot import types
from telebot.types import Message
from info import (User, help_text, questions, city_info, answers,
                  answer_to_city)

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)
user_data = {}


def save_data():
    with open('user_data.json', 'w') as f:
        json.dump({k: v.__dict__ for k, v in user_data.items()}, f)


def load_data():
    global user_data
    try:
        with open('user_data.json', 'r') as f:
            user_data = {k: User(**v) for k, v in json.load(f).items()}
    except FileNotFoundError:
        user_data = {}
    except json.JSONDecodeError:
        user_data = {}


load_data()


load_data()


def filter_hello(message: Message) -> bool:
    password = "привет"
    return password in message.text.lower()


def filter_bye(message: Message) -> bool:
    password = "пока"
    return password in message.text.lower()


@bot.message_handler(content_types=['text'], func=filter_hello)
def say_hello(message: Message):
    bot.send_message(message.chat.id, f"Приветствую вас, многоуважаемый "
                                      f"{message.from_user.first_name}.")


@bot.message_handler(content_types=['text'], func=filter_bye)
def say_bye(message: Message):
    bot.send_message(message.chat.id, f"До свидания, многоуважаемый "
                                      f"{message.from_user.first_name}.")


@bot.message_handler(commands=['greet'])
def greet(message: Message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('/start')
        button_help = types.KeyboardButton('/help')
        markup.add(button_start, button_help)
        bot.send_message(message.chat.id,
                         "Добро пожаловать в тест-бота «Какой город мира"
                         " идеален для вас?» Выберите одну из команд:",
                         reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Произошла ошибка, попробуйте ещe")


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    user_id = message.chat.id
    user_data[user_id] = User()
    save_data()
    ask_question(message)


@bot.message_handler(commands=['help'])
def send_help(message: Message):
    try:
        bot.send_message(message.chat.id, help_text)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Произошла ошибка, попробуйте ещe")


def ask_question(message: Message):
    try:
        user_id = message.chat.id
        user = user_data[user_id]
        if len(user.answers) < len(questions):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for option in answers[len(user.answers)]:
                markup.add(option)
            msg = bot.send_message(message.chat.id,
                                   questions[len(user.answers)],
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, process_step)
        else:
            calculate_scores(message)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Произошла ошибка, попробуйте ещe")


def process_step(message: Message):
    try:
        user_id = message.chat.id
        user = user_data[user_id]
        user.answers.append(message.text)
        save_data()
        ask_question(message)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Произошла ошибка, попробуйте ещe")


def calculate_scores(message: Message):
    try:
        user_id = message.chat.id
        user = user_data[user_id]
        for answer in user.answers:
            city = answer_to_city.get(answer)
            if city:
                user.scores[city] += 1
        result = max(user.scores, key=user.scores.get)
        bot.send_message(message.chat.id, f"Ваш идеальный город - {result}!"
                                          f"{city_info[result]}")
        photo = Image.open(f"{result}.png").convert("RGB")
        bot.send_photo(message.chat.id, photo)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Произошла ошибка, попробуйте ещe")


load_data()

bot.polling(non_stop=True)
