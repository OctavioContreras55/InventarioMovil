import flet as ft

class DashboardView:
    def __init__(self, page: ft.Page, user_data: dict, theme):
        self.page = page
        self.user_data = user_data
        self.theme = theme
    
    def build(self):
        """Construye y retorna la vista del Dashboard"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(
                                ft.Icons.DASHBOARD,
                                size=60,
                                color=self.theme.ACCENT_PRIMARY
                            ),
                            ft.Text(
                                "Dashboard",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=self.theme.TEXT_PRIMARY
                            ),
                            ft.Text(
                                f"Bienvenido, {self.user_data['username']}",
                                size=16,
                                color=self.theme.TEXT_SECONDARY
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                        ),
                        padding=30,
                        bgcolor=self.theme.BACKGROUND_SECONDARY,
                        border_radius=12,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=8,
                            color=self.theme.SHADOW,
                            offset=ft.Offset(0, 2)
                        ),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
        )
