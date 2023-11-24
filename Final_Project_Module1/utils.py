from filters import BrightnessIncreaseFilter, BrightnessReduceFilter, \
                    InverseFilter

filters = {
    1: {
        "name": "Inverse Filter",
        "description": "Этот фильтр конвертирует картинку в черно-белый.",
        "class": InverseFilter(),
    },
    2: {
        "name": "Brightness Increase Filter",
        "description": "Этот фильтр увеличит яркость на значение пользователя",
        "class": BrightnessIncreaseFilter(),
    },
    3: {
        "name": "Brightness Reduce Filter",
        "description": "Этот фильтр уменьшает яркость на значение пользователя",
        "class": BrightnessReduceFilter(),

    }
}
