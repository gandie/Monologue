from kivy.app import App
from kivy.properties import *
from layout import MasterLayout
from kivy.core.window import Window

from logic import Logic

class MonologueApp(App):

    logic = ObjectProperty(None)
    tabs = ObjectProperty(None)


    def build(self):

        self.logic = Logic()
        self.tabs = MasterLayout(do_default_tab = False, tab_width=Window.width/3)
        self.logic.register_layout(self.tabs)

        return self.tabs

if __name__ == '__main__':
    MonologueApp().run()
