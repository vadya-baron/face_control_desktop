import logging
import time

import cv2
from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.core.window import Window
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image

from View import BaseScreenView
from View.components import AppToast


class Detect(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = kw.get('model').name_screen
        self.main_container = None
        self.main_container_body = None
        self.main_container_default_text = None
        self.top_app_bar = None
        self.detection_btn = None
        self.detect_interval = None
        self.this_clock = Clock
        self.image = Image()
        self.toast = AppToast()

    def model_is_changed(self, **kwargs) -> None:
        load_employees = kwargs.get('load_employees', None)
        error = kwargs.get('error', False)

        if error is True:
            self.main_container_default_text.text = 'Ошибка приложения. Обратитесь в технический отдел.'

        if load_employees is False:
            self.main_container_default_text.text = 'Запустите приложение Admin и добавьте сотрудников'

        if load_employees is True:
            self.main_container_default_text.text = 'Нажмите кнопку "Начать детекцию"'
            self.detection_btn.disabled = False

    def start_detection(self, *args):
        if self.controller.set_capture() == False:
            self.main_container_default_text.text = 'Ошибка приложения. Обратитесь в технический отдел.'
        else:
            btn = MDRectangleFlatIconButton(
                    id='stop_detection',
                    icon='radiobox-marked',
                    text='Остановить детеуцию',
                    theme_text_color='Custom',
                    text_color='white',
                    theme_icon_color='Custom',
                    icon_color='white',
                    pos_hint={'center_x': .5, 'center_y': .5},
                    on_release=self.stop_detection,
                    md_bg_color='#B71C1C',
                    disabled=False,
                    width='150dp'
                )

            self.main_container_body.clear_widgets()
            self.main_container_body.add_widget(self.image)
            self.top_app_bar.clear_widgets()
            self.top_app_bar.add_widget(btn)
            self.this_clock.schedule_interval(self.detect_video, 1.0 / float(self.detect_interval))

    def stop_detection(self, *args):
        self.this_clock.unschedule(self.detect_video)
        self.controller.stop_detect()
        btn = MDRectangleFlatIconButton(
                id='start_detection',
                icon='radiobox-marked',
                text='Начать детеуцию',
                theme_text_color='Custom',
                text_color='white',
                theme_icon_color='Custom',
                icon_color='white',
                pos_hint={'center_x': .5, 'center_y': .5},
                on_release=self.start_detection,
                md_bg_color='#B71C1C',
                disabled=False,
            )
        self.top_app_bar.clear_widgets()
        self.top_app_bar.add_widget(btn)
        self.main_container_body.clear_widgets()

    def detect_video(self, *args):
        try:
            frame, employee_id, messages = self.controller.detect_video()
            if frame.size == 0 or len(frame.shape) == 0:
                return
        except Exception as e:
            logging.exception(e)
            return

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

        if len(messages) > 0:
            if employee_id > 0:
                self.toast.show_messages(
                    messages=messages,
                    img_src=self.controller.get_employee_photo(employee_id),
                    action='success'
                )
                # self.this_clock.unschedule(self.detect_video)
                # self.this_clock.schedule_once(self.start_detection, 5)
            elif employee_id < 0:
                self.toast.show_messages(messages=messages, action='error')
            elif employee_id == 0:
                self.toast.show_messages(messages=messages, action='warning')

    def build_layout(self):
        self.add_widget(
            MDBoxLayout(
                MDBoxLayout(
                    MDLabel(text='Детектор', id='default_text', halign='center'),
                    id='container_body',
                    pos_hint={'top': 1},
                    specific_text_color='#FAFAFA',
                    orientation='vertical',
                    height=Window.height - 70,
                ),
                MDBottomNavigation(
                    MDRectangleFlatIconButton(
                        id='detection_btn',
                        icon='radiobox-marked',
                        text='Начать детеуцию',
                        theme_text_color='Custom',
                        text_color='white',
                        theme_icon_color='Custom',
                        icon_color='white',
                        pos_hint={'center_x': .5, 'center_y': .5},
                        on_release=self.start_detection,
                        md_bg_color='#B71C1C',
                        disabled=True,
                    ),
                    id='top_app_bar',
                    size_hint_y=None,
                    md_bg_color='#F5F5F5',
                    padding=[0, 0, 0, 50],
                ),
                id='container',
                specific_text_color='#FAFAFA',
                orientation='vertical',
                md_bg_color='#F5F5F5',
            ),
        )

    def on_enter(self):
        self.main_container = self.manager_screens.children[0].children[0]
        self.top_app_bar = self.main_container.ids.top_app_bar
        self.detection_btn = self.top_app_bar.ids.detection_btn
        self.main_container_body = self.main_container.ids.container_body
        self.main_container_default_text = self.main_container.ids.container_body.ids.default_text

        if self.controller.is_db_ready() is False:
            self.main_container_default_text.text = 'Запустите приложение Admin и добавьте сотрудников'
        else:
            self.main_container_default_text.text = 'Идет загрузка сотрудников'
            Clock.schedule_once(self.controller.load_employees)
