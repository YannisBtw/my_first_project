import random


def apply_emojify_filter(text):
    words = text.split()
    emojis = ["😀", "😂", "😎", "🚀", "❤️", "🌈", "💖", "💗", "🥰", "💞"]
    result = words[0]
    for word in words[1:]:
        result += " " + random.choice(emojis) + " " + word
    return result


def apply_word_reverse_filter(text):
    words = text
    result = ""
    for index in range(len(words)):
        result += words[len(words) - 1 - index]
    return result


def apply_sentence_reverse_filter(text):
    words = text.split()
    result = ""
    for index in range(len(words)):
        result += " " + words[len(words) - 1 - index]
    return result


def apply_invert_filter(text):
    inverted_text = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                inverted_text += char.lower()
            else:
                inverted_text += char.upper()
        else:
            inverted_text += char
    return inverted_text


filters = {
    1: {
        "name": "Emojify Filter",
        "description": "Этот фильтр добавляет случайные смайлики между словами",
        "function": apply_emojify_filter,
    },
    2: {
        "name": "Word Reverse Filter",
        "description": "Этот фильтр переворачивает каждое слово в тексте.",
        "function": apply_word_reverse_filter,
    },
    3: {
        "name": "Sentence Reverse Filter",
        "description": "Этот фильтр меняет местами слова в тексте.",
        "function": apply_sentence_reverse_filter,

    },
    4: {
        "name": "Invert Filter",
        "description": "Этот фильтр инвертирует регистр букв в тексте.",
        "function": apply_invert_filter,
    }
}
while True:
    print("Меню фильтров:")
    for key, filter_data in filters.items():
        print(f"{key}: {filter_data['name']}")

    print("0: Выход")

    choice = input("Выберите фильтр (или 0 для выхода): ")

    if choice == "0":
        print("До свидания!")
        break

    if choice.isdigit():
        choice = int(choice)
        if choice in filters:
            filter_data = filters[choice]
            print(filter_data["name"] + ":")
            print(filter_data["description"])
            apply_filter = input("Применить фильтр к тексту (Да/Нет)? ").lower()
            if apply_filter == "да":
                text = input("Введите текст для фильтрации: ")
                result = filter_data["function"](text)
                print(f"Результат: {result}")
            elif apply_filter == "нет":
                continue
            else:
                print("Некорректный ввод. Возврат в меню.")
        else:
            print("Некорректный выбор фильтра.")
    else:
        print("Некорректный ввод. Пожалуйста, введите номер фильтра.")
