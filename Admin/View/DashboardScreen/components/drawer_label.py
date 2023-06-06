from kivymd.uix.navigationdrawer import MDNavigationDrawerItem


class DrawerLabelItem(MDNavigationDrawerItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_color = '#1B1B1B'
        self.icon_color = '#1B1B1B'
        self.focus_behavior = False
        self.selected_color = '#1B1B1B'
        _no_ripple_effect = True
