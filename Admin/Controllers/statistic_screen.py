import logging
from pathlib import Path
from typing import NoReturn
import datetime
import pandas as pd

from Models import StatisticScreenModel
from Utilits import Helpers
from View.StatisticScreen import StatisticScreenView


class StatisticScreenController:
    def __init__(self, model: StatisticScreenModel, lang: dict):
        self.model = model
        self.lang = lang
        self.helpers = Helpers()
        self.view = StatisticScreenView(controller=self, model=self.model)

    def get_view(self) -> StatisticScreenView:
        return self.view

    def reset_data(self, *args) -> NoReturn:
        self.model.reset_data()

    def get_data(self, filter_data: dict) -> list[dict]:
        return self.model.get_data(self._get_statistic_filter(filter_data))

    def upload_file(self, filter_data: dict, file_ext: str = 'xlsx') -> str:
        filter_data['all_data'] = True
        data = self.model.get_data(self._get_statistic_filter(filter_data))

        if len(data) == 0:
            return ''

        export_path = self.model.get_export_path(file_ext)
        try:
            if self._export_file(data, export_path, file_ext):
                return export_path
        except Exception as e:
            logging.exception(e)

        return ''

    def _get_statistic_filter(self, filter_data: dict) -> dict:
        filters = {}

        id = filter_data.get('id')
        employee_id = filter_data.get('employee_id')
        employees_ids = filter_data.get('employee_ids')
        ids = filter_data.get('ids')
        date_from = filter_data.get('date_from')
        date_to = filter_data.get('date_to')
        direction = filter_data.get('direction')
        all_data = filter_data.get('all_data')
        limit = int(filter_data.get('limit', 0))
        page = int(filter_data.get('page', 0))

        # params
        if employee_id is not None:
            employee_id = int(employee_id)

        if id is not None:
            id = int(id)

        if all_data is not None:
            all_data = int(all_data)

        if direction is not None:
            direction = int(direction)

        if date_from is None or date_from == '':
            date_from = '{date:%Y-%m-%d 00:00:00}'.format(date=datetime.datetime.now())
        else:
            date_from = str(date_from) + ' 00:00:00'

        if date_to is None or date_to == '':
            date_to = '{date:%Y-%m-%d 23:59:59}'.format(date=datetime.datetime.now())
        else:
            date_to = str(date_to) + ' 23:59:59'

        # filters
        if employee_id is not None and employee_id > 0:
            filters['employee_id'] = employee_id

        if id is not None and id > 0:
            filters['id'] = id

        if employees_ids is not None and len(employees_ids) > 0:
            employees_ids = list(map(lambda item_id: self.helpers.escape(item_id), employees_ids))
            filters['employee_ids'] = employees_ids

        if ids is not None and len(ids) > 0:
            ids = list(map(lambda item_id: self.helpers.escape(item_id), ids))
            filters['ids'] = ids

        if date_from is not None and date_from != '':
            filters['date_from'] = date_from

        if date_to is not None and date_to != '':
            filters['date_to'] = date_to

        if direction is not None:
            filters['direction'] = direction

        if all_data is not None and all_data == 1:
            return filters

        if limit > 0:
            filters['limit'] = limit
        else:
            filters['limit'] = 100

        if page > 0:
            filters['page'] = page
        else:
            filters['page'] = 1

        return filters

    @staticmethod
    def _export_file(data: list[dict], export_path: str, file_ext: str) -> bool:
        format_data = []

        for item in data:
            visit_date = item.get('visit_date')
            date_time = visit_date[:-3]
            date = visit_date[:-9]

            if item.get('direction') == 1:
                start_time = ''
                end_time = date_time
            else:
                start_time = date_time
                end_time = ''

            format_data.append({
                'date': date,
                'display_name': item.get('display_name'),
                'start_time': start_time,
                'end_time': end_time,
            })

        df = pd.DataFrame(format_data)
        df.columns = ['Дата', 'ФИО', 'Пришел', 'Ушел']
        df.index = df['Дата']
        df.drop('Дата', axis=1, inplace=True)

        if export_path[:2] == './' or export_path[:2] == '..':
            export_path = Path(Path.cwd(), export_path)

        if file_ext == 'csv':
            df.to_csv()
        elif file_ext == 'html':
            df.to_html(export_path)
        else:
            df.to_excel(export_path)

        return True
