import logging
import datetime
import pickle
import numpy as np
import os
import cv2

from Models.base_model import BaseScreenModel


class AddEmployeeScreenModel(BaseScreenModel):
    def __init__(self, config: dict, name_screen: str, debug: bool = False, **kwargs):
        self._debug = debug
        self._data_load_status = None
        self._data_base = kwargs.get('data_base')
        self._cropping = kwargs.get('cropping')
        self._recognition = kwargs.get('recognition')
        self._config = config
        self._dataset_path = self._config['CROPPING_CONFIG']['dataset_path']
        self._person_display_path = self._config['EMPLOYEES_CONFIG']['person_display_path']
        self.data = None
        self.name_screen = name_screen
        self._observers = []

        if self._config['CROPPING_CONFIG']['crop_size_width'] is None:
            self._crop_size_width = 0
        else:
            self._crop_size_width = int(self._config['CROPPING_CONFIG']['crop_size_width'])

        if self._config['CROPPING_CONFIG']['crop_size_height'] is None:
            self._crop_size_height = 0
        else:
            self._crop_size_height = int(self._config['CROPPING_CONFIG']['crop_size_height'])

    def save_employee(self, employee_data: dict):
        date = self.get_date_time()
        employee_data['date_create'] = date
        employee_data['date_update'] = date

        if employee_data.get('external_id') is None:
            employee_data['external_id'] = None

        if employee_data.get('external_id') is None:
            employee_data['external_id'] = 0

        if employee_data.get('status') is None:
            employee_data['status'] = 1

        employee_id = self._data_base.save_employee(employee_data)
        if employee_id is None or employee_id is False:
            return False

        return employee_id

    def add_employee_vectors(self, employee_id: int, face_vector: np.ndarray, face_recognize_vector: np.array) -> bool:
        employee_data = {'employee_id': employee_id, 'face_vector': pickle.dumps(face_vector),
                         'face_recognize_vector': pickle.dumps(face_recognize_vector)}

        return self._data_base.add_employee_vectors(employee_data)

    def get_data(self, id: int):
        try:
            self.data = self._data_base.get_employee(id)
        except Exception as e:
            logging.exception(e)
            self.data = {}

        return self.data

    def save_person_display(self, employee_id: str, first_image: np.ndarray):
        try:
            cv2.imwrite(self._person_display_path + employee_id + '.jpg', first_image)
        except Exception as e:
            logging.exception(e)
            return False

        return True

    def get_crop(
            self,
            employee_id: str,
            data: np.ndarray
    ) -> np.ndarray:
        if len(data) > 0:
            crop_data, messages = self._cropping.cropping(data)

            if len(crop_data) == 0:
                return np.ndarray((0,))

            if self._crop_size_width > 0 and self._crop_size_height > 0:
                small = cv2.resize(
                    crop_data,
                    (self._crop_size_width, self._crop_size_height),
                    interpolation=cv2.INTER_LINEAR
                )
            elif self._crop_size_width > 0 and self._crop_size_height == 0:
                height = crop_data.shape[0]
                width = crop_data.shape[1]
                ratio = self._crop_size_width / width
                new_height = int(height * ratio)
                small = cv2.resize(
                    crop_data,
                    (self._crop_size_width, new_height),
                    interpolation=cv2.INTER_LINEAR
                )
            else:
                small = cv2.resize(crop_data, (0, 0), fx=0.5, fy=0.5)

            cv2.imwrite(
                self._dataset_path + 'employee_id_' + employee_id + '_' +
                '{date:%Y-%m-%d_%H-%M-%S}'.format(date=datetime.datetime.now()) + '.jpg',
                small
            )

            return small

        return np.ndarray((0,))

    def get_face_encodings(self, face_vector: np.ndarray) -> (np.array, list):
        return self._recognition.get_face_encodings(face_vector)

    def remove_data(self, employee_id: str) -> bool:
        if self._data_base.remove_employee(int(employee_id)) is False:
            return False

        try:
            os.remove(self._person_display_path + str(employee_id) + '.jpg')
        except Exception as e:
            logging.exception(e)

        return True
