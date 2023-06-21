import logging

import face_recognition
import numpy as np


class Recognition:
    def __init__(self, config: dict, debug: bool = False):
        self._debug = debug
        self._config = config
        self._tolerance = float(config['tolerance'])
        self._active_employees = []
        self._blocked_employees = []
        self._persons_display_names = {}
        self._known_face_encodings = {}
        self._blocked_known_face_encodings = []
        if self._tolerance <= 0.1:
            raise Exception('Слишком маленький допуск. Измените параметр tolerance')

    def load_vectors(
            self,
            active_employees: list[dict],
            blocked_employees: list[dict],
            active_vectors: list[dict],
            blocked_vectors: list[dict]
    ) -> None:
        self._active_employees = []
        self._blocked_employees = []
        self._persons_display_names = {}
        self._known_face_encodings = {}
        self._blocked_known_face_encodings = []

        if len(active_employees) == 0:
            raise Exception('Нет ни одного сотрудника')

        if len(active_vectors) == 0:
            raise Exception('Нет векторов для сотрудников')

        if len(blocked_employees) > 0 and len(blocked_vectors) == 0:
            raise Exception('Нет векторов для блокированных сотрудников')

        for employee in active_employees:
            self._persons_display_names[str(employee['id'])] = employee['display_name']

        # persons_vectors
        for vector in active_vectors:
            if self._known_face_encodings.get(str(vector['employee_id'])):
                self._known_face_encodings[str(vector['employee_id'])].append(vector['face_recognize_vector'])
            else:
                self._known_face_encodings[str(vector['employee_id'])] = [vector['face_recognize_vector']]

        if len(self._known_face_encodings) == 0:
            raise Exception('Нет векторов для блокированных сотрудников')
        else:
            logging.info('Загружено персон: ' + str(len(self._known_face_encodings)))

        if len(blocked_employees) > 0:
            for vector in blocked_vectors:
                self._blocked_known_face_encodings.append(vector['face_recognize_vector'])

    def recognition(self, image: np.ndarray) -> (int, list, np.ndarray):
        if len(image) == 0:
            return 0, [], np.ndarray([])

        encodings = face_recognition.face_encodings(image)
        if len(encodings) == 0:
            return 0, [], np.ndarray([])

        if len(encodings) > 1:
            return 0, ['only_one_face'], np.ndarray([])

        first_encoding = encodings[len(encodings)-1]
        # Сначала пробежим по блокированным
        if len(self._blocked_known_face_encodings) > 0:
            matches = face_recognition.compare_faces(
                self._blocked_known_face_encodings,
                first_encoding,
                tolerance=self._tolerance
            )
            matches_sum = sum(matches)
            if matches_sum >= 1:
                return -1, ['access_denied'], first_encoding

        for personId, person_faces in self._known_face_encodings.items():
            matches = face_recognition.compare_faces(person_faces, first_encoding, tolerance=self._tolerance)

            matches_sum = sum(matches)
            if matches_sum == 0:
                continue

            tolerance = matches_sum / len(matches)
            if tolerance >= self._tolerance:
                return int(personId), [
                    'confirmed_person',
                    self._persons_display_names[str(personId)],
                    'recognition_success'
                ], first_encoding

        return 0, ['unknown_person'], first_encoding

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
