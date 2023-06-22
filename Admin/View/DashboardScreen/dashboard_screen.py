from typing import NoReturn, Union

from kivy.clock import Clock

from View.DashboardScreen.components import ScreenData
from View import BaseScreenView
from View.components import AppDialog, AppToast


class DashboardScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.main_container = None
        self.name = kw.get('model').name_screen
        self.dialog = AppDialog()
        self.toast = AppToast()
        # self.loading_dialog.bind(on_dismiss=self.controller.reset_data)
        self.model.add_observer(self)
        self.this_clock = Clock

    def show_dialog_wait(self) -> NoReturn:
        """Отображает диалоговое окно ожидания, пока модель обрабатывает данные."""
        self.dialog.show()

    def show_toast(self, interval: Union[int, float]) -> NoReturn:
        self.toast.show(text='Данные загружены!')

    def model_is_changed(self) -> None:
        """
        Вызывается каждый раз, когда в модели происходит какое-либо изменение.
        При изменении пользовательский интерфейс обновляется.
        """
        if self.model.data_load_status:
            self.dialog.close()
            # Clock.schedule_once(self.show_toast, 1)
        if self.model.data_load_status is False:
            self.dialog.close()
            self.dialog.show(text='Ошибка загрузки данных! Обратитесь к администратору.', auto_dismiss=False)

    def on_enter(self):
        self.controller.reset_data()
        self.main_container = self.manager_screens.children[0].children[0].ids.screen_manager.children[0].ids.container
        self.load_data()
        self.this_clock.schedule_interval(self.load_data, 10)

    def load_data(self, *args):
        self.controller.reset_data()
        data = self.controller.get_data()
        self.main_container.clear_widgets()
        self.main_container.add_widget(
            ScreenData(
                dataset=data,
                show_work_time=True
            )
        )
