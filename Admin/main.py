from pathlib import Path

from kivy import Config
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.utils import platform
from kivy.core.window import Window
import yaml
import logging

from View.screens import screens
from libs.data_base_handler import DataBaseHandler

realpath = Path(Path.cwd())


class Admin(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_path = Path(realpath, 'config', 'config.yml')
        self.icon_path = Path(realpath, 'assets', 'images', 'icon-w.png')

        Config.set('kivy', 'window_icon', self.icon_path)

        with open(self.config_path) as config_file:
            self.config = yaml.safe_load(config_file)

        if self.config is None:
            print('Файл с конфигурацией не найден')
            exit(1)

        self.config['SERVICE']['platform'] = platform
        self.config['SERVICE']['realpath'] = Path(realpath)

        logging.basicConfig(
            level=logging.DEBUG,
            filename=Path(realpath, 'logs', 'stream.log'),
            encoding='utf-8',
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - '
                   '(%(filename)s).%(funcName)s(%(lineno)d): %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.data_base = DataBaseHandler(self.config)

        self.load_all_kv_files(self.directory)
        self.manager_screens = MDScreenManager()
        
    def build(self) -> MDScreenManager:
        if platform == 'android' or platform == 'ios':
            Window.maximize()
        else:
            Window.size = (1280, 900)
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> None:
        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)


Admin().run()
