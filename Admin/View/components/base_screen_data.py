from kivy.core.window import Window
from kivy.properties import (
    StringProperty,
    ListProperty,
    BooleanProperty,
    DictProperty,
    ObjectProperty,
    NumericProperty
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, IRightBodyTouch
from kivymd.uix.scrollview import MDScrollView


class RightEmployeeActions(IRightBodyTouch, MDRaisedButton):
    _action_name = StringProperty()
    _data_id = NumericProperty()
    adaptive_width = True


class RightEmployeeVisitTime(IRightBodyTouch, MDLabel):
    adaptive_width = True


class BaseScreenData(MDBoxLayout):
    screen_title = StringProperty()
    default_text = StringProperty(defaultvalue='')
    notfound_message = StringProperty(defaultvalue='')
    dataset = ListProperty(defaultvalue=None)
    show_work_time = BooleanProperty(defaultvalue=False)
    show_today_statistic = BooleanProperty(defaultvalue=False)
    actions = DictProperty(defaultvalue={})
    object_beginning = ObjectProperty()
    object_end = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.id = 'main_screen'
        self.size_hint_y = None
        self.height = Window.height - 100
        self.padding = ('20dp', '20dp', '20dp', '20dp')

        self.reload()

    def reload(self):
        self.clear_widgets()
        self.add_widget(
            MDLabel(
                font_style='H6',
                text=self.screen_title,
                id='screen_title',
                size_hint_y=.0,
                radius=[10, 10, 10, 10],
                padding=[10, 80, 10, 10],
                font_size='20dp',
                text_size='20dp',
                bold=True,
                markup=True,
            )
        )

        self.add_widget(MDLabel(text=self.default_text, id='default_text', halign='center'))
        if self.notfound_message == '':
            self.notfound_message = 'Нет данных'

        box_list = None
        if self.dataset is not None:
            if len(self.dataset) > 0:
                box_list = self.append_data()
            elif len(self.dataset) == 0:
                box_list = MDLabel(text=self.notfound_message, id='notfound_message', halign='center')

        self.add_widget(MDBoxLayout(
            self._get_service_panel(),
            MDScrollView(
                box_list
            ),
            id='items',
            md_bg_color='#FAFAFA',
            orientation='vertical',
            padding=5,
            size_hint_y=None,
            height=Window.height - 150,
        ))

    def actions_handler(self, right_employee_actions):
        if len(self.actions) == 0:
            return
        action = self.actions.get(right_employee_actions._action_name)
        if action is None:
            return
        action(id=right_employee_actions._data_id)

    def append_data(self, **kwargs):
        return MDList(spacing=5)

    def _get_service_panel(self):
        return MDBoxLayout(orientation='horizontal', padding=[0, 0, 0, 0], height='1dp', adaptive_height=True)
