import os
import cv2
import numpy as np


class Cropping:
    def __init__(self, config: dict, debug: bool = False):
        self._debug = debug
        self._config = config

        cascade = self._config['cascade']
        self._filling = self._config['filling']

        if not os.path.isfile(cascade):
            raise Exception(f'Файл {cascade} не найден')

        if self._config['crop_size_width'] is None:
            self._crop_size_width = 0
        else:
            self._crop_size_width = int(self._config['crop_size_width'])

        if self._config['crop_size_height'] is None:
            self._crop_size_height = 0
        else:
            self._crop_size_height = int(self._config['crop_size_height'])

        self._face_cascade = cv2.CascadeClassifier(cascade)

    def cropping(self, image: np.ndarray) -> (np.ndarray, list):
        faces = self._face_cascade.detectMultiScale(image)
        face = np.array([])
        messages = []

        if len(faces) == 0:
            messages.append('no_face')
            return np.array([]), messages

        if len(faces) > 1:
            messages.append('only_one_face')
            return np.array([]), messages

        for x, y, width, height in faces:
            cropped = image[y:y + height, x:x + width]

            if self._crop_size_width > 0 and self._crop_size_height > 0:
                face = cv2.resize(
                    cropped,
                    (self._crop_size_width, self._crop_size_height),
                    interpolation=cv2.INTER_LINEAR
                )
            elif self._crop_size_width > 0 and self._crop_size_height == 0:
                height = cropped.shape[0]
                width = cropped.shape[1]
                ratio = self._crop_size_width / width
                new_height = int(height * ratio)
                face = cv2.resize(
                    cropped,
                    (self._crop_size_width, new_height),
                    interpolation=cv2.INTER_LINEAR
                )

        return face, messages
