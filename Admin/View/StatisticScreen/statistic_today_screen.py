from View import BaseScreenView
from View.StatisticScreen.components import ScreenData
from View.components import AppDialog, AppToast


class StatisticTodayScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main_container = None
        self.name = kw.get('model').name_screen
        self.dialog = AppDialog()
        self.toast = AppToast()
        self.model.add_observer(self)

    def model_is_changed(self) -> None:
        pass

    def on_enter(self):
        data = self.controller.get_data()
        self.main_container = self.manager_screens.children[0].children[0].ids.screen_manager.children[0].ids.container

        self.main_container.clear_widgets()
        self.main_container.add_widget(
            ScreenData(
                screen_title='Статистика за сегодня',
                notfound_message='Нет данных',
                dataset=data,
                today=True,
                actions={'update_data': self.update_data, 'upload_file': self.upload_file}
            )
        )

    def update_data(self, **kwargs):
        self.controller.reset_data()
        data = self.controller.get_data()
        self.main_container.clear_widgets()
        self.main_container.add_widget(
            ScreenData(
                screen_title='Статистика за сегодня',
                notfound_message='Нет данных',
                dataset=data,
                today=True,
                actions={'update_data': self.update_data, 'upload_file': self.upload_file}
            )
        )
        self.toast.show('Данные обновлены')

    def upload_file(self, **kwargs):
        file_ext = kwargs.get('file_ext', 'xlsx')
        file_path = self.controller.upload_file(file_ext=file_ext)

        if file_path != '':
            self.toast.show('Данные выгружены в файл: ' + file_path)
        else:
            self.toast.show('Ошибка выгрузки данных', 'error')
