from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar


class AppToast(Snackbar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.toast = Snackbar(
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
            self.toast.bg_color = '#B71C1C'
        elif action == 'warning':
            self.toast.bg_color = '#FF6F00'
        else:
            self.toast.bg_color = self.theme_cls.primary_color

        self.toast.dismiss()
        self.toast.text = text
        self.toast.open()

    def show_messages(self, messages: list, action: str = 'success'):
        if len(messages) == 0:
            return

        self.toast.dismiss()
        self.toast = Snackbar(
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=.8,
            shadow_color='#f0f0f0',
            elevation=1,
            duration=3,
            auto_dismiss=True,
            bg_color=self.theme_cls.primary_color,
            pos_hint={'center_x': 0.5},
            orientation='vertical',
        )
        if action == 'error':
            self.toast.bg_color = '#B71C1C'
        elif action == 'warning':
            self.toast.bg_color = '#FF6F00'
        else:
            self.toast.bg_color = self.theme_cls.primary_color

        for message in messages:
            self.toast.add_widget(
                MDLabel(text=str(message), text_color='#FFFFFF', theme_text_color='Custom')
            )

        self.toast.open()
