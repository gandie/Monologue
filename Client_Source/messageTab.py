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

from message import Message

class MessageTab(TabbedPanelItem):
    logic = ObjectProperty(None)
    layout = ObjectProperty(None)
    root = ObjectProperty(None)

    def __init__(self,**kargs):
        super(MessageTab,self).__init__(**kargs)
        self.logic = App.get_running_app().logic
        self.build_interface()

    def build_interface(self):
        self.mainlayout = FloatLayout()

        self.scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.scroll_layout.bind(minimum_height = self.scroll_layout.setter('height'))


        # Make sure the height is such that there is something to scroll.
        
        self.scroll_view = ScrollView(
            size_hint = (1, 0.9),
            pos_hint = {'x' : 0, 'y' : 0.1}
        )
        self.scroll_view.add_widget(self.scroll_layout)


        self.send_button = Button(
            text = 'Send',
            on_press = self.logic.btn_send_msg,
            size_hint = (0.5, 0.1),
            pos_hint = {'x' : 0, 'y' : 0}
        )

        self.textfield = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'x' : 0.5, 'y' : 0}
        )            
        
        self.mainlayout.add_widget(self.send_button)
        self.mainlayout.add_widget(self.textfield)

        self.mainlayout.add_widget(self.scroll_view)
        self.add_widget(self.mainlayout)

        # testing
        #for i in range(10):
        #    self.add_message('foo {}'.format(i))

    def add_message(self, msg):
        the_message = Message(msg)
        self.scroll_layout.add_widget(the_message)
