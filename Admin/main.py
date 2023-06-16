from pathlib import Path
from kivy import Config
from kivy.uix.screenmanager import FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.utils import platform
from kivy.core.window import Window
from kivy.clock import Clock
import yaml
import logging

from View import Preloader
from View.screens import screens
from Components import DataBaseHandler, Cropping, Recognition

realpath = Path(Path.cwd())
if platform == 'android' or platform == 'ios':
    Window.maximize()
else:
    Window.size = (1280, 900)


class Admin(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.debug = False
        self.load_all_kv_files(str(Path(realpath, 'View')))
        self.manager_screens = MDScreenManager()
        preloader = Preloader()

        self.manager_screens.add_widget(preloader)
        self.manager_screens.current = 'Preloader'

        self.data_base = None
        self.cropping = None
        self.recognition = None

        self.config_path = Path(realpath, 'config', 'config.yml')
        self.icon_path = Path(realpath, 'assets', 'images', 'icon-w.png')

        Config.set('kivy', 'window_icon', self.icon_path)
        Window.bind(on_close=self.on_stop)

        with open(self.config_path) as config_file:
            self.app_config = yaml.safe_load(config_file)

        if self.app_config is None:
            print('Файл с конфигурацией не найден')
            exit(1)

        self.debug = bool(self.app_config['SERVICE']['debug'])
        self.lang = self.app_config['LANGUAGE']

    def build(self) -> MDScreenManager:
        self.title = self.app_config['SERVICE']['name']

        self.app_config['SERVICE']['platform'] = platform
        self.app_config['SERVICE']['realpath'] = str(Path(realpath))

        logging.basicConfig(
            level=logging.INFO,
            filename=str(Path(realpath, self.app_config['SERVICE']['logs_path'], 'stream.log')),
            encoding='utf-8',
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - '
                   '(%(filename)s).%(funcName)s(%(lineno)d): %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        logging.info('Программа стартовала')
        return self.manager_screens

    def on_start(self):
        Clock.schedule_once(self.load_component, 1)

    def on_stop(self):
        self.data_base.backup_db()

    def load_component(self, *args):
        try:
            self.data_base = DataBaseHandler(self.app_config['DB_CONFIG'], self.debug)
            self.cropping = Cropping(self.app_config['CROPPING_CONFIG'], self.debug)
            self.recognition = Recognition(self.app_config['RECOGNITION_COMPONENT'], self.debug)
        except Exception as e:
            logging.exception(e)
            exit(1)

        self.generate_application_screens()
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, *args):
        self.manager_screens.transition = FadeTransition(duration=.5)
        self.manager_screens.current = 'loading_screen'

    def generate_application_screens(self) -> None:
        for i, name_screen in enumerate(screens.keys()):
            try:
                model = screens[name_screen]['model'](
                    config=self.app_config,
                    name_screen=name_screen,
                    debug=self.debug,
                    data_base=self.data_base if screens[name_screen]['components']['data_base'] else None,
                    cropping=self.cropping if screens[name_screen]['components']['cropping'] else None,
                    recognition=self.recognition if screens[name_screen]['components']['recognition'] else None
                )

                controller = screens[name_screen]['controller'](model, self.lang)
                view = controller.get_view()
                view.manager_screens = self.manager_screens
                view.name = name_screen
                self.manager_screens.add_widget(view)
            except Exception as e:
                logging.exception(e)
                exit(1)


Admin().run()
