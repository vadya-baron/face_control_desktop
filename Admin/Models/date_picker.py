import locale

from kivy.properties import StringProperty
from kivymd.uix.pickers import MDDatePicker


class BaseDatePicker(MDDatePicker):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    title = StringProperty('Выберите дату')
    title_input = StringProperty('Введите дату')
    pass
