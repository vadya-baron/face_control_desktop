from pathlib import Path

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.widget import MDWidget

from View import BaseScreenView


class LoadingScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = kw.get('model').name_screen
        self.model.add_observer(self)

    def model_is_changed(self) -> None:
        pass

    def on_enter(self):
        self.manager_screens.children[0].children[0].ids.screen_manager.children[0].ids.container.clear_widgets()
        self.manager_screens.children[0].children[0].ids.screen_manager.children[0].ids.container.add_widget(
            MDCard(
                MDBoxLayout(
                    FitImage(
                        source=str(Path(Path.cwd(), 'assets', 'images', 'icon.png')),
                        pos_hint={'center_x': .5, 'center_y': .5},
                        height='150dp',
                        size_hint=(.6, '150dp'),
                    ),
                    MDWidget(height=50, size_hint=(1, None), ),
                    MDRectangleFlatIconButton(
                        icon='monitor-dashboard',
                        text='Рабочий стол',
                        pos_hint={'center_x': .5, 'center_y': .5},
                        width='50dp',
                        font_size='20dp',
                        size_hint=(.8, None),
                        on_release=lambda x: self.switch_screen('dashboard_screen')
                    ),
                    MDRectangleFlatIconButton(
                        icon='chart-timeline',
                        text='Статистика за сегодня',
                        pos_hint={'center_x': .5, 'center_y': .5},
                        width='50dp',
                        font_size='20dp',
                        size_hint=(.8, None),
                        on_release=lambda x: self.switch_screen('statistic_today_screen')
                    ),
                    MDRectangleFlatIconButton(
                        icon='account-group',
                        text='Сотрудники',
                        pos_hint={'center_x': .5, 'center_y': .5},
                        width='50dp',
                        font_size='20dp',
                        size_hint=(.8, None),
                        on_release=lambda x: self.switch_screen('employees_screen')
                    ),
                    MDRectangleFlatIconButton(
                        icon='account-multiple-plus-outline',
                        text='Добавить сотрудника',
                        pos_hint={'center_x': .5, 'center_y': .5},
                        width='50dp',
                        font_size='20dp',
                        size_hint=(.8, None),
                        on_release=lambda x: self.switch_screen('add_employee_screen'),
                    ),
                    MDWidget(height=70, size_hint=(1, None),),
                    pos_hint={'center_x': .5, 'center_y': .5},
                    orientation='vertical',
                    spacing='20dp',
                    padding=(0, '50dp', 0, '100dp'),
                ),

                pos_hint={'center_x': .5, 'center_y': .5},
                md_bg_color='#FAFAFA',
                width='400dp',
                size_hint=(None, .7),
            )
        )
