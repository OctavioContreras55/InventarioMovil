from models import add_user, authenticate_user

class LoginController:
    def __init__(self, view):
        self.view = view

    def login(self, username, password):
        user_data = authenticate_user(username, password)
        if user_data:
            # Transición directa sin mensaje (más profesional)
            self.view.go_to_principal(user_data)
        else:
            self.view.show_message("Usuario o contraseña incorrectos.")

class RegisterController:
    def __init__(self, view):
        self.view = view

    def register(self, username, email, password):
        success, message = add_user(username, email, password)
        self.view.show_message(message)
