import flet as ft

class AjustesView:
    def __init__(self, page: ft.Page, user_data: dict, theme):
        self.page = page
        self.user_data = user_data
        self.theme = theme
    
    def build(self):
        """Construye y retorna la vista de Configuración"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Configuración",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme.TEXT_PRIMARY
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "🚧 Vista en construcción",
                        size=16,
                        color=self.theme.TEXT_SECONDARY
                    ),
                ],
            ),
            padding=20,
        )
