import flet as ft
from models.model_colors import DarkTheme

class PrincipalView:
    def __init__(self, page: ft.Page, user_data):
        self.page = page
        self.page.title = "Vista Principal"
        self.page.bgcolor = DarkTheme.BACKGROUND_PRIMARY
        self.user_data = user_data
        self.theme = DarkTheme
        
        # Mensaje de bienvenida inicial con animación
        self.welcome_banner = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE,
                        color=self.theme.SUCCESS,
                        size=24
                    ),
                    ft.Text(
                        f"¡Bienvenido, {user_data['username']}!",
                        color=self.theme.TEXT_PRIMARY,
                        size=16,
                        weight=ft.FontWeight.W_500
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            bgcolor=self.theme.BACKGROUND_SECONDARY,
            padding=ft.padding.symmetric(vertical=12, horizontal=20),
            border_radius=8,
            border=ft.border.all(1, self.theme.SUCCESS),
            opacity=0,  # Inicia invisible
            animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_OUT)
        )
        
        self.start_message = ft.Text(
            f"Bienvenido {user_data['username']}", 
            color=self.theme.TEXT_PRIMARY, 
            size=24, 
            weight=ft.FontWeight.BOLD
        )
        self.content_area = ft.Container(
            content=self.start_message,
            alignment=ft.alignment.center,
            expand=True,
            padding=20,
            bgcolor=self.theme.BACKGROUND_PRIMARY,
        )
        self.nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME,
                    selected_icon=ft.Icons.HOME_SHARP,
                    label="Dashboard",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.INVENTORY,
                    selected_icon=ft.Icons.INVENTORY_2_SHARP,
                    label="Inventario",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.ADD,
                    selected_icon=ft.Icons.ADD_SHARP,
                    label="Agregar",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SETTINGS,
                    selected_icon=ft.Icons.SETTINGS_SHARP,
                    label="Configuración",
                )
            ],
            on_change=self.on_nav_change,
            selected_index=0,
            bgcolor=self.theme.BACKGROUND_SECONDARY,
            indicator_color=self.theme.ACCENT_PRIMARY,
        )
        self.page.add(self.build_principal_view())
        self.page.update()
        
        # Animar el banner de bienvenida después de un momento
        import time
        time.sleep(0.3)  # Pequeña pausa
        self.welcome_banner.opacity = 1
        self.page.update()
        
        time.sleep(3)
        self.welcome_banner.opacity = 0
        self.page.update()
    def build_principal_view(self):
        return ft.Column(
            controls=[
                self.welcome_banner,
                self.content_area,
                self.nav_bar,
            ],
            expand=True,
            spacing=0,
        )
    
    def on_nav_change(self, e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            self.content_area.content = self.build_start_view()
        elif selected_index == 1:
            self.content_area.content = self.build_inventory_view()
        elif selected_index == 2:
            self.content_area.content = self.add_item_view()
        elif selected_index == 3:
            self.content_area.content = self.build_settings_view()
        self.page.update()
    
    def build_start_view(self):
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
                                f"Panel de Control",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=self.theme.TEXT_PRIMARY
                            ),
                            ft.Text(
                                f"Hola, {self.user_data['username']}",
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

    def build_inventory_view(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Inventario de Productos",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme.TEXT_PRIMARY
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        controls=[
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("Código", color=self.theme.TEXT_PRIMARY)),
                                    ft.DataColumn(ft.Text("Nombre", color=self.theme.TEXT_PRIMARY)),
                                    ft.DataColumn(ft.Text("Cantidad", color=self.theme.TEXT_PRIMARY)),
                                    ft.DataColumn(ft.Text("Acciones", color=self.theme.TEXT_PRIMARY)),
                                ],
                                rows=[
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("1", color=self.theme.TEXT_SECONDARY)),
                                            ft.DataCell(ft.Text("Item 1", color=self.theme.TEXT_SECONDARY)),
                                            ft.DataCell(ft.Text("10", color=self.theme.TEXT_SECONDARY)),
                                            ft.DataCell(
                                                ft.Row(
                                                    controls=[
                                                        ft.IconButton(
                                                            icon=ft.Icons.EDIT,
                                                            icon_color=self.theme.ACCENT_PRIMARY,
                                                            tooltip="Editar"
                                                        ),
                                                        ft.IconButton(
                                                            icon=ft.Icons.DELETE,
                                                            icon_color=self.theme.ERROR,
                                                            tooltip="Eliminar"
                                                        ),
                                                    ],
                                                    spacing=5
                                                )
                                            ),
                                        ]
                                    ),
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("2", color=self.theme.TEXT_SECONDARY)),
                                            ft.DataCell(ft.Text("Item 2", color=self.theme.TEXT_SECONDARY)),
                                            ft.DataCell(ft.Text("5", color=self.theme.TEXT_SECONDARY)),
                                            ft.DataCell(
                                                ft.Row(
                                                    controls=[
                                                        ft.IconButton(
                                                            icon=ft.Icons.EDIT,
                                                            icon_color=self.theme.ACCENT_PRIMARY,
                                                            tooltip="Editar"
                                                        ),
                                                        ft.IconButton(
                                                            icon=ft.Icons.DELETE,
                                                            icon_color=self.theme.ERROR,
                                                            tooltip="Eliminar"
                                                        ),
                                                    ],
                                                    spacing=5
                                                )
                                            ),
                                        ]
                                    ),
                                ],
                                bgcolor=self.theme.BACKGROUND_SECONDARY,
                                border=ft.border.all(1, self.theme.BORDER_PRIMARY),
                                border_radius=8,
                                heading_row_color=self.theme.BACKGROUND_TERTIARY,
                            ),
                        ],
                        scroll=ft.ScrollMode.ADAPTIVE
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
        )
        
    def add_item_view(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Aquí puedes agregar un nuevo ítem.", color=self.theme.TEXT_PRIMARY, size=24, weight=ft.FontWeight.BOLD),
                ],
            )
        )
        
    def build_settings_view(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Aquí puedes cambiar la configuración.", color=self.theme.TEXT_PRIMARY, size=24, weight=ft.FontWeight.BOLD),
                ],
            )
        )