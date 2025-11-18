import flet as ft
from controllers import LoginController
from models.model_colors import DarkTheme

class LoginView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Inicio de Sesión"
        self.theme = DarkTheme
        self.page.bgcolor = self.theme.BACKGROUND_PRIMARY
        self.controller = LoginController(self)

        self.title = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Iniciar Sesión", 
                        size=32, 
                        color=self.theme.TEXT_PRIMARY, 
                        weight=ft.FontWeight.BOLD, 
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(
                        content=ft.Image(
                            src="assets/logoStockFlow.png",
                            width=120,
                            height=120,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        padding=ft.padding.only(top=5, bottom=5),
                        alignment=ft.alignment.center
                    ),
                    ft.Divider(height=1, thickness=1, color=self.theme.DIVIDER),
                    
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=20, bottom=20),
            alignment=ft.alignment.center,
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
            padding=ft.padding.only(bottom=25)
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
            padding=ft.padding.only(bottom=30)
        )

        self.login_button = ft.Container(
            content=ft.ElevatedButton(
                text="Iniciar Sesión", 
                on_click=self.on_login, 
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
            ),
            alignment=ft.alignment.center
        )
        
        self.register_button = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "¿No tienes cuenta?", 
                        size=15, 
                        color=self.theme.TEXT_SECONDARY, 
                        weight=ft.FontWeight.W_500, 
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.TextButton(
                        text="Registrate", 
                        on_click=self.go_to_register, 
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
                alignment=ft.alignment.center,
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.only(top=15),
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
            padding=ft.padding.only(top=20),
            alignment=ft.alignment.center_right
        )

        self.controller = LoginController(self)
        self.page.add(self.gen_login_view())
        self.page.update()

    def gen_login_view(self):
            login_view = ft.Container(
                content=ft.Column(
                    controls=[
                        self.title,
                        ft.Container(height=10),
                        self.username,
                        self.password,
                        ft.Container(height=15),
                        self.login_button,
                        self.register_button,
                        self.home_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                    
                ),
                alignment=ft.alignment.center,
                expand=True,
                padding=40,
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
            return login_view

    def on_login(self, e):

        self.login_button.visible = False
        self.page.update()      
        self.controller.login(self.username.content.content.value, self.password.content.content.value)

    def show_message(self, message):
        if "incorrectas" in message.lower() or "incorrecto" in message.lower() or "error" in message.lower():
            bg_color = self.theme.ERROR
            self.username.content.content.value = ""
            self.password.content.content.value = ""
            
            self.login_button.visible = True
            
            snack_bar = ft.SnackBar(
                content=ft.Text(message, color=ft.Colors.WHITE, size=16),
                bgcolor=bg_color,
                duration=3000,
                action="OK",
                action_color=ft.Colors.WHITE
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.page.update()

    def go_to_register(self, e):
        from views import RegisterView
        self.page.clean()
        RegisterView(self.page)

    def go_to_home(self, e):
        from views import HomeView
        self.page.clean()
        HomeView(self.page)
        
    def go_to_principal(self, user_data):
        from views import PrincipalView
        self.page.clean()
        PrincipalView(self.page, user_data)