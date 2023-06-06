import datetime
import time
from typing import Union


def get_time() -> str:
    """Возвращает строку с текущей датой и временем."""

    return datetime.datetime.fromtimestamp(
        time.mktime(datetime.datetime.now().timetuple())
    ).strftime("%d-%m-%Y %H:%M:%S")

class DataBaseHandler:
    def __init__(self, config: dict):
        """Подключение к базе"""
        self.db_name = ''

    def get_employes(self) -> Union[list[dict], None]:
        data = [{'id': 1, 'name': 'Vaday'}]
        time.sleep(0.3)
        return data

    def save_employee(self, data: dict) -> bool:
        if data is None:
            return False

        return True
