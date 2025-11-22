import flet as ft

class SensoresView:
    def __init__(self, page: ft.Page, user_data: dict, theme):
        self.page = page
        self.user_data = user_data
        self.theme = theme
    
    def build(self):
        """Construye y retorna la vista de Monitoreo ESP32"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.SENSORS,
                        size=80,
                        color=self.theme.ACCENT_PRIMARY
                    ),
                    ft.Text(
                        "Monitoreo ESP32",
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
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            padding=20,
        )
