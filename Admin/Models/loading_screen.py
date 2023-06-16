from Models.base_model import BaseScreenModel


class LoadingScreenModel(BaseScreenModel):
    def __init__(self, config: dict, name_screen: str, debug: bool = False, **kwargs):
        self._debug = debug
        self._config = config
        self.name_screen = name_screen
        self._observers = []
