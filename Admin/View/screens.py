from Controllers import (
    LoadingScreenController,
    StatisticScreenController,
    DashboardScreenController,
    StatisticTodayScreenController,
    AddEmployeeScreenController,
    EmployeesScreenController
)

from Models import (
    LoadingScreenModel,
    DashboardScreenModel,
    StatisticScreenModel,
    StatisticTodayScreenModel,
    EmployeesScreenModel,
    AddEmployeeScreenModel
)

screens = {
    'loading_screen': {
        'model': LoadingScreenModel,
        'controller': LoadingScreenController,
        'components': {'data_base': False, 'cropping': False, 'recognition': False},
    },
    'dashboard_screen': {
        'model': DashboardScreenModel,
        'controller': DashboardScreenController,
        'components': {'data_base': True, 'cropping': False, 'recognition': False},
    },
    'statistic_screen': {
        'model': StatisticScreenModel,
        'controller': StatisticScreenController,
        'components': {'data_base': True, 'cropping': False, 'recognition': False},
    },
    'statistic_today_screen': {
        'model': StatisticTodayScreenModel,
        'controller': StatisticTodayScreenController,
        'components': {'data_base': True, 'cropping': False, 'recognition': False},
    },
    'employees_screen': {
        'model': EmployeesScreenModel,
        'controller': EmployeesScreenController,
        'components': {'data_base': True, 'cropping': False, 'recognition': False},
    },
    'add_employee_screen': {
        'model': AddEmployeeScreenModel,
        'controller': AddEmployeeScreenController,
        'components': {'data_base': True, 'cropping': True, 'recognition': True},
    },
}
