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

#class Logic(object):
class Logic(FloatLayout):
    '''
    simple logic module to run chat-client using urlrequests (HTTP POST)
    '''
    
    layout = ObjectProperty(None)

    connected = BooleanProperty(False)
    writing = BooleanProperty(False)

    contacts = ListProperty(None)
    convers_partner = StringProperty(None)
    name = StringProperty(None)
    conversations = DictProperty({})
    messages = ListProperty([])

    ip = StringProperty(None)
    port = StringProperty(None)
    url = StringProperty(None)

    def __init__(self):
        pass

    def register_layout(self, layout):
        self.layout = layout

    def btn_connect_run(self,instance):
        '''connect to server, get initial contacts'''
        self.ip = self.layout.server_tab.ip_input.input_value
        self.port = self.layout.server_tab.port_input.input_value
        self.name = self.layout.server_tab.name_input.input_value

        print self.ip, self.port, self.name

        self.url = 'http://{0}:{1}'.format(self.ip, self.port)
        self.url_fetch_contacts(1)

    def btn_call_up(self, instance):
        '''talk to contact from list'''
        self.convers_partner = instance.text
        self.url_fetch_conversation(1)
        if not self.writing:
            Clock.schedule_interval(self.url_fetch_conversation,1)
            self.writing = True

        self.layout.switch_to(self.layout.message_tab)

    def btn_send_msg(self, instance):
        '''self-explaining...'''
        message = self.layout.message_tab.textfield.text
        self.url_send_msg(message)
        self.layout.message_tab.textfield.text = ''
        #self.layout.text_export.text = ''

    def url_fetch_contacts(self, dt):

        params = json.dumps(
            {
                'name' : self.name,
                'command' : 'update_contacts'
            }
        )
        req = UrlRequest(self.url, on_success = self.connection_success,
                         on_error = self.connection_error, req_body = str(params))

    def url_fetch_conversation(self, dt):
        params = json.dumps(
            {
                'name' : self.name,
                'convers_partner' : self.convers_partner,
                'command' : 'fetch_conversation'
            }
        )
        req = UrlRequest(self.url, on_success = self.connection_success,
                         on_error = self.connection_error, req_body = str(params))

    def url_send_msg(self, message):
        params = json.dumps(
            {
                'name' : self.name,
                'convers_partner' : self.convers_partner,
                'command' : 'send_msg',
                'msg' : message
            }
        )

        req = UrlRequest(self.url, on_success = self.connection_success,
                         on_error = self.connection_error, req_body = str(params))

    def connection_success(self, req, results):
        if not self.connected:
            self.connected = True
            Clock.schedule_interval(self.url_fetch_contacts, 1)
        new_result = json.loads(results)
        command = new_result['command']
        if command == 'update_contacts':
            self.contacts = new_result['contacts']
            self.layout.update_contacts()
        elif command == 'fetch_conversation':
            self.messages = new_result['messages']
            print self.messages
            self.layout.update_msg()

    def connection_error(self, req, results):
        print 'error!'
        if self.connected:
            self.connected = False
            self.layout.contacts_tab.content.clear_widgets()
            Clock.unschedule(self.url_fetch_contacts)
        if self.writing:
            self.writing = False
            self.layout.text_import.text = ''
            Clock.unschedule(self.url_fetch_conversation)

