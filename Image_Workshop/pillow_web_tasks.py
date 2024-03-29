
# Повтори методы обработки изображения за наставником

from PIL import Image

# Открываем изображение (open)

# Показываем изображение (show)

# Сохраняем изображение. Можно сохранить в любом формате (save)

# Дальше смотрим на параметры изображения

# Размер изображения (size)

# Размер можно сохранить в переменные (ширина, высота)


# Формат изображения (format)

# А теперь изменим наше изображение

# Изменяем размер изображения (resize)


# Поворачиваем изображение (rotate)




# Самостоятельное задание в группах 1
# Примени преобразования так, чтобы вернуть изображение task1.jpeg к нормальному виду

img = Image.open("task1.jpeg").convert("L")
img.show()





# Повтори методы обработки изображения за наставником
from PIL import Image

img = Image.open("image_1.png").convert("L")

# Обрезаем изображение
# im.crop((left, upper, right, lower))
# left, upper - координаты верхнего левого угла
# right, lower - координаты нижнего правого угла

# обрежем изображение по координатам углов (40, 30) и (60, 50)





# Рисуем на изображении
from PIL import ImageDraw

draw = ImageDraw.Draw(img)

# Рисуем линию
# ImageDraw.Draw.line(xy, fill=None, width=0, joint=None)
# xy – координаты начала и конца линии
# fill – цвет линии
# width – толщина линии
# joint – тип соединения линий. Возможные значения: “curve”, “none”, “miter”, “round”, “bevel”.





# Рисуем прямоугольник
# ImageDraw.Draw.rectangle(xy, fill=None, outline=None, width=0)
# xy – координаты верхнего левого и нижнего правого угла прямоугольника
# fill – цвет заливки
# outline – цвет границы
# width – толщина границы





# Рисуем текст

# ImageDraw.Draw.text(xy, text, fill=None, font=None, anchor=None, spacing=0, align=”left”)
# xy – координаты верхнего левого угла текста
# text – текст
# fill – цвет текста
# font – шрифт
# anchor – определяет как координаты xy будут интерпретироваться. Если anchor = None, то координаты xy будут интерпретироваться как координаты левого верхнего угла текста. Если anchor = “mm”, то координаты xy будут интерпретироваться как координаты центра текста.
# spacing – межстрочный интервал
# align – выравнивание текста. Возможные значения: “left”, “center”, “right”.







# Самостоятельное задание в группах 2
# Подпиши мем из картинки hlebushek.png и сохрани его
meme = Image.open("hlebushek.png")
meme.show()






# Повтори методы обработки изображения за наставником
from PIL import Image

# Попиксельное изменение изображения
# _________________________________________________________________

# получение цвета пикселя по координатам
# Image.getpixel((x, y))
# x, y – координаты пикселя



# изменение цвета пикселя по координатам
# Image.putpixel((x, y), color)
# x, y – координаты пикселя



# Поменяем цвета на изображении

img = Image.open("meme.png").convert("L")

w, h = img.size
img.show() # показываем изображение
