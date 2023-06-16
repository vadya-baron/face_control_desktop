from kivymd.uix.screen import MDScreen


class Preloader(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'Preloader'
