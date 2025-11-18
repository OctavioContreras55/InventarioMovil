import flet as ft
from models.model_colors import DarkTheme

class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Vista Principal"
        self.theme = DarkTheme
        self.page.bgcolor = self.theme.BACKGROUND_PRIMARY
        self.page.add(self.build_home_view())

    def build_home_view(self):
        vista_principal = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Bienvenido", 
                            size=42, 
                            color=self.theme.TEXT_PRIMARY, 
                            weight=ft.FontWeight.BOLD, 
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=ft.padding.only(top=30, bottom=20),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Image(
                            src="assets/logoStockFlow.png",
                            width=200,
                            height=200,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        padding=ft.padding.only(bottom=20),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Seleccione una opción para continuar", 
                            size=18, 
                            color=self.theme.TEXT_SECONDARY, 
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=ft.padding.only(bottom=60),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            icon=ft.Icons.PERSON,
                            text="Iniciar Sesión", 
                            on_click=self.go_to_login, 
                            width=200, 
                            height=60, 
                            color=ft.Colors.WHITE, 
                            bgcolor=self.theme.BUTTON_PRIMARY,
                            style=ft.ButtonStyle(
                                elevation=8,
                                shadow_color=self.theme.SHADOW,
                                shape=ft.RoundedRectangleBorder(radius=15),
                                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                            )
                        ),
                        padding=ft.padding.only(bottom=25),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            icon=ft.Icons.PERSON_ADD,
                            text="Registrarse", 
                            on_click=self.go_to_register, 
                            width=200, 
                            height=60, 
                            color=ft.Colors.WHITE, 
                            bgcolor=self.theme.BUTTON_PRIMARY,
                            style=ft.ButtonStyle(
                                elevation=8,
                                shadow_color=self.theme.SHADOW,
                                shape=ft.RoundedRectangleBorder(radius=15),
                                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                            )
                        ),
                        padding=ft.padding.only(bottom=25),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            icon=ft.Icons.LOGOUT,
                            text="Salir", 
                            on_click=lambda e: self.page.window.close(), 
                            width=200, 
                            height=55, 
                            color=ft.Colors.WHITE, 
                            bgcolor=self.theme.BUTTON_DANGER,
                            style=ft.ButtonStyle(
                                elevation=6,
                                shadow_color=self.theme.SHADOW,
                                shape=ft.RoundedRectangleBorder(radius=15),
                                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                            )
                        ),
                        padding=ft.padding.only(top=30),
                        alignment=ft.alignment.center
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
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
        return vista_principal
        
    def go_to_login(self, e):
        from views import LoginView
        self.page.clean()
        LoginView(self.page)

    def go_to_register(self, e):
        from views import RegisterView
        self.page.clean()
        RegisterView(self.page)
