
from View.DashboardScreen.dashboard_screen import DashboardScreenView


class DashboardScreenController:
    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = DashboardScreenView(controller=self, model=self.model)

    def get_view(self) -> DashboardScreenView:
        return self.view
