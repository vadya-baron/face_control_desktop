from typing import NoReturn

from Models import DashboardScreenModel
from View.DashboardScreen import DashboardScreenView


class DashboardScreenController:
    def __init__(self, model: DashboardScreenModel, lang: dict):
        self.model = model
        self.lang = lang
        self.view = DashboardScreenView(controller=self, model=self.model)

    def get_view(self) -> DashboardScreenView:
        return self.view

    def reset_data(self, *args) -> NoReturn:
        self.model.reset_data()

    def get_data(self) -> list[dict]:
        return self.model.get_data()
