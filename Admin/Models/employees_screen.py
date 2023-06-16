import logging
from Models.base_model import BaseScreenModel


class EmployeesScreenModel(BaseScreenModel):
    def __init__(self, config: dict, name_screen: str, debug: bool = False, **kwargs):
        self._debug = debug
        self._data_load_status = None
        self._data_base = kwargs.get('data_base')
        self._config = config
        self._person_display_path = self._config['EMPLOYEES_CONFIG']['person_display_path']
        self.data = []
        self.name_screen = name_screen
        self._observers = []

    def reset_data(self):
        self.data = []

    def get_data(self):
        if len(self.data) > 0:
            return self.data

        employees = self._data_base.get_employees({})
        if len(employees) == 0:
            return []

        for employee in employees:
            employee['photo'] = self._person_display_path + str(employee['id']) + '.jpg'

        self.data = employees

        return self.data

    def block_employee(self, employee_id: int):
        return self.update_status(employee_id, 2)

    def unblock_employee(self, employee_id: int):
        return self.update_status(employee_id, 1)

    def update_status(self, employee_id: int, status: int):
        if self._data_base.update_status_employee(employee_id, status):
            employees = self._data_base.get_employees({})
            if len(employees) == 0:
                return []

            for employee in employees:
                employee['photo'] = self._person_display_path + str(employee['id']) + '.jpg'

            self.data = employees
            self.notify_observers(self.name_screen)
            return True

        return False

    def remove_employee(self, employee_id: int):
        if self._data_base.remove_employee(employee_id):
            return True

        return False
