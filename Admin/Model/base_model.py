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
