
#!/usr/bin/python

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from view.image_uploader import UploadScreen
from view.register import RegistrationScreen
from view.login import LoginScreen
from view.main_screen import MainScreen

from model.user import User
from model.animal_classifier import AnimalClassifier

class Controller:
    def __init__(self, user, main_page, animal_classifier) -> None:
        self.user = user
        self.main_page = main_page
        self.animal_classifier = animal_classifier

    def handle_button_login(self, email, password):
        self.user.login(email, password)

    def handle_button_register(self, email, password):
        self.user.register(email, password)

    def handle_logout_button(self,):
        self.user.logout_user()
        self.main_page.update_label_user('')

    def handle_label_user(self):
        email = self.user.get_email()
        self.main_page.update_label_user(f'Hi, {email} !')

    def preprocess_input_image(self, path_data):
        return self.animal_classifier.preprocess_input_data(path_data)
    
    def predict_image(self, input_tensor):
        prediction = self.animal_classifier.run_predict(input_tensor) 
        return prediction

    def get_user_email(self):
        return self.user.get_email()

    def is_user_is_authenticated(self):
        return self.user.is_authenticated()
    
class ScreenHandler(App):
    def build(self):

        classifier = AnimalClassifier()
        classifier.load_model('./classifier_model/model_2.h5')

        model = User()
        view = MainScreen()
        controller = Controller(model, view, classifier)
        view.set_controller(controller)

        screen_manager = ScreenManager()
        
        main_screen = Screen(name='main_screen')
        main_screen.add_widget(view)
        screen_manager.add_widget(main_screen)
        
        upload_screen = UploadScreen(name='upload_screen')
        upload_screen.set_controller(controller)
        screen_manager.add_widget(upload_screen)
        
        registration_screen = RegistrationScreen(name='registration_screen')
        registration_screen.set_controller(controller)
        screen_manager.add_widget(registration_screen)

        login_screen = LoginScreen(name='login_screen')
        login_screen.set_controller(controller)
        screen_manager.add_widget(login_screen)

        return screen_manager
    
