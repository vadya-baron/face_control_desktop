import logging
from Models.base_model import BaseScreenModel


class StatisticTodayScreenModel(BaseScreenModel):
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

    def get_data(self, for_date):
        if len(self.data) > 0:
            return self.data

        dataset = {}
        employees = self._data_base.get_employees({'status': 1})
        if len(employees) == 0:
            return []

        list_start, list_end = self._data_base.get_start_end_working(for_date)

        if len(list_start) == 0:
            return []

        for employee in employees:
            dataset[employee['id']] = employee
            dataset[employee['id']]['stat'] = {'start_date': '', 'end_date': ''}

        for item in list_start:
            if dataset.get(item['employee_id']) is None:
                continue
            else:
                stat = {'start_date': item.get('visit_date'), 'end_date': '--:--', 'id': item.get('id')}

                dataset[item['employee_id']]['stat'] = stat

        if len(list_end) == 0:
            self.data = self._get_list_data(dataset)
            return self.data

        for item in list_end:
            if dataset.get(item['employee_id']) is None:
                continue
            else:
                if dataset[item['employee_id']]['stat']['id'] != item['id']:
                    dataset[item['employee_id']]['stat']['end_date'] = item.get('visit_date')
                else:
                    continue

        self.data = self._get_list_data(dataset)
        return self.data

    def _get_list_data(self, dataset) -> list[dict]:
        if len(dataset) == 0:
            return []

        list_data = []

        for employee_id in dataset:
            dataset[employee_id]['photo'] = self._person_display_path + str(employee_id) + '.jpg'
            list_data.append(dataset[employee_id])

        return list_data
