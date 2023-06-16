import logging
import datetime
from Models.base_model import BaseScreenModel


class DashboardScreenModel(BaseScreenModel):
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

        employees = self._data_base.get_employees({'status': 1})
        if len(employees) == 0:
            return []

        for employee in employees:
            employee['photo'] = self._person_display_path + str(employee['id']) + '.jpg'

        date = '{date:%Y-%m-%d}'.format(date=datetime.datetime.now())
        statistics = self._data_base.get_visits({
            'date_from': date + ' 00:00:00',
            'date_to': date + ' 23:59:59',
            'limit': 10000
        })

        if len(statistics) == 0:
            self.data = employees
            return self.data

        stat_dict = {}
        for item in statistics:
            if stat_dict.get(item['employee_id']):
                stat_dict[item['employee_id']].append(item)
            else:
                stat_dict[item['employee_id']] = []
                stat_dict[item['employee_id']].append(item)

        for employee in employees:
            time_go_work = stat_dict.get(employee['id'])
            if time_go_work is None:
                continue
            else:
                if len(time_go_work) == 0:
                    employee['time_go_work'] = {}
                    continue

                if len(time_go_work) == 1:
                    employee['time_go_work'] = {
                        'entered_time': self._get_start_and_end_time(time_go_work, True)
                    }
                    continue

                time_go_work = time_go_work[::len(time_go_work) - 1]

                try:
                    if int(time_go_work[0]['direction']) == 0:
                        employee['time_go_work'] = {
                            'entered_time': self._get_start_and_end_time(time_go_work, False)
                        }
                        continue
                except IndexError:
                    employee['time_go_work'] = {
                        'entered_time': self._get_start_and_end_time(time_go_work, False)
                    }
                    continue

                employee['time_go_work'] = {
                    'entered_time': self._get_start_and_end_time(time_go_work, False),
                    'came_out_time': self._get_start_and_end_time(time_go_work, True)
                }

        self.data = employees

        return self.data

    # HELPERS
    @staticmethod
    def _get_start_and_end_time(data: list, start: bool) -> str:
        try:
            if start:
                return data[0]['visit_date'][-8:-3]
            else:
                return data[-1]['visit_date'][-8:-3]
        except IndexError:
            return ''
