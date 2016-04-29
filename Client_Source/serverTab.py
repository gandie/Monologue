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
from kivy.core.window import Window

from inputGroup import InputGroup

class ServerTab(TabbedPanelItem):
    logic = ObjectProperty(None)
    inputHeight = "0.2"

    def __init__(self,**kargs):
        super(ServerTab,self).__init__(**kargs)
        self.logic = App.get_running_app().logic
        self.build_interface()

    def build_interface(self):
        self.layout = FloatLayout()
        self.ip_input = InputGroup(
            "IP-Adresse",
            "127.0.0.1",
            size_hint=(0.7,self.inputHeight),
            pos_hint={'x': 0.025 , 'y':0.7}
        )
        self.port_input = InputGroup(
            "Port", 
            "14242",
            size_hint=(0.225,self.inputHeight),
            pos_hint={'x': 0.75 , 'y':0.7}
        )
        self.name_input = InputGroup(
            "Name",
            "name",
            size_hint=(0.95,self.inputHeight),
            pos_hint={'x': 0.025 , 'y':0.45}
        )
        self.btn_connect = Button(
            text="connect",
            on_press=self.logic.btn_connect_run,
            size_hint=(1,self.inputHeight),
            pos_hint={'x': 0 , 'y':0},
            background_color=[0.25,0.88,0.13,1]
        )

        self.layout.add_widget(self.ip_input)
        self.layout.add_widget(self.port_input)
    
        self.layout.add_widget(self.btn_connect)
        self.layout.add_widget(self.name_input)
        self.add_widget(self.layout)

