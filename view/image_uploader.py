#!/usr/bin/python

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label

class UploadScreen(Screen):

    controller = None

    def on_enter(self, *args):

        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.file_chooser = FileChooserListView(path=".")
        layout.add_widget(self.file_chooser)
        
        self.upload_button = Button(text="Upload", size_hint=(1, None), height=50)
        self.upload_button.bind(on_release=self.image_predict)
        layout.add_widget(self.upload_button)
        
        self.image = Image(allow_stretch=True)
        layout.add_widget(self.image)

        self.prediction_label = Label(text=".", size_hint=(1, None), height=50)
        layout.add_widget(self.prediction_label)    

        back_button = Button(text='Go back', size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)

    def image_predict(self, instance):

        selected_path = self.file_chooser.selection and self.file_chooser.selection[0]

        if selected_path:
            
            self.image.source = selected_path
            try:
                input_tensor = self.controller.preprocess_input_image(selected_path) 
                prediction_result = self.controller.predict_image(input_tensor) 
            except Exception as e:
                prediction_result = f'Error'
                
            self.prediction_label.text = f"Prediction: {prediction_result}"
    
    def set_controller(self, controller):
        self.controller = controller

    def go_back(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_screen'
