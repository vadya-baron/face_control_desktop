import logging
from Models.base_model import BaseScreenModel


class StatisticScreenModel(BaseScreenModel):
    def __init__(self, config: dict, name_screen: str, debug: bool = False, **kwargs):
        self._debug = debug
        self._data_load_status = None
        self._data_base = kwargs.get('data_base')
        self._config = config
        self._person_display_path = self._config['EMPLOYEES_CONFIG']['person_display_path']
        self._export_path = self._config['SERVICE']['export_path']
        self.data = []
        self.name_screen = name_screen
        self._observers = []

    def reset_data(self):
        self.data = []

    def get_export_path(self, file_ext: str):
        return self._export_path + self.get_date_time() + '.' + file_ext

    def get_data(self, filters: dict) -> list[dict]:
        if len(self.data) > 0:
            return self.data

        employees = self._data_base.get_employees(filters)
        if len(employees) == 0:
            return []

        employees_dict = {}
        for item in employees:
            employees_dict[item['id']] = item

        employees_visits = self._data_base.get_visits(filters)
        if len(employees_visits) == 0:
            return []

        for item in employees_visits:
            employee = employees_dict.get(item['employee_id'])

            if employee is not None:
                item['display_name'] = employee.get('display_name')
                item['employee_position'] = employee.get('employee_position')

        self.data = employees_visits

        return self.data

    def _get_list_data(self, dataset) -> list[dict]:
        if len(dataset) == 0:
            return []

        list_data = []

        for employee_id in dataset:
            dataset[employee_id]['photo'] = self._person_display_path + str(employee_id) + '.jpg'
            list_data.append(dataset[employee_id])

        return list_data
