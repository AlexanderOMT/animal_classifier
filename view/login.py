#!/usr/bin/python

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.controller = None

        self.orientation = 'vertical'
        
        layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(300), dp(200)))
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        layout.spacing = dp(10)

        self.email_input = TextInput(hint_text='Email', font_size=dp(18), size_hint=(None, None), size=(dp(300), dp(50)))
        layout.add_widget(self.email_input)

        self.password_input = TextInput(hint_text='Password', password=True, font_size=dp(18), size_hint=(None, None), size=(dp(300), dp(50)))
        layout.add_widget(self.password_input)

        login_button = Button(text='Login', size_hint=(None, None), size=(dp(200), dp(50)), font_size=dp(20))
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)

        back_button = Button(text='Go back', size_hint=(None, None), size=(dp(200), dp(50)))
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)
        
        self.add_widget(layout)
    
    def login(self, instance):

        self.clear_widgets()

        email = self.email_input.text
        password = self.password_input.text

        self.controller.handle_button_login(email, password)

        if self.controller.is_user_is_authenticated():
            status = 'Login successful'
            self.controller.handle_label_user()
            
        else: 
            status = 'Login failed'
                
        result_label = Label(text=status)
        self.add_widget(result_label)
        
        back_button = Button(text='Go back', size_hint=(None, None), size=(dp(200), dp(50)))
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

    def set_controller(self, controller):
        self.controller = controller

    def go_back(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_screen'