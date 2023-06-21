from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.screen import MDScreen

from Utilits.observer import Observer


class BaseScreenView(ThemableBehavior, MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()
    manager_screens = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

        self.app = MDApp.get_running_app()

        self.build_layout()
        self.model.add_observer(self)
