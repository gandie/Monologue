from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import *
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class ContactTab(TabbedPanelItem):
    logic = ObjectProperty(None)

    def __init__(self,**kargs):
        super(ContactTab,self).__init__(**kargs)
        self.logic = App.get_running_app().logic
        self.build_interface()

    def build_interface(self):
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.clear_widgets()
        self.layout.bind(minimum_height=self.layout.setter('height'))
        for contact in self.logic.contacts:
            # dont add yourself to contact-list!
            if str(contact) == self.logic.name:
                continue
            btn = Button(text = contact, size_hint_y=None, height=40,
                                    on_press = self.logic.btn_call_up)
            self.layout.add_widget(btn)
        self.content = ScrollView()
        self.content.add_widget(self.layout)

    def contact_tab_update(self):
        self.build_interface()
