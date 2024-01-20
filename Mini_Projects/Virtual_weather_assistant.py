user_name = input("Напиши свое имя:\n")
weather_type = input("Какая у тебя погода (солнечно, дождь, туман, пасмурно и тд):\n")
temperature = int(input("Какая сейчас температура:\n"))
time_of_day = input("Какое у тебя время суток:\n")

print("Привет,", user_name)
print("Я твой виртуальный помощник")
print("Сегодня на улице", weather_type)
print("Температура воздуха составляет", temperature, "град. по Цельсию")

is_cold = temperature < 10
is_warm = 10 <= temperature <= 25
is_hot = temperature > 25

if time_of_day == "утро" and not (weather_type == "дождь" or weather_type == "туман"):
    print("Сейчас самое время насладиться свежим воздухом - погода отличная!")
elif time_of_day == "вечер" and weather_type == "дождь":
    print("Как насчёт любимого фильма или книги?")
# И снова наш код
if is_cold or weather_type == "дождь" and not is_hot:
    print("Лучше надень что-то теплое и возьми зонт!")
if is_warm and not (weather_type == "дождь" or weather_type == "ветер"):
    print("Идеальная погода для куртки и кроссовок!")
else:
    print("Лучше остаться дома.")