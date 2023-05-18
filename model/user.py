import json
import pyrebase

class User:

    def __init__(self, email=None) -> None:
        self.email = email
        self._uid = None
    
    def register(self, email, password):

        auth = self._connect_database()    
        try:
            user = auth.create_user_with_email_and_password(email, password)
            self.email = user['email']
            self._uid = user['localId']
        except Exception as e:
            print(e)

    def login(self, email, password):

        auth = self._connect_database()
        try:            
            user = auth.sign_in_with_email_and_password(email, password)
            self.email = user['email']
            self._uid = user['localId']

        except Exception as e:
            print(e)

    def logout_user(self):
        auth = self._connect_database()
        try:
            auth.current_user = None 
            self.email = self._uid = None 
        except Exception as e:
            print(e)

    def get_email(self):
        return self.email

    def is_authenticated(self):
        
        try:
            if self._uid:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def _connect_database(self):

        with open("./database_config/config.json", "r") as file:
            config = json.load(file)

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()  

        return auth           