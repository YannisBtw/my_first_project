import telebot
from telebot import types
import os
from dotenv import load_dotenv
from PIL import Image

from data import WELCOME_TEXT, GOOD_ENDING_TEXT, BAD_ENDING_TEXT, HELP_TEXT
from json_handler import load_json
from data import Buttons

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

user_location = {}


def make_murkup(buttons: list) -> types.ReplyKeyboardMarkup:
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=True)
    for button in buttons:
        murkup.add(button)
    return murkup


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    try:
        chat_id = message.chat.id
        location = "start"

        if chat_id in user_location:
            location = user_location[chat_id]
        user_location[message.chat.id] = location

        murkup = make_murkup([Buttons.START, Buttons.HELP])

        msg = bot.send_message(chat_id, WELCOME_TEXT, reply_markup=murkup)

        bot.register_next_step_handler(msg, handle_answer)
    except Exception as e:
        print(f"Error in start: {e}")


@bot.message_handler(commands=['help'])
def help(message: types.Message):
    try:
        bot.send_message(message.chat.id, HELP_TEXT)
    except Exception as e:
        print(f"Error in help: {e}")


def handle_answer(message: types.Message) -> None:
    try:
        if message.text == Buttons.START:
            start_game(message)
        elif message.text == Buttons.HELP:
            help(message)
        else:
            bot.send_message(message.chat.id, "Такой команды нет")
    except Exception as e:
        print(f"Error in handle_answer: {e}")


def start_game(message: types.Message) -> None:
    try:
        chat_id: int = message.chat.id
        location: str = user_location[chat_id]
        all_locations: dict = load_json("locations.json")

        if location:
            current_location = all_locations[location]
            buttons = list(current_location["scenarios"].keys())
            murkup = make_murkup(buttons)
            description = current_location["description"]
            image = current_location["image"]
            photo = Image.open(f"{image}").convert("RGB")

            bad_ending = current_location["bad_ending"]
            good_ending = current_location["good_ending"]

            if bool(int(bad_ending)):
                bot.send_message(chat_id, BAD_ENDING_TEXT)
                return
            elif bool(int(good_ending)):
                bot.send_message(chat_id, GOOD_ENDING_TEXT)
                return

            msg = bot.send_message(chat_id, description, reply_markup=murkup)
            bot.send_photo(chat_id, photo)

            bot.register_next_step_handler(msg, send_location)
        else:
            bot.send_message(chat_id, "Нет стартовой локации")
    except Exception as e:
        print(f"Error in start_game: {e}")


def send_location(message: types.Message):
    try:
        user_text = message.text
        chat_id = message.chat.id
        location: str = user_location[chat_id]
        all_locations: dict = load_json("locations.json")
        current_locations: dict = all_locations[location]
        user_choice = current_locations["scenarios"][user_text]
        description = user_choice.get("description", "Вперед, детектив...")

        if 'image' in user_choice:
            image = user_choice["image"]
            photo = Image.open(f"{image}").convert("RGB")
            bot.send_photo(chat_id, photo)
        bot.send_message(chat_id, description)
        if "new_location" in user_choice:
            user_location[chat_id] = user_choice["new_location"]
            start_game(message)
    except Exception as e:
        print(f"Error in send_location: {e}")


try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Error in bot polling: {e}")
