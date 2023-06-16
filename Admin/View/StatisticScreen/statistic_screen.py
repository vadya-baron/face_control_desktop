from View import BaseScreenView
from View.StatisticScreen.components import ScreenData
from View.components import AppDialog, AppToast


class StatisticScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main_container = None
        self.name = kw.get('model').name_screen
        self.dialog = AppDialog()
        self.toast = AppToast()
        # self.loading_dialog.bind(on_dismiss=self.controller.reset_data)
        self.model.add_observer(self)

    def model_is_changed(self) -> None:
        pass

    def on_enter(self):
        self.main_container = self.manager_screens.children[0].children[0].ids.screen_manager.children[0].ids.container

        self.main_container.clear_widgets()
        self.main_container.add_widget(
            ScreenData(
                screen_title='Статистика сотрудников',
                notfound_message='Нет данных',
                dataset=[],
                today=False,
                actions={'upload_data': self.upload_data, 'upload_file': self.upload_file}
            )
        )

    def upload_data(self, **kwargs):
        self.controller.reset_data()
        filter = kwargs.get('filter', {})
        dataset = self.controller.get_data(filter)

        if len(dataset) == 0:
            self.main_container.clear_widgets()
            self.main_container.add_widget(
                ScreenData(
                    screen_title='Статистика сотрудников',
                    notfound_message='Нет данных',
                    dataset=[],
                    filter=filter,
                    today=False,
                    actions={'upload_data': self.upload_data, 'upload_file': self.upload_file}
                )
            )
            self.toast.show('Данные не найдены')
        else:
            self.main_container.clear_widgets()
            self.main_container.add_widget(
                ScreenData(
                    screen_title='Статистика сотрудников',
                    notfound_message='Нет данных',
                    dataset=dataset,
                    filter=filter,
                    today=False,
                    actions={'upload_data': self.upload_data, 'upload_file': self.upload_file}
                )
            )
            self.toast.show('Данные загружены')

    def upload_file(self, **kwargs):
        filter = kwargs.get('filter', {})
        file_ext = kwargs.get('file_ext', 'xlsx')
        file_path = self.controller.upload_file(filter, file_ext)

        if file_path != '':
            self.toast.show('Данные выгружены в файл: ' + file_path)
        else:
            self.toast.show('Ошибка выгрузки данных', 'error')
