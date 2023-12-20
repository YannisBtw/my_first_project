import telebot
from info import list_of_commands, sigma_history, sigma_becoming
from PIL import Image

token = "6623726531:AAEa3dkb83RAPEpCULiDeDrH7FtYOc58y6o"
bot = telebot.TeleBot(token=token)


def filter_hello(message):
    password = "привет"
    return password in message.text.lower()


def filter_bye(message):
    password = "пока"
    return password in message.text.lower()


def show_menu(message):
    for key, commands_data in list_of_commands.items():
        bot.send_message(message.chat.id, f"{key}: {commands_data['name']}"
                                          f" ({commands_data['description']})")


@bot.message_handler(content_types=['text'], func=filter_hello)
def say_hello(message):
    bot.send_message(message.chat.id, f"Приветствую вас, многоуважаемый "
                                      f"{message.from_user.first_name}.")


@bot.message_handler(content_types=['text'], func=filter_bye)
def say_bye(message):
    bot.send_message(message.chat.id, f"До свидания, многоуважаемый "
                                      f"{message.from_user.first_name}.")


@bot.message_handler(commands=["start"])
def say_start(message):
    bot.send_message(message.chat.id, f"Приветствую вас, многоуважаемый "
                                      f"{message.from_user.first_name}. "
                                      "Я сигма-бот, расскажу тебе о себе! "
                                      "Рекомендую ознакомиться с доступными "
                                      "командами (/help)")


@bot.message_handler(commands=["help"])
def say_help(message):
    bot.send_message(message.chat.id, "Друг, вот список того, что я умею:")
    show_menu(message)


@bot.message_handler(commands=["history"])
def say_history(message):
    bot.send_message(message.chat.id, sigma_history)


@bot.message_handler(commands=["becoming"])
def say_history(message):
    bot.send_message(message.chat.id, sigma_becoming)


@bot.message_handler(commands=["photo"])
def send_photo(message):
    photo = Image.open("sigma.jpg").convert("RGB")
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['favorite_song'])
def send_music(message):
    audio1 = open('interworld — metamorphosis [sigma edit].mp3', 'rb')
    audio2 = open('КРИПЕР СИГМА И СВИНКА СИГМА МЕМ.mp3', 'rb')
    bot.send_audio(message.chat.id, audio1)
    bot.send_audio(message.chat.id, audio2)


@bot.message_handler(commands=["favorite_video"])
def send_video(message):
    video = open('sigma.mp4', 'rb')
    bot.send_video(message.chat.id, video)


@bot.message_handler(content_types=['text'])
def repeat_message(message):
    bot.send_message(message.chat.id, f"Сигмы не говорят «{message.text}».")


bot.polling(none_stop=True)
