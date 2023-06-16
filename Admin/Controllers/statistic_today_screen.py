import logging
from pathlib import Path
from typing import NoReturn
import datetime
import pandas as pd

from Models import StatisticTodayScreenModel
from Utilits import Helpers
from View.StatisticScreen import StatisticTodayScreenView


class StatisticTodayScreenController:
    def __init__(self, model: StatisticTodayScreenModel, lang: dict):
        self.model = model
        self.lang = lang
        self.helpers = Helpers()
        self.view = StatisticTodayScreenView(controller=self, model=self.model)

    def get_view(self) -> StatisticTodayScreenView:
        return self.view

    def reset_data(self, *args) -> NoReturn:
        self.model.reset_data()

    def upload_file(self, for_date: str = '', file_ext: str = 'xlsx') -> str:
        data = self.model.get_data(self.get_for_date(for_date))

        if len(data) == 0:
            return ''

        export_path = self.model.get_export_path(file_ext)
        try:
            if self._export_file(data, export_path, file_ext):
                return export_path
        except Exception as e:
            logging.exception(e)

        return ''

    def get_data(self, for_date: str = '') -> list[dict]:
        return self.model.get_data(self.get_for_date(for_date))

    def get_for_date(self, for_date: str = ''):
        if for_date is None or for_date == '':
            for_date = '{date:%Y-%m-%d}'.format(date=datetime.datetime.now())
        else:
            if self.helpers.date_validate(for_date) is False:
                for_date = '{date:%Y-%m-%d}'.format(date=datetime.datetime.now())

        return for_date

    @staticmethod
    def _export_file(data: list[dict], export_path: str, file_ext: str) -> bool:
        format_data = []

        for item in data:
            stat = item.get('stat')
            end_date = stat.get('end_date')
            start_date = stat.get('start_date')
            if start_date is None or start_date == '--:--' or start_date == '':
                continue

            date_time = start_date[:-3]
            date = start_date[:-9]

            format_data.append({
                'date': date,
                'display_name': item.get('display_name'),
                'start_time': date_time,
                'end_time': end_date,
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
