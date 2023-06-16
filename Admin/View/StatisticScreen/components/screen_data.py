from pathlib import Path

from kivy.properties import BooleanProperty, StringProperty, NumericProperty, DictProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IRightBodyTouch

from Models import BaseDatePicker
from View.components import BaseScreenData


class RightEmployeeVisitTime(IRightBodyTouch, MDLabel):
    adaptive_width = True


class ServiceButton(MDRaisedButton):
    _action_name = StringProperty()
    _data_id = NumericProperty()
    _direction = StringProperty()
    _file_ext = StringProperty()
    adaptive_width = True


class ScreenData(BaseScreenData):
    today = BooleanProperty(defaultvalue=False)
    filter = DictProperty(defaultvalue={})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def append_data(self, **kwargs):
        box_list = MDList(spacing=5)
        right_container_width = 200
        dd = 0
        for data in self.dataset:
            dd += 1
            bg_color = '#FFFFFF' if dd % 2 else '#F0F0F0'

            if self.today:
                right_model_first, right_model_second = self.get_stat_data(data.get('stat', {}), start_end=True)
                photo = ImageLeftWidget(
                    source=str(
                        Path(data.get('photo', Path(Path.cwd(), 'assets', 'images', 'icon.png')))),
                    radius=[20, 20, 20, 20]
                )
            else:
                right_container_width = 300
                right_model_first, right_model_second = self.get_stat_data(data, start_end=False)
                photo = None

            list_item = TwoLineAvatarIconListItem(
                photo,
                right_model_first,
                right_model_second,
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
    def get_stat_data(stat: dict, start_end: bool = False) -> tuple[
        RightEmployeeVisitTime | None,
        RightEmployeeVisitTime | None
    ]:
        if start_end:
            start_date = stat.get('start_date', '--:--')
            end_date = stat.get('end_date', '--:--')

            if start_date != '--:--':
                start_date = start_date[-8:-3]

            if end_date != '--:--':
                end_date = end_date[-8:-3]

            right_model_first = RightEmployeeVisitTime(
                text=start_date,
                size_hint_x=90,
                width=90,
                padding=[10, 10, 10, 10],
                id='right_model_first'
            )

            right_model_second = RightEmployeeVisitTime(
                text=end_date,
                size_hint_x=90,
                width=90,
                padding=[10, 10, 10, 10],
                id='right_model_second'
            )
        else:
            visit_date = stat.get('visit_date', '')
            direction = stat.get('direction', None)

            if visit_date != '':
                visit_date = visit_date[:-3]

            if direction == 1:
                direction = 'Вошел'
            elif direction == 0:
                direction = 'Вышел'
            else:
                direction = 'Нет данных'

            right_model_first = RightEmployeeVisitTime(
                text=visit_date,
                size_hint_x=90,
                width=90,
                padding=[10, 10, 10, 10],
                id='right_model_first'
            )

            right_model_second = RightEmployeeVisitTime(
                text=direction,
                size_hint_x=90,
                width=90,
                padding=[10, 10, 10, 10],
                id='right_model_second'
            )

        return right_model_first, right_model_second

    def _get_service_panel(self, **kwargs):
        if self.today:
            service_panel = [
                ServiceButton(
                    text='Обновить данные',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    _action_name='update_data',
                    on_release=self.update_data_handler
                )
            ]
            if len(self.dataset) > 0:
                service_panel.append(
                    ServiceButton(
                        text='Выгрузить в xlsx',
                        pos_hint={'center_x': 0.5, 'center_y': 0.5},
                        _action_name='upload_file',
                        _file_ext='xlsx',
                        on_release=self.upload_file_handler,
                        md_bg_color='#2c3940',
                        x=10,
                        y=30
                    )
                )
        else:
            filter_page = self.filter.get('page', 0)
            service_panel = [
                ServiceButton(
                    text='С даты',
                    pos_hint={'center_x': .5, 'center_y': .5},
                    on_release=lambda x: self.show_date_picker(dialog_id='date_from'),
                    theme_icon_color='Custom',
                    md_bg_color='#546E7A'
                ),
                ServiceButton(
                    text='По дату',
                    pos_hint={'center_x': .5, 'center_y': .5},
                    on_release=lambda x: self.show_date_picker(dialog_id='date_to'),
                    theme_icon_color='Custom',
                    md_bg_color='#546E7A'
                ),
                ServiceButton(
                    text='Загрузить данные',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    _action_name='upload_data',
                    on_release=self.upload_data_handler,
                    x=10,
                    y=30
                )
            ]

            if filter_page > 0:
                if filter_page > 1:
                    service_panel.append(
                        ServiceButton(
                            text='<',
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            _action_name='upload_data',
                            _direction='-',
                            on_release=self.upload_data_handler,
                            x=10,
                            y=30
                        )
                    )
                if len(self.dataset) > 0:
                    service_panel.append(
                        ServiceButton(
                            text='>',
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            _action_name='upload_data',
                            _direction='+',
                            on_release=self.upload_data_handler,
                            x=10,
                            y=30
                        )
                    )
                    service_panel.append(
                        ServiceButton(
                            text='Выгрузить в xlsx',
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            _action_name='upload_file',
                            _file_ext='xlsx',
                            on_release=self.upload_file_handler,
                            md_bg_color='#2c3940',
                            x=10,
                            y=30
                        )
                    )

        return MDBoxLayout(
            *service_panel,
            id='service_container',
            orientation='horizontal',
            padding=[5, 20, 20, 20],
            height='50dp',
            adaptive_height=True,
            spacing=10,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

    def update_data_handler(self, instance):
        action = self.actions.get(instance._action_name)
        if action is None:
            return

        action()

    def upload_data_handler(self, instance):
        action = self.actions.get(instance._action_name)
        direction = instance._direction

        if action is None:
            return

        if direction != '':
            if direction == '+':
                self.filter['page'] += 1
            if direction == '-' and self.filter['page'] > 1:
                self.filter['page'] -= 1
        else:
            self.filter['page'] = 1

        action(filter=self.filter)

    def upload_file_handler(self, instance):
        action = self.actions.get(instance._action_name)
        file_ext = instance._file_ext
        if action is None:
            return

        action(filter=self.filter, file_ext=file_ext)

    def date_picker_on_save(self, instance, value, date_range):
        if instance.id == 'date_from':
            self.filter['date_from'] = '{date:%Y-%m-%d}'.format(date=value)

        if instance.id == 'date_to':
            self.filter['date_to'] = '{date:%Y-%m-%d}'.format(date=value)

    def date_picker_on_cancel(self, instance, value):
        if instance.id == 'date_from':
            self.filter['date_from'] = ''

        if instance.id == 'date_to':
            self.filter['date_to'] = ''

    def show_date_picker(self, dialog_id: str, *args):
        date_dialog = BaseDatePicker()
        date_dialog.id = dialog_id
        date_dialog.bind(on_save=self.date_picker_on_save, on_cancel=self.date_picker_on_cancel)
        date_dialog.open()
