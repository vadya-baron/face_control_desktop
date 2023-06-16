import os
import cv2

from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.widget import MDWidget

from View import BaseScreenView
from View.components import AppDialog, AppToast


class AddEmployeeScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = kw.get('model').name_screen
        self.dialog = AppDialog()
        self.toast = AppToast()
        self.employee_data = {}
        self.employee_photos = []
        self.main_container = None

        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            selector='multi',
            preview=True,
            ext=['.jpg', '.jpeg'],
        )

        self.model.add_observer(self)

    def add_employee(self):
        self.employee_data['display_name'] = self.main_container.children[0].children[0].ids.display_name.text
        self.employee_data['employee_position'] = self.main_container.children[0].children[0].ids.employee_position.text

        added, messages = self.controller.save_employee(self.employee_data, self.employee_photos)
        if added is False:
            if len(messages) > 0:
                self.toast.show_messages(messages=messages, action='error')
            else:
                self.toast.show('Запись сотрудника не удалась', action='error')
            return

        self.employee_data = {}
        self.employee_photos = []
        self.main_container.children[0].children[0].ids.display_name.text = ''
        self.main_container.children[0].children[0].ids.employee_position.text = ''

        if len(messages) > 0:
            self.toast.show_messages(messages)
        else:
            self.toast.show('Сотрудник добавлен')

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser('~'))
        self.manager_open = True

    def select_path(self, path):
        """Он будет вызван, когда вы нажмете на имя файла или кнопку выбора каталога.

        :type path: str;
        :param path: путь к выбранному каталогу или файлу;
        """

        self.exit_manager()

        if len(path) == 0:
            self.toast.show(text='Не выбрано ни одного фото', action='error')

        for photo in path:
            img = cv2.imread(str(photo))
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.employee_photos.append(img)
            # cv2.imshow('image', img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

        #self.toast.show('Добавлено файлов: ' + str(len(path)))
        self.toast.show_messages(path, 'success')

    def exit_manager(self, *args):
        """Вызывается, когда пользователь достигает корня дерева каталогов."""

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Вызывается при нажатии кнопок на мобильном устройстве."""

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def model_is_changed(self) -> None:
        pass

    def on_enter(self):
        self.employee_data = {'display_name': None, 'employee_position': None, 'external_id': None}
        self.employee_photos = []

        self.main_container = self.manager_screens.children[0].children[0].ids.screen_manager.children[0].ids.container
        self.main_container.clear_widgets()
        self.main_container.add_widget(
            MDBoxLayout(
                MDLabel(
                    font_style='H6',
                    text='Добавить сотрудника',
                    id='screen_title',
                    size_hint_y=.0,
                    radius=[10, 10, 10, 10],
                    padding=[10, 80, 10, 10],
                    font_size='20dp',
                    text_size='20dp',
                    bold=True,
                    markup=True,
                ),
                MDLabel(text='', id='default_text', halign='center'),
                id='main_screen',
                orientation='vertical',
                size_hint_y=None,
                height=Window.height - 100,
                padding=('20dp', '20dp', '20dp', '20dp')
            )
        )

        self.main_container.add_widget(
            MDCard(
                MDBoxLayout(
                    MDTextField(
                        hint_text='ФИО',
                        id='display_name',
                        mode='rectangle',
                        size_hint=(.8, None),
                        pos_hint={'center_x': .5, 'center_y': .5},
                    ),
                    MDTextField(
                        hint_text='Должность',
                        id='employee_position',
                        mode='rectangle',
                        size_hint=(.8, None),
                        pos_hint={'center_x': .5, 'center_y': .5},
                    ),
                    MDWidget(height=2, size_hint=(1, None), ),
                    MDLabel(
                        text='Фото сотрудника (желательно три разных фото одного сотрудника)',
                        halign='left',
                        pos_hint={'center_x': .5, 'center_y': .5},
                        size_hint=(.8, None),
                        height=15
                    ),
                    MDRectangleFlatIconButton(
                        icon='image',
                        id='employee_photos',
                        text='Добавить фотографии',
                        pos_hint={'center_x': .5, 'center_y': .5},
                        width='50dp',
                        font_size='20dp',
                        size_hint=(.8, None),
                        on_release=lambda x: self.file_manager_open()
                    ),
                    MDWidget(height=50, size_hint=(1, None), ),
                    MDRectangleFlatIconButton(
                        icon='content-save',
                        text='Сохранить сотрудника',
                        pos_hint={'center_x': .5, 'center_y': .5},
                        width='50dp',
                        font_size='20dp',
                        size_hint=(.8, None),
                        on_release=lambda x: self.add_employee()
                    ),
                    MDWidget(height=70, size_hint=(1, None), ),
                    pos_hint={'center_x': .5, 'center_y': .5},
                    orientation='vertical',
                    spacing='20dp',
                    padding=(0, '50dp', 0, '100dp'),
                ),

                pos_hint={'center_x': .5, 'center_y': .5},
                md_bg_color='#FAFAFA',
                width='400dp',
                size_hint=(None, .7),
                id='add_employee_card'
            )
        )
