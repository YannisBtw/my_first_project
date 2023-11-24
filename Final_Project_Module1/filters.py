from PIL import Image


def get_color_change_values() -> tuple[int, int, int]:
    red_value = int(input("Введите значение изменения красного [0,255]: "))
    green_value = int(input("Введите значение изменения зеленого [0,255]:"))
    blue_value = int(input("Введите значение изменения синего [0,255]: "))
    while red_value not in range(0, 256):
        red_value = int(
            input("Значение красного не в [0,255]. Повторите попытку: "))
    while green_value not in range(0, 256):
        green_value = int(
            input("Значение зеленого не в [0,255]. Повторите попытку: "))
    while blue_value not in range(0, 256):
        blue_value = int(
            input("Значение синего не в [0,255]. Повторите попытку: "))
    return red_value, green_value, blue_value


class Filter:
    """
    Базовый класс для создания фильтров
    """

    def apply_to_pixel(self, red_pixel, green_pixel, blue_pixel: int) \
            -> tuple[int, int, int]:
        """
        Применяет фильтр к одному пикселю
        :param blue_pixel: значение синиго канала
        :param green_pixel: начение зеленого канала
        :param red_pixel: начение красного канала
        :return: новый цвет пикселя
        """
        raise NotImplementedError()

    def apply_to_image(self, img: Image.Image) -> Image.Image:
        """
        Проходится циклом по всем пикселям, меняя старые на новые
        :param img: загруженное изображение
        :return: измененное изображение
        """
        for i in range(img.width):
            for j in range(img.height):
                red_pixel, green_pixel, blue_pixel = img.getpixel((i, j))
                new_red_pixel, new_green_pixel, new_blue_pixel \
                    = self.apply_to_pixel(red_pixel, green_pixel, blue_pixel)
                img.putpixel((i, j), (
                    new_red_pixel, new_green_pixel, new_blue_pixel))
        return img


class BrightnessIncreaseFilter(Filter):
    """
    Фильтр увеличивает яркость каналов на пользовательское значение
    """

    def apply_to_pixel(self, red_pixel, green_pixel, blue_pixel: int) \
            -> tuple[int, int, int]:
        new_red_pixel = min(255, red_pixel + 150)
        new_green_pixel = min(255, green_pixel + 150)
        new_blue_pixel = min(255, blue_pixel + 150)
        return new_red_pixel, new_green_pixel, new_blue_pixel


class BrightnessReduceFilter(Filter):
    """
    Фильтр уменьшает яркость каналов на пользовательское значение
    """

    def apply_to_pixel(self, red_pixel, green_pixel, blue_pixel: int) \
            -> tuple[int, int, int]:
        new_red_pixel = max(0, red_pixel - 150)
        new_green_pixel = max(0, green_pixel - 150)
        new_blue_pixel = max(0, blue_pixel - 150)
        return new_red_pixel, new_green_pixel, new_blue_pixel


class InverseFilter(Filter):
    """
    Фильтр инвертирует цвета в заданной картинке
    """

    def apply_to_pixel(self, red_pixel, green_pixel, blue_pixel: int) \
            -> tuple[int, int, int]:
        new_red_pixel = 255 - red_pixel
        new_green_pixel = 255 - green_pixel
        new_blue_pixel = 255 - blue_pixel
        return new_red_pixel, new_green_pixel, new_blue_pixel
