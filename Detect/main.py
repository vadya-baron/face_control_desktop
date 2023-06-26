from pathlib import Path
from kivy import Config
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.utils import platform
from kivymd.icon_definitions import md_icons
from kivy.core.window import Window
import yaml
import logging
import codecs

from Controllers import DetectScreenController
from Models import DetectScreenModel
from Components import DataBaseHandler, Cropping, Recognition
from View import Load

realpath = Path(Path.cwd())
if platform == 'android' or platform == 'ios':
    Window.maximize()
else:
    Window.size = (1024, 768)


class Detect(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.debug = False
        self.load_all_kv_files(str(Path(realpath, 'View')))
        self.manager_screens = MDScreenManager()
        self.data_base = None
        self.cropping = None
        self.recognition = None

        try:
            if platform == 'win':
                self.config_path = Path(realpath, 'config', 'win-config.yml')
                config_file = codecs.open(str(self.config_path), 'r', 'UTF-8')
                self.app_config = yaml.safe_load(config_file)
                config_file.close()
            else:
                self.config_path = Path(realpath, 'config', 'config.yml')
                with open(self.config_path) as config_file:
                    self.app_config = yaml.safe_load(config_file)
        except Exception as e:
            logging.exception(e)
            exit(1)

        self.icon_path = Path(realpath, 'assets', 'images', 'icon-w.png')

        Config.set('kivy', 'window_icon', self.icon_path)
        Window.bind(on_close=self.on_stop)

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

        self.load_components()

        load_view = Load()
        load_view.manager_screens = self.manager_screens
        self.manager_screens.add_widget(load_view)

        try:
            model = DetectScreenModel(
                config=self.app_config,
                name_screen='detect',
                debug=self.debug,
                data_base=self.data_base,
                cropping=self.cropping,
                recognition=self.recognition
            )

            controller = DetectScreenController(model, self.lang)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.detect_interval = self.app_config['SERVICE']['detect_interval']
            view.name = 'detect'
            self.manager_screens.add_widget(view)
        except Exception as e:
            logging.exception(e)
            exit(1)


        self.manager_screens.current = 'load'

        logging.info('Программа стартовала')
        return self.manager_screens

    def load_components(self, *args):
        try:
            self.data_base = DataBaseHandler(self.app_config['DB_CONFIG'], self.debug)
            self.cropping = Cropping(self.app_config['CROPPING_CONFIG'], self.debug)
            self.recognition = Recognition(self.app_config['RECOGNITION_COMPONENT'], self.debug)
        except Exception as e:
            logging.exception(e)
            exit(1)

    # При приеме видео потока и одновременном изменении размера окна, приложение падает
    # @staticmethod
    # def on_resize():
    #     print('on_resize')
    #     Detect().run()


Detect().run()
