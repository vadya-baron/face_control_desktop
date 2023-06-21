from kivy.clock import Clock
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar


class AppToast(Snackbar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._toast = Snackbar(
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=.8,
            shadow_color='#f0f0f0',
            elevation=1,
            duration=3,
            auto_dismiss=True,
            bg_color=self.theme_cls.primary_color,
        )

    def show(self, text: str, action: str = 'success'):
        if action == 'error':
            self._toast.bg_color = '#B71C1C'
        elif action == 'warning':
            self._toast.bg_color = '#FF6F00'
        else:
            self._toast.bg_color = self.theme_cls.primary_color

        self._toast.dismiss()
        self._toast.text = text
        self._toast.open()

    def show_messages(self, messages: list, img_src: str = '', action: str = 'success'):
        if len(messages) == 0:
            return

        self._toast.dismiss()
        self._toast = Snackbar(
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=.8,
            shadow_color='#f0f0f0',
            elevation=1,
            duration=10,
            auto_dismiss=True,
            bg_color=self.theme_cls.primary_color,
            pos_hint={'center_x': 0.5},
            orientation='vertical',
        )
        if action == 'error':
            self._toast.bg_color = '#B71C1C'
        elif action == 'warning':
            self._toast.bg_color = '#FF6F00'
        else:
            self._toast.bg_color = self.theme_cls.primary_color

        if img_src is not None and img_src != '':
            self._toast.size_hint_y = .4
            self._toast.size_hint_x = .5

            self._toast.add_widget(
                FitImage(source=img_src, size_hint_y='120dp', size_hint_x=.5)
            )

        if len(messages) > 1:
            self._toast.padding = [10, 10, 10, 50]
            self._toast.spacing = '25dp'

        for message in messages:
            self._toast.add_widget(
                MDLabel(text=str(message), text_color='#FFFFFF', theme_text_color='Custom')
            )

        self._toast.open()
