from PIL import Image
import os
from utils import filters


def main():
    print("Добро пожаловать в консольный фоторедактор.")
    is_finished = False
    while not is_finished:
        path = input("Введите путь к файлу: ")

        while not os.path.exists(path):
            path = input("Файл не найден. Пожалуйста, введите путь еще раз: ")

        img = Image.open(path).convert("RGB")

        print("Меню фильтров:")
        for key, filter_data in filters.items():
            print(f"{key}: {filter_data['name']}")

        print("0: Выход")

        choice = int(input("Выберите фильтр (или 0 для выхода): "))

        if choice == 0:
            print("До свидания!")
            exit()

        while not choice <= 3:
            choice = int(
                input("Неккоректный ввод. Пожалуйста, повторите ввод."))

        filter_data = filters[choice]
        filter_class = filter_data["class"]
        print(filter_data["name"] + ":")
        print(filter_data["description"])
        apply_filter = input("Применить фильтр (Да/Нет)? ").lower()
        if apply_filter == "да" or apply_filter == "lf":
            img = filter_class.apply_to_image(img)
        elif apply_filter == "нет" or apply_filter == "ytn":
            continue

        save_path = input("Куда сохранить: ")

        img.save(save_path)

        answer = input("Ещё раз? (Да/Нет): ").lower()
        while answer not in ["нет", "да", "lf", "ytn"]:
            answer = input("Неккорентный ввод. Пожалуйста, повторите попытку: ")
        is_finished = answer == "нет"


if __name__ == "__main__":
    main()
