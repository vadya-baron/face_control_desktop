from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog


class AppDialog(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog()

    def show(self, title: str = '', text: str = '', auto_dismiss: bool = True, dialog_buttons: list = None):
        self.dialog.auto_dismiss = auto_dismiss
        if title is None or title == '':
            return

        self.dialog.title = title

        if text != '':
            self.dialog.text = text

        box = None
        if dialog_buttons is not None and len(dialog_buttons) > 0:
            self.dialog.type = 'custom'

            box = MDBoxLayout(
                pos_hint={'center_x': 0.5, 'center_y': 100},
                padding=[400, 0, 0, 0],
                orientation='horizontal',
            )
            for button in dialog_buttons:
                box.add_widget(
                    MDRaisedButton(
                        text=str(button.get('text')),
                        theme_text_color="Custom",
                        text_color=str(button.get('text_color', '#FFFFFF')),
                        line_color=str(button.get('line_color', '#1976D2')),
                        on_release=button.get('on_release', self.dialog.dismiss),
                    )
                )

        if box is not None:
            self.dialog.add_widget(box)

        #self.dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        self.dialog.shadow_color = '#f0f0f0'
        self.dialog.elevation = 1
        #self.dialog.padding = [0, 0, 0, 0]
        #self.dialog.height = '300dp'
        #self.dialog.size_hint = [.8, .4]
        self.dialog.open()

    def close(self):
        self.dialog.dismiss()
