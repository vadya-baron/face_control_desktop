import face_recognition
import numpy as np


class Recognition:
    def __init__(self, config: dict, debug: bool = False):
        self._debug = debug
        self._config = config

    @staticmethod
    def get_face_encodings(image: np.ndarray) -> (np.array, list):
        if len(image) == 0:
            return 0, []

        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 1:
            return np.array(()), ['only_one_face']

        if len(encodings) == 0:
            return np.array(()), ['i_can_identify_the_face_in_the_photo']

        return encodings[0], []
