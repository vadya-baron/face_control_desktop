from pathlib import Path

from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (
    ImageLeftWidget,
    MDList, IRightBodyTouch,
    TwoLineAvatarIconListItem
)
from kivymd.uix.scrollview import MDScrollView

from View.components import BaseScreenData


class RightEmployeeVisitTime(IRightBodyTouch, MDLabel):
    adaptive_width = True


class ScreenData(BaseScreenData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notfound_message = 'Нет сотрудников'
        self.screen_title = 'Рабочий стол'

    def append_data(self, **kwargs):
        box_list = MDList(spacing=5)
        right_container_width = 10
        dd = 0
        for data in self.dataset:
            status = data.get('status', 2)
            dd += 1
            bg_color = '#FFFFFF' if dd % 2 else '#F0F0F0'

            if status == 2:
                bg_color = '#BDBDBD'

            right_come_data = None
            right_came_out_data = None
            right_is_present = None

            if self.show_work_time:
                right_container_width = 400
                right_come_data, right_came_out_data, right_is_present = self.get_show_work_time_data(data)

            list_item = TwoLineAvatarIconListItem(
                ImageLeftWidget(
                    source=str(
                        Path(data.get('photo', Path(Path.cwd(), 'assets', 'images', 'icon.png')))),
                    radius=[20, 20, 20, 20]
                ),
                right_come_data,
                right_came_out_data,
                right_is_present,
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

    @staticmethod
    def get_show_work_time_data(data) -> tuple[
        RightEmployeeVisitTime | None,
        RightEmployeeVisitTime | None,
        RightEmployeeVisitTime | None
    ]:
        time_go_work = data.get('time_go_work', {})
        right_come_data = None
        right_came_out_data = None
        right_is_present = None

        if time_go_work is not None:
            is_present = False
            entered_time = 'Вошел: '
            entered_time += str(time_go_work.get('entered_time', '--:--'))

            came_out_time = 'Вышел: '
            came_out_time += str(time_go_work.get('came_out_time', '--:--'))

            if entered_time != 'Вошел: --:--' and came_out_time == 'Вышел: --:--':
                is_present = True

            right_come_data = RightEmployeeVisitTime(
                text=entered_time,
                size_hint_x=90,
                width=90,
                padding=[10, 10, 10, 10],
                id='right_come_data'
            )

            right_came_out_data = RightEmployeeVisitTime(
                text=came_out_time,
                size_hint_x=90,
                width=90,
                padding=[10, 10, 10, 10],
                id='right_came_out_data'
            )

            if is_present:
                right_is_present = RightEmployeeVisitTime(
                    text='Присутствует',
                    size_hint_x=90,
                    width=90,
                    padding=[10, 10, 10, 10],
                    theme_text_color='Custom',
                    text_color='#00C853',
                    id='right_is_present'
                )
            else:
                right_is_present = RightEmployeeVisitTime(
                    text='Отсутствует',
                    size_hint_x=90,
                    width=90,
                    padding=[10, 10, 10, 10],
                    theme_text_color='Custom',
                    text_color='#B71C1C',
                    id='right_is_present'
                )

        return right_come_data, right_came_out_data, right_is_present
