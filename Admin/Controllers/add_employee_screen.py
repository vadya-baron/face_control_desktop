import logging

from Models import AddEmployeeScreenModel
from View.EmployeesScreen import AddEmployeeScreenView


class AddEmployeeScreenController:
    def __init__(self, model: AddEmployeeScreenModel, lang: dict):
        self.model = model
        self.lang = lang
        self.view = AddEmployeeScreenView(controller=self, model=self.model)

    def get_view(self) -> AddEmployeeScreenView:
        return self.view

    def save_employee(self, employee_data: dict, employee_photos: list) -> (bool, list):
        messages = []
        if employee_data.get('display_name') is None:
            messages.append(self.lang.get('enter_employee_full_name', ''))

        if employee_data.get('employee_position') is None:
            messages.append(self.lang.get('enter_employee_position', ''))

        if len(employee_photos) == 0:
            messages.append(self.lang.get('not_single_photo_has_been_added', ''))

        if len(messages) > 0:
            return False, messages

        employee_id = self.model.save_employee(employee_data)
        if employee_id is False:
            messages.append(self.lang.get('employee_record_failed', ''))
            return False, messages

        first_image = None
        count = 1
        for image in employee_photos:
            try:
                face_vector = self.model.get_crop(str(employee_id), image)
                if len(face_vector) == 0:
                    self.model.remove_data(employee_id)
                    messages.append(self.lang.get('i_can_identify_the_face_in_the_photo', ''))
                    return False, messages
            except Exception as e:
                logging.error('Error: get_crop')
                logging.exception(e)
                self.model.remove_data(employee_id)
                messages.append(self.lang.get('i_can_identify_the_face_in_the_photo', ''))
                return False, messages

            if count == 1:
                first_image = face_vector

            count += 1

            face_recognize_vector, mess = self.model.get_face_encodings(face_vector)
            if len(face_recognize_vector) == 0:
                self.model.remove_data(employee_id)
                if len(mess) > 0:
                    for mes_item in mess:
                        messages.append(self.lang.get(str(mes_item), ''))
                else:
                    messages.append(self.lang.get('i_can_identify_the_face_in_the_photo', ''))

                return False, messages

            if not self.model.add_employee_vectors(int(employee_id), face_vector, face_recognize_vector):
                self.model.remove_data(employee_id)
                messages.append(self.lang.get('employee_record_failed', ''))
                return False, messages

        if first_image is not None:
            if not self.model.save_person_display(str(employee_id), first_image):
                self.model.remove_data(employee_id)
                messages.append(self.lang.get('employee_record_failed', ''))
                return False, messages

        messages.append(self.lang.get('employee_added', ''))

        return True, messages

    def get_data(self, employee_id: int | str) -> dict:
        if employee_id is None:
            return {}

        return self.model.get_data(int(employee_id))

    def set_data(self, employee: dict) -> dict:
        if employee is None:
            return {}

        return self.model.get_data(int(id))


