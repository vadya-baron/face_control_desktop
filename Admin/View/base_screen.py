from pathlib import Path

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import FadeTransition

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import (
    MDNavigationLayout,
    MDNavigationDrawer,
    MDNavigationDrawerMenu,
    MDNavigationDrawerHeader,
    MDNavigationDrawerDivider,
    MDNavigationDrawerLabel
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar

from Utilits.observer import Observer
from View.components import DrawerClickableItem


class BaseScreenView(ThemableBehavior, MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()
    manager_screens = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

        self.app = MDApp.get_running_app()

        self.build_layout()
        self.model.add_observer(self)

    def switch_screen(self, screen):
        self.nav_drawer_close()
        self.app.root.transition = FadeTransition(duration=.3)
        self.app.root.current = screen

    def nav_drawer_open(self, *args):
        nav_drawer = self.children[0].ids.nav_drawer
        nav_drawer.set_state('open')

    def nav_drawer_close(self, *args):
        nav_drawer = self.children[0].ids.nav_drawer
        nav_drawer.set_state('close')

    def build_layout(self):
        icon = Path(Path.cwd(), 'assets', 'images', 'icon.png')

        self.add_widget(MDNavigationLayout(
            MDScreenManager(
                MDScreen(
                    MDTopAppBar(
                        id='top_app_bar',
                        title='Панель управления сотрудниками',
                        elevation=4,
                        pos_hint={'top': 1},
                        md_bg_color='#1976D2',
                        specific_text_color='#FFFFFF',
                        left_action_items=[['menu', lambda x: self.nav_drawer_open()]],
                    ),
                    MDBoxLayout(
                        id='container',
                        #md_bg_color='#FFFFFF',
                        orientation='vertical',
                        size_hint_y=None,
                        height=Window.height - 100
                    ),
                    md_bg_color='#FAFAFA'
                ),
                id='screen_manager'
            ),
            MDNavigationDrawer(
                MDNavigationDrawerMenu(
                    MDNavigationDrawerHeader(
                        text='МЕНЮ',
                        source=str(icon),
                        title_color='#4a4939',
                        spacing='4dp',
                        padding=('12dp', 0, 0, '56dp'),
                    ),
                    DrawerClickableItem(
                        icon='monitor-dashboard',
                        text_right_color='#90CAF9',
                        text='Рабочий стол',
                        radius=(5, 5, 5, 5),
                        size_hint=(.5, None),
                        on_release=lambda x: self.switch_screen('dashboard_screen')
                    ),
                    MDNavigationDrawerDivider(),
                    MDNavigationDrawerLabel(text='Статистика', padding=('10dp', 0, 0, 0)),
                    DrawerClickableItem(
                        icon='chart-arc',
                        text_right_color='#90CAF9',
                        text='Загрузить всю статистику',
                        radius=(5, 5, 5, 5),
                        size_hint=(.5, None),
                        on_release=lambda x: self.switch_screen('statistic_screen')
                    ),
                    DrawerClickableItem(
                        icon='chart-timeline',
                        text_right_color='#90CAF9',
                        text='Статистика за сегодня',
                        radius=(5, 5, 5, 5),
                        size_hint=(.5, None),
                        on_release=lambda x: self.switch_screen('statistic_today_screen')
                    ),
                    MDNavigationDrawerDivider(),
                    MDNavigationDrawerLabel(text='Сотрудники', padding=('10dp', 0, 0, 0)),
                    DrawerClickableItem(
                        icon='account-group',
                        text_right_color='#90CAF9',
                        text='Все сотрудники',
                        radius=(5, 5, 5, 5),
                        size_hint=(.5, None),
                        on_release=lambda x: self.switch_screen('employees_screen')
                    ),
                    DrawerClickableItem(
                        icon='account-multiple-plus-outline',
                        text_right_color='#90CAF9',
                        text='Добавить сотрудника',
                        radius=(5, 5, 5, 5),
                        size_hint=(.5, None),
                        on_release=lambda x: self.switch_screen('add_employee_screen')
                    ),
                    spacing=15,
                ),
                id='nav_drawer',
                radius=(0, 5, 5, 0)
            )
        ))
        # print(self.children)
        # self.main_screen = self.children[0].ids.screen_manager.children[0].ids.main_screen

    @staticmethod
    def get_this_screen_title_label(children=None):
        if children is None:
            children = []
        if len(children) > 0:
            for item in children:
                if item.id == 'screen_title':
                    return item
        return None
