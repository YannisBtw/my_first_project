phrase_bad = "Пошло вон, упырское отродье!"
phrase_neutral = "Проходи, не задерживайся, бродяга."
phrase_king = "Ваше величество! Как мы вам рады! Добро пожаловать!"

fraction = input("Введите вашу фракцию (орк, бандит, крестьянин, король:)\n")

if fraction == "орк":
    print(phrase_bad)
elif fraction == "бандит":
    print(phrase_bad)
elif fraction == "крестьянин":
    print(phrase_neutral)
elif fraction == "король":
    print(phrase_king)