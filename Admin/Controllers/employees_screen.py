from typing import NoReturn

from Models import EmployeesScreenModel
from View.EmployeesScreen import EmployeesScreenView


class EmployeesScreenController:
    def __init__(self, model: EmployeesScreenModel, lang: dict):
        self.model = model
        self.lang = lang
        self.view = EmployeesScreenView(controller=self, model=self.model)

    def get_view(self) -> EmployeesScreenView:
        return self.view

    def reset_data(self, *args) -> NoReturn:
        self.model.reset_data()

    def get_data(self) -> list[dict]:
        return self.model.get_data()

    def block_employee(self, employee_id: int) -> bool:
        if employee_id == 0:
            return False

        return self.model.block_employee(employee_id)

    def unblock_employee(self, employee_id: int) -> bool:
        if employee_id == 0:
            return False

        return self.model.unblock_employee(employee_id)

    def remove_employee(self, employee_id: int) -> bool:
        if employee_id == 0:
            return False

        return self.model.remove_employee(employee_id)
