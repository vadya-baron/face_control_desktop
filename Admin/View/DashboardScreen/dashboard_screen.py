from pathlib import Path

from kivymd.uix.navigationdrawer import (
    MDNavigationLayout,
    MDNavigationDrawer,
    MDNavigationDrawerMenu,
    MDNavigationDrawerHeader, MDNavigationDrawerLabel, MDNavigationDrawerDivider
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar

from View.DashboardScreen.components.drawer_item import DrawerClickableItem
from View.base_screen import BaseScreenView


class DashboardScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        icon = Path(Path.cwd(), 'assets', 'images', 'icon.png')

        self.add_widget(MDNavigationLayout(
            MDScreenManager(
                MDScreen(
                    MDTopAppBar(
                        title='Панель управления сотрудниками',
                        elevation=4,
                        pos_hint={'top': 1},
                        md_bg_color='#1976D2',
                        specific_text_color='#FFFFFF',
                        left_action_items=[['menu', lambda x: self.nav_drawer_open()]],
                    )
                )
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
                        size_hint=(.5, None)
                    ),
                    MDNavigationDrawerDivider(),
                    MDNavigationDrawerLabel(text='Статистика', padding=('10dp', 0, 0, 0)),
                    DrawerClickableItem(
                        icon='chart-arc',
                        text_right_color='#90CAF9',
                        text='Загрузить всю статистику',
                        radius=(5, 5, 5, 5),
                        size_hint=(.5, None)
                    ),
                    DrawerClickableItem(
                        icon='chart-timeline',
                        text_right_color='#90CAF9',
                        text='Начало и конец работы',
                        radius=(5, 5, 5, 5),
                        size_hint=(.5, None)
                    ),
                    MDNavigationDrawerDivider(),
                    MDNavigationDrawerLabel(text='Сотрудники', padding=('10dp', 0, 0, 0)),
                    DrawerClickableItem(
                        icon='account-group',
                        text_right_color='#90CAF9',
                        text='Все сотрудники',
                        radius=(5, 5, 5, 5),
                        size_hint=(.5, None)
                    ),
                    DrawerClickableItem(
                        icon='account-multiple-plus-outline',
                        text_right_color='#90CAF9',
                        text='Добавить сотрудника',
                        radius=(5, 5, 5, 5),
                        size_hint=(.5, None)
                    ),
                    spacing=15
                ),
                id='nav_drawer',
                radius=(0, 5, 5, 0)
            )

        ))

    def nav_drawer_open(self, *args):
        nav_drawer = self.children[0].ids.nav_drawer
        nav_drawer.set_state('open')

    def model_is_changed(self) -> None:
        pass
