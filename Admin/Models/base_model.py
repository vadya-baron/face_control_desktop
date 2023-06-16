import datetime
import time


class BaseScreenModel:

    _observers = []

    def add_observer(self, observer) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer) -> None:
        self._observers.remove(observer)

    def notify_observers(self, name_screen: str) -> None:
        for observer in self._observers:
            if observer.name == name_screen:
                observer.model_is_changed()
                break

    @staticmethod
    def get_date_time() -> str:
        return datetime.datetime.fromtimestamp(
            time.mktime(datetime.datetime.now().timetuple())
        ).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_date() -> str:
        return datetime.datetime.fromtimestamp(
            time.mktime(datetime.datetime.now().timetuple())
        ).strftime('%Y-%m-%d')

    @staticmethod
    def get_time() -> str:
        return datetime.datetime.fromtimestamp(
            time.mktime(datetime.datetime.now().timetuple())
        ).strftime('%H:%M:%S')
