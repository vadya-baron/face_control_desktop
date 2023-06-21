import datetime
import logging
import time
import numpy as np
import cv2
from pathlib import Path

from Models import BaseScreenModel


class DetectScreenModel(BaseScreenModel):
    def __init__(self, config: dict, name_screen: str, debug: bool = False, **kwargs):
        self._debug = debug
        self._config = config
        self.name_screen = name_screen
        self._data_base = kwargs.get('data_base')
        self._cropping = kwargs.get('cropping')
        self._recognition = kwargs.get('recognition')
        self._capture = None
        self._frame = None
        self._observers = []
        try:
            self.capture_input = self._config['SERVICE']['capture_input']
            self.person_display_path = self._config['EMPLOYEES_CONFIG']['person_display_path']
            self.capture_width = self._config['SERVICE']['capture_width']
            self.capture_height = self._config['SERVICE']['capture_height']
            if self._config['SERVICE']['min_time_between_rec'] is None:
                self._min_time_between_rec = 60
            else:
                self._min_time_between_rec = int(self._config['SERVICE']['min_time_between_rec'])

            self.temp_dict_of_employees = {}

        except Exception as e:
            logging.exception(e)
            exit(1)

    def is_db_ready(self) -> bool:
        return self._data_base.is_db_ready()

    def cropping(self) -> (np.ndarray, list):
        return self._cropping.cropping(self._frame)

    def add_employee_statistic(self, employee_id: int) -> bool:
        if employee_id <= 0:
            return True

        test_time = int(time.time())
        new_employee = False

        if self.temp_dict_of_employees.get(employee_id) is None:
            self.temp_dict_of_employees[employee_id] = {'last_time_rec': test_time + self._min_time_between_rec}
            new_employee = True

        if new_employee is False and int(self.temp_dict_of_employees[employee_id]['last_time_rec']) > test_time:
            return True

        try:
            last_visit = self._data_base.get_last_visit(employee_id, {
                'date_from': '{date:%Y-%m-%d 00:00:00}'.format(date=datetime.datetime.now())
            })

            if last_visit.get('direction', 1) == 1:
                direction = 0
            else:
                direction = 1

            self._data_base.add_visit(employee_id, direction)
            self.temp_dict_of_employees[employee_id]['last_time_rec'] = test_time + self._min_time_between_rec
        except Exception as e:
            logging.exception(e)
            return False

        return True

    def capture_read(self, *args) -> np.ndarray:
        ret, frame = self._capture.read()
        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        #rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        self._frame = frame

        return self._frame

    def recognition(self, crop_data: np.ndarray, *args) -> (int, list):
        return self._recognition.recognition(crop_data)

    def stop_read(self, *args) -> None:
        self._capture.release()
        cv2.destroyAllWindows()

    def set_capture(self) -> bool:
        try:
            self._capture = cv2.VideoCapture(self.capture_input)
            if self._capture.isOpened():
                self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.capture_width))
                self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.capture_height))
        except Exception as e:
            logging.exception(e)
            return False

        return True

    def get_employee_photo(self, employee_id) -> str:
        if self.person_display_path[:2] == './' or self.person_display_path[:2] == '..':
            export_path = Path(Path.cwd(), self.person_display_path)
        else:
            export_path = self.person_display_path

        return str(export_path) + '/' + str(employee_id) + '.jpg'

    def load_employees(self) -> None:
        active_employees = self._data_base.get_employees(statuses=[1])
        if len(active_employees) == 0:
            logging.warning('load_employees -> active_employees = notfound')
            self.notify_observers(self.name_screen, load_employees=False)
            return

        employees_ids = []
        for employee in active_employees:
            employees_ids.append(employee['id'])

        active_vectors = self._data_base.get_vectors(employees_ids)
        if len(active_vectors) == 0:
            logging.warning('load_employees -> active_vectors = notfound')
            self.notify_observers(self.name_screen, error=True)
            return

        blocked_employees = self._data_base.get_employees(statuses=[2])
        blocked_vectors = []
        if len(blocked_employees) > 0:
            blocked_employees_ids = []
            for employee in blocked_employees:
                blocked_employees_ids.append(employee['id'])
            blocked_vectors = self._data_base.get_vectors(blocked_employees_ids)
            if len(blocked_vectors) == 0:
                logging.warning('load_employees -> blocked_vectors = notfound')
                self.notify_observers(self.name_screen, error=True)
                return

        try:
            self._recognition.load_vectors(
                active_employees=active_employees,
                blocked_employees=blocked_employees,
                active_vectors=active_vectors,
                blocked_vectors=blocked_vectors
            )
        except Exception as e:
            logging.exception(e)
            self.notify_observers(self.name_screen, error=True)
            return

        self.notify_observers(self.name_screen, load_employees=True)
