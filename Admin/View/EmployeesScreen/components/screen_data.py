from pathlib import Path

from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import (
    ImageLeftWidget,
    MDList, IRightBodyTouch,
    TwoLineAvatarIconListItem
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.widget import MDWidget

from View.components import BaseScreenData


class RightEmployeeActions(IRightBodyTouch, MDRaisedButton):
    _action_name = StringProperty()
    _data_id = NumericProperty()
    adaptive_width = True


class ScreenData(BaseScreenData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def append_data(self, **kwargs):
        box_list = MDList(spacing=5)
        right_container_width = 10
        dd = 0
        for data in self.dataset:
            status = data.get('status', 0)
            dd += 1
            bg_color = '#FFFFFF' if dd % 2 else '#F0F0F0'
            action_block = None

            if status == 2:
                bg_color = '#BDBDBD'

            if len(self.actions) > 0:
                right_container_width = 250
                action_block = self.get_show_actions_data(status, data.get('id'))

            list_item = TwoLineAvatarIconListItem(
                ImageLeftWidget(
                    source=str(
                        Path(data.get('photo', Path(Path.cwd(), 'assets', 'images', 'icon.png')))),
                    radius=[20, 20, 20, 20]
                ),
                MDBoxLayout(
                    MDWidget(),
                    action_block,
                    RightEmployeeActions(
                        text='Удалить',
                        _data_id=data.get('id'),
                        _action_name='remove_employee',
                        pos_hint={'center_x': .5, 'center_y': .5},
                        on_release=self.actions_handler,
                        md_bg_color='#B71C1C',
                    ),
                    id='item_service_container',
                    orientation='horizontal',
                    height='50dp',
                    width='250dp',
                    adaptive_height=True,
                    spacing=10,
                    pos_hint={'center_x': .5, 'center_y': 0.5},
                ),
                text=str(data.get('display_name', '')),
                secondary_text=str(data.get('employee_position', '')),
                bg_color=bg_color,
                _txt_bot_pad=15,
                radius=[10, 10, 10, 10],
                divider=None,
                size_hint_y=None,
            )

            list_item.ids._right_container.width = right_container_width

            box_list.add_widget(
                list_item
            )

        return box_list

    def get_show_actions_data(self, status: int, data_id: int) -> RightEmployeeActions | None:
        if status == 1:
            action_block = RightEmployeeActions(
                text='Блокировать',
                _data_id=data_id,
                _action_name='employee_block',
                pos_hint={'center_x': .5, 'center_y': .5},
                on_release=self.actions_handler
            )
        elif status == 2:
            action_block = RightEmployeeActions(
                text='Восстановить',
                _data_id=data_id,
                _action_name='employee_unblock',
                pos_hint={'center_x': .5, 'center_y': .5},
                on_release=self.actions_handler
            )
        else:
            action_block = None

        return action_block
