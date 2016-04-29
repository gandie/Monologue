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

class Message(GridLayout):
    logic = ObjectProperty(None)
    text = StringProperty(None)

    def __init__(self,text,**kargs):
        super(Message,self).__init__(**kargs)
        self.logic = App.get_running_app().logic
        self.text = text
        self.cols = 1
        self.spacing = 10
        self.size_hint_y=None
        self.build_interface()

    def build_interface(self):
        self.label = Label(
            text=self.text,
            halign="left",
            text_size=(Window.width,None),
            padding_x=20
        )
        self.add_widget(self.label)

