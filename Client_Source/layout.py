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
from kivy.network.urlrequest import UrlRequest
import json

''' Frontend Modules '''
from serverTab import ServerTab
from messageTab import MessageTab
from contactTab import ContactTab

from logic import Logic

class MasterLayout(TabbedPanel):

    # GUI

    # TABS
    server_tab = ObjectProperty(None)
    message_tab = ObjectProperty(None)
    contacts_tab = ObjectProperty(None)

    # BUTTONS
    btn_connect = ObjectProperty(None)
    btn_send = ObjectProperty(None)

    # TEXT IN / OUTPUT
    text_import = ObjectProperty(None)
    text_export = ObjectProperty(None)

    # CONNECTION IN / OUTPUT
    name_input = ObjectProperty(None)
    ip_input = ObjectProperty(None)
    port_input = ObjectProperty(None)



    '''
    connected = BooleanProperty(False)
    writing = BooleanProperty(False)

    contacts = ListProperty(None)
    convers_partner = StringProperty(None)
    name = StringProperty(None)
    conversations = DictProperty({})

    messages = ListProperty([])
    '''

    logic = ObjectProperty(None)

    def __init__(self, **kwargs):
       super(MasterLayout, self).__init__(**kwargs)
       self.logic = App.get_running_app().logic
       self.build_interface()

    def update_contacts(self):
        '''this guy is called after contacts are fetched from server'''
        '''
        self.contacts_tab.content.clear_widgets()
        for contact in self.logic.contacts:
            # dont add yourself to contact-list!
            if str(contact) == self.logic.name:
                continue
            contact_button = Button(text = contact, 
                                    on_press = self.logic.btn_call_up)
            self.contacts_tab.content.add_widget(contact_button)
        '''
        self.contacts_tab.contact_tab_update()

    def update_msg(self):
        '''this guy is called after messages are fetched from server'''
        #self.text_import.text = ''
        # CLEAR MESSAGES!!!

        self.message_tab.scroll_layout.clear_widgets()

        for message in self.logic.messages:
            msg = message[0] + ': ' + message[1]
            self.message_tab.add_message(msg)



    def build_interface(self):
        '''create application layout and stuff'''

        # SERVER TAB
        self.server_tab = ServerTab(text='Server')
        self.add_widget(self.server_tab)
        # CONTACTS TAB
        self.contacts_tab = ContactTab(text='Contact')
        self.add_widget(self.contacts_tab)
        # MSG TAB
        self.message_tab = MessageTab(text='Message')
        self.add_widget(self.message_tab)
    
