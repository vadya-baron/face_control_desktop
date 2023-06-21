import logging

import numpy as np

from Models import DetectScreenModel
from View import Detect


class DetectScreenController:
    def __init__(self, model: DetectScreenModel, lang: dict):
        self.model = model
        self.lang = lang
        self.view = Detect(controller=self, model=self.model)
        self._capture = None
        self._face = None
        self._face_sum = 0
        self._capture_compare = None
        self._capture_diff = None

    def get_view(self) -> Detect:
        return self.view

    def is_db_ready(self, *args) -> bool:
        return self.model.is_db_ready()

    def set_capture(self, *args) -> bool:
        return self.model.set_capture()

    def detect_video(self, *args) -> (np.ndarray, int, list):
        capture = self.model.capture_read()

        self._capture = capture

        if self._capture_compare is None:
            self._capture_compare = capture
        else:
            capture_diff = round(np.linalg.norm((self._capture_compare - capture) * 0.001), 0)
            if capture_diff is not None:
                if capture_diff == self._capture_diff:
                    self._capture_diff = capture_diff
                    return np.ndarray([]), 0, []

            self._capture_diff = capture_diff

        try:
            crop_data, messages = self.model.cropping()
        except Exception as e:
            logging.warning(e)
            return self._capture, 0, []

        if len(crop_data.shape) == 0:
            if len(messages) > 0:
                logging.warning('DetectScreenController -> detect_video -> crop_data messages: ' + ', '.join(messages))

            return self._capture, 0, []

        employee_id, messages, face = self.model.recognition(crop_data)

        if employee_id == 0:
            if self._face is None:
                self._face = face
            else:
                face_sum = 0
                try:
                    face_sum = round(np.linalg.norm(self._face - face + 0.1), 1)
                except Exception as e:
                    logging.exception(e)

                if self._face_sum == face_sum:
                    return self._capture, employee_id, []

                self._face_sum = face_sum

        if employee_id > 0:
            self.model.add_employee_statistic(employee_id)

        return self._capture, employee_id, self.get_lang_messages(messages)

    def stop_detect(self, *args) -> None:
        return self.model.stop_read()

    def load_employees(self, *args) -> None:
        self.model.load_employees()

    def get_lang_messages(self, messages: list) -> list:
        lang_messages = []
        if len(messages) > 0:
            for message in messages:
                lang = self.lang.get(message, False)
                if lang:
                    lang_messages.append(lang)

        return lang_messages

    def get_employee_photo(self, employee_id) -> str:
        return self.model.get_employee_photo(employee_id)
