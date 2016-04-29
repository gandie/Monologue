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

class InputGroup(GridLayout):
    text = StringProperty(None)
    value = StringProperty(None)

    def __init__(self,label,value,**kargs):
        super(InputGroup,self).__init__(**kargs)

        self.show_text = label
        self.input_value = value
        self.rows = 2
        self.build_interface()

    def build_interface(self):
        self.label = Label(text = self.show_text)
        #self.input = TextInput(text = self.input_value)
        self.a_input = TextInput(text = self.input_value)
        self.a_input.bind(text = self.on_text)
        self.add_widget(self.label)
        self.add_widget(self.a_input)

    def on_text(self, instance, value):
        self.input_value = value
        #print 'jow'
        #print value
