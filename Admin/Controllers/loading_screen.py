from Models import LoadingScreenModel
from View.LoadingScreen import LoadingScreenView


class LoadingScreenController:
    def __init__(self, model: LoadingScreenModel, lang: dict):
        self.model = model
        self.lang = lang
        self.view = LoadingScreenView(controller=self, model=self.model)

    def get_view(self) -> LoadingScreenView:
        return self.view
