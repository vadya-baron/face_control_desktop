from kivy.clock import Clock
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.screen import MDScreen


class Load(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'load'

    def on_enter(self):
        Clock.schedule_once(self.load_detect, 0)

    def load_detect(self, *args):
        self.parent.transition = FadeTransition(duration=.3)
        self.parent.current = 'detect'
