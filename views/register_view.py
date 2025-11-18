import flet as ft
from controllers import RegisterController
from models.model_colors import DarkTheme

class RegisterView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Registro de Usuario"
        self.theme = DarkTheme
        self.page.bgcolor = self.theme.BACKGROUND_PRIMARY
        self.controller = RegisterController(self)
        self.tittle = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Registrarse", 
                        size=26, 
                        color=self.theme.TEXT_PRIMARY, 
                        weight=ft.FontWeight.BOLD, 
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(
                        content=ft.Image(
                            src="assets/logoStockFlow.png",
                            width=90,
                            height=90,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        padding=ft.padding.only(top=2, bottom=2),
                        alignment=ft.alignment.center
                    ),
                    ft.Divider(height=1, thickness=1, color=self.theme.DIVIDER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.alignment.center
            ),
            padding=ft.padding.only(top=8, bottom=8),
            alignment=ft.alignment.center
        )
        self.username = ft.Container(
            content=ft.Container(
                content=ft.TextField(
                    prefix_icon=ft.Icons.PERSON, 
                    label="Usuario", 
                    width=320, 
                    height=60, 
                    border_color=self.theme.BORDER_PRIMARY, 
                    focused_border_color=self.theme.ACCENT_PRIMARY,
                    bgcolor=self.theme.BACKGROUND_TERTIARY,
                    color=self.theme.TEXT_PRIMARY,
                    border_radius=12,
                    text_size=16,
                    label_style=ft.TextStyle(color=self.theme.TEXT_SECONDARY),
                    cursor_color=self.theme.ACCENT_PRIMARY
                ),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=self.theme.SHADOW,
                    offset=ft.Offset(0, 2)
                ),
                border_radius=12
            ),
            padding=ft.padding.only(bottom=12)
        )
        self.email = ft.Container(
            content=ft.Container(
                content=ft.TextField(
                    prefix_icon=ft.Icons.EMAIL, 
                    label="Correo Electrónico", 
                    width=320, 
                    height=60, 
                    border_color=self.theme.BORDER_PRIMARY, 
                    focused_border_color=self.theme.ACCENT_PRIMARY,
                    bgcolor=self.theme.BACKGROUND_TERTIARY,
                    color=self.theme.TEXT_PRIMARY,
                    border_radius=12,
                    text_size=16,
                    label_style=ft.TextStyle(color=self.theme.TEXT_SECONDARY),
                    cursor_color=self.theme.ACCENT_PRIMARY
                ),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=self.theme.SHADOW,
                    offset=ft.Offset(0, 2)
                ),
                border_radius=12
            ),
            padding=ft.padding.only(bottom=12)
        )
        self.password = ft.Container(
            content=ft.Container(
                content=ft.TextField(
                    prefix_icon=ft.Icons.LOCK, 
                    label="Contraseña", 
                    password=True, 
                    can_reveal_password=True, 
                    width=320, 
                    height=60, 
                    border_color=self.theme.BORDER_PRIMARY, 
                    focused_border_color=self.theme.ACCENT_PRIMARY,
                    bgcolor=self.theme.BACKGROUND_TERTIARY,
                    color=self.theme.TEXT_PRIMARY,
                    border_radius=12,
                    text_size=16,
                    label_style=ft.TextStyle(color=self.theme.TEXT_SECONDARY),
                    cursor_color=self.theme.ACCENT_PRIMARY
                ),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=self.theme.SHADOW,
                    offset=ft.Offset(0, 2)
                ),
                border_radius=12
            ),
            padding=ft.padding.only(bottom=18)
        )

        self.register_button = ft.ElevatedButton(
            text="Registrar", 
            on_click=self.on_register, 
            width=150, 
            height=50, 
            color=ft.Colors.WHITE, 
            bgcolor=self.theme.BUTTON_PRIMARY,
            style=ft.ButtonStyle(
                elevation=8,
                shadow_color=self.theme.SHADOW,
                shape=ft.RoundedRectangleBorder(radius=12),
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            )
        )
        self.login_button = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "¿Ya tienes una cuenta?", 
                        size=14, 
                        color=self.theme.TEXT_SECONDARY, 
                        weight=ft.FontWeight.W_500, 
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.TextButton(
                        text="Iniciar Sesión", 
                        on_click=self.go_to_login,
                        style=ft.ButtonStyle(
                            color=self.theme.ACCENT_SECONDARY,
                            text_style=ft.TextStyle(
                                size=15, 
                                weight=ft.FontWeight.W_500, 
                                decoration=ft.TextDecoration.UNDERLINE, 
                                decoration_color=self.theme.ACCENT_SECONDARY
                            )
                        )
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                alignment=ft.alignment.center
            ),
            padding=ft.padding.only(top=18),
            alignment=ft.alignment.center
        )
        self.home_button = ft.Container(
            content=ft.ElevatedButton(
                icon=ft.Icons.HOME,
                text="Inicio", 
                on_click=self.go_to_home, 
                width=120, 
                height=45, 
                color=ft.Colors.WHITE, 
                bgcolor=self.theme.BUTTON_SECONDARY,
                style=ft.ButtonStyle(
                    elevation=4,
                    shape=ft.RoundedRectangleBorder(radius=10),
                    text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
                )
            ),
            padding=ft.padding.only(top=15),
            alignment=ft.alignment.center_right
        )

        self.page.add(self.gen_view_register())
        self.page.update()

    def gen_view_register(self):
        register_view = ft.Container(
            content=ft.Column(
                controls=[
                    self.tittle,
                    ft.Container(height=5),
                    self.username,
                    self.email,
                    self.password,
                    ft.Container(height=10),
                    self.register_button,
                    self.login_button,
                    self.home_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            expand=True,
            padding=35,
            bgcolor=self.theme.BACKGROUND_SECONDARY,
            border_radius=15,
            margin=ft.margin.all(10),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=self.theme.SHADOW,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
        )
        return register_view

    def on_register(self, e):

        username = self.username.content.content.value
        email = self.email.content.content.value       
        password = self.password.content.content.value 

        if not username or not email or not password:
            self.show_message("Por favor completa todos los campos")
            return
    
        self.controller.register(username, email, password)
        
        print("Registro solicitado para:", username, email)

    def show_message(self, message):
        if "exito" in message.lower() or "exitosamente" in message.lower():
            import time
            bg_color = self.theme.SUCCESS
            self.username.content.content.value = ""
            self.email.content.content.value = ""
            self.password.content.content.value = ""
            time.sleep(2)
            self.go_to_login(None)
            self.page.update()
        else:
            bg_color = self.theme.ERROR
            
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE, size=16),
            bgcolor=bg_color,
            duration = 3000,
            action="OK",
            action_color=ft.Colors.WHITE
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()
    
    def go_to_login(self, e):
        from views import LoginView
        self.page.clean()
        LoginView(self.page)

    def go_to_home(self, e):
        from views import HomeView
        self.page.clean()
        HomeView(self.page)
