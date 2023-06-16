from View.EmployeesScreen.components import ScreenData
from View import BaseScreenView
from View.components import AppDialog, AppToast


class EmployeesScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main_container = None
        self.name = kw.get('model').name_screen
        self.dialog = AppDialog()
        self.toast = AppToast()
        # self.loading_dialog.bind(on_dismiss=self.controller.reset_data)
        self.model.add_observer(self)

    def model_is_changed(self) -> None:
        self.get_on_load_data()

    def on_enter(self):
        self.get_on_load_data()

    def employee_block(self, **kwargs):
        if self.controller.block_employee(int(kwargs.get('id', 0))):
            self.toast.show('Сотрудник заблокирован')
        else:
            self.toast.show('Не удалось заблокировать сотрудника', 'error')

    def employee_unblock(self, **kwargs):
        if self.controller.unblock_employee(int(kwargs.get('id', 0))):
            self.toast.show('Сотрудник разблокирован')
        else:
            self.toast.show('Не удалось разблокировать сотрудника', 'error')

    def remove_employee(self, **kwargs):
        if self.controller.remove_employee(int(kwargs.get('id', 0))):
            self.controller.reset_data()
            data = self.controller.get_data()

            self.main_container.clear_widgets()
            self.main_container.add_widget(
                ScreenData(
                    screen_title='Сотрудники',
                    notfound_message='Сотрудники не найдены',
                    dataset=data,
                    actions={
                        'employee_block': self.employee_block,
                        'employee_unblock': self.employee_unblock,
                        'remove_employee': self.remove_employee
                    }
                )
            )
            self.toast.show('Сотрудник удален')
        else:
            self.toast.show('Не удалось удалить сотрудника', 'error')

    def get_on_load_data(self):
        self.controller.reset_data()
        data = self.controller.get_data()
        self.main_container = self.manager_screens.children[0].children[0].ids.screen_manager.children[0].ids.container

        self.main_container.clear_widgets()
        self.main_container.add_widget(
            ScreenData(
                screen_title='Сотрудники',
                notfound_message='Сотрудники не найдены',
                dataset=data,
                actions={
                    'employee_block': self.employee_block,
                    'employee_unblock': self.employee_unblock,
                    'remove_employee': self.remove_employee
                }
            )
        )
