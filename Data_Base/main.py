import json
from info import game_data


def register_player():
    """Функция регистрации игрока.
    Возвращает словарь player = {"username": ..., "location": ...}
    с именем игрока и начальной локацией."""
    username = input("Введите ваше имя: ")
    player = {
        "username": username,
        "location": "start"
    }
    with open(f"{username}.json", "w") as file:
        json.dump(player, file)
    return player


def start_game(player, game_data):
    print("Приветствую вас в мире приключений!")
    while True:
        current_location = player["location"]
        print(game_data[current_location]["description"])
        options = game_data[current_location]["options"]
        if not options:
            print("Игра завершена.")
            break
        choice = input("Выберите вариант: ")
        if choice in options:
            player["location"] = options[choice]
            with open(f"{player['username']}.json", "w") as file:
                json.dump(player, file)
        else:
            print("Неверный выбор. Попробуйте снова.")


player = register_player()
start_game(player, game_data)
