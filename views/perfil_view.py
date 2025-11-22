import flet as ft

class PerfilView:
    def __init__(self, page: ft.Page, user_data: dict, theme):
        self.page = page
        self.user_data = user_data
        self.theme = theme
    
    def build(self):
        """Construye y retorna la vista de Mi Perfil"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.PERSON,
                        size=80,
                        color=self.theme.ACCENT_PRIMARY
                    ),
                    ft.Text(
                        "Mi Perfil",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme.TEXT_PRIMARY
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        f"Usuario: {self.user_data['username']}",
                        size=16,
                        color=self.theme.TEXT_PRIMARY
                    ),
                    ft.Text(
                        f"Email: {self.user_data['email']}",
                        size=14,
                        color=self.theme.TEXT_SECONDARY
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            padding=20,
        )
