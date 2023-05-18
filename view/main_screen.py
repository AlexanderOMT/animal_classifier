#!/usr/bin/python

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget



class MainScreen(BoxLayout):

    controller = None
        
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 20  
        self.padding = 20 
        
        self.title_label = Label(text='Prototype 0.1', font_size=24, size_hint=(1, 0.3), pos_hint={'center_x': 0.5})
        self.add_widget(self.title_label)

        self.user_label = Label(text='', font_size=16, size_hint=(1, 0.3), pos_hint={'center_x': 0.5})
        self.add_widget(self.user_label)

        self.buttons_layout = BoxLayout(orientation='vertical', spacing=10)
        
        self.login_button = Button(text='Login', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        self.login_button.bind(on_press=self.login_user)
        self.buttons_layout.add_widget(self.login_button)

        self.register_button = Button(text='Register', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        self.register_button.bind(on_press=self.register_user)
        self.buttons_layout.add_widget(self.register_button)

        self.upload_button = Button(text='Upload photo', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        self.upload_button.bind(on_press=self.upload_photo)
        self.buttons_layout.add_widget(self.upload_button)

        self.logout_button = Button(text='Logout', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        self.logout_button.bind(on_press=self.logout_user)
        self.buttons_layout.add_widget(self.logout_button)

        self.add_widget(self.buttons_layout)
        self.add_widget(Widget())  

    def update_label_user(self, user_email):
        self.user_label.text = user_email

    def logout_user(self, instance):
        self.controller.handle_logout_button()

    def upload_photo(self, instance):
        app = App.get_running_app()
        app.root.current = 'upload_screen'

    def register_user(self, instance):
        app = App.get_running_app()
        app.root.current = 'registration_screen'

    def login_user(self, instance):
        app = App.get_running_app()
        app.root.current = 'login_screen'

    def set_controller(self, controller):
        self.controller = controller




