from kivymd.uix.navigationdrawer import MDNavigationDrawerItem


class DrawerClickableItem(MDNavigationDrawerItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus_color = '#E3F2FD'
        self.text_color = '#4a4939'
        self.icon_color = '#4a4939'
        self.ripple_color = '#E3F2FD'
        self.selected_color = '#1B1B1B'
