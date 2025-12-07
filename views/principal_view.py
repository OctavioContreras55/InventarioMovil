import flet as ft
from models.model_colors import DarkTheme

# Importar las vistas separadas
from views.dashboard_view import DashboardView
from views.inventario_view import InventarioView
from views.control_puerta_view import ControlPuertaView
from views.almacenes_view import AlmacenesView
from views.reportes_view import ReportesView
from views.sensores_view import SensoresView
from views.ajustes_view import AjustesView
from views.perfil_view import PerfilView

class PrincipalView:
    def __init__(self, page: ft.Page, user_data):
        self.page = page
        self.page.title = "StockFlow"
        self.page.bgcolor = DarkTheme.BACKGROUND_PRIMARY
        self.user_data = user_data
        self.theme = DarkTheme
        self.current_view = "dashboard"
        
        # Instanciar todas las vistas
        self.views = {
            "dashboard": DashboardView(page, user_data, self.theme),
            "inventario": None,
            "control_puerta": ControlPuertaView(page, user_data, self.theme),
            "almacenes": AlmacenesView(page, user_data, self.theme),
            "reportes": ReportesView(page, user_data, self.theme),
            "sensores": SensoresView(page, user_data, self.theme),
            "ajustes": AjustesView(page, user_data, self.theme),
            "perfil": PerfilView(page, user_data, self.theme),
        }
        
        self.drawer = self.build_drawer()
        self.page.drawer = self.drawer
        
        self.menu_button = ft.FloatingActionButton(
            icon=ft.Icons.MENU,
            bgcolor=self.theme.ACCENT_PRIMARY,
            on_click=lambda e: self.page.open(self.drawer),
        )
        
        self.content_area = ft.Container(
            content=self.views["dashboard"].build(),
            expand=True,
            bgcolor=self.theme.BACKGROUND_PRIMARY,
        )
            
        
        self.page.add(
            ft.Stack(
                controls=[
                    self.content_area,
                    ft.Container(
                        content=self.menu_button,
                        top=20,
                        left=20,
                    )
                ],
                expand=True,
            )
        )
        
        self.page.update()
    
    def build_drawer(self):
        view_to_index = {
            "dashboard": 0,
            "inventario": 1,
            "control_puerta": 2,
            "almacenes": 3,
            "reportes": 4,
            "sensores": 5,
            "ajustes": 6,
            "perfil": 7,
        }
        
        selected = view_to_index.get(self.current_view, 0)
        
        return ft.NavigationDrawer(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src="assets/logoStockFlow.png",
                                width=80,
                                height=80,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.Text(
                                f"Hola, {self.user_data['username']}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=self.theme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                self.user_data['email'],
                                size=14,
                                color=self.theme.TEXT_SECONDARY,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    padding=20,
                    bgcolor=self.theme.BACKGROUND_SECONDARY,
                ),
                ft.Divider(height=1, color=self.theme.DIVIDER),
                ft.Container(
                    content=ft.Text(
                        "NAVEGACIÓN",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme.TEXT_SECONDARY,
                    ),
                    padding=ft.padding.only(left=20, top=15, bottom=5),
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="Dashboard",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.INVENTORY_OUTLINED,
                    selected_icon=ft.Icons.INVENTORY,
                    label="Inventario",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.LOCK_OPEN_OUTLINED,
                    selected_icon=ft.Icons.LOCK_OPEN,
                    label="Control de Puerta",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.WAREHOUSE_OUTLINED,
                    selected_icon=ft.Icons.WAREHOUSE,
                    label="Almacenes",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.ANALYTICS_OUTLINED,
                    selected_icon=ft.Icons.ANALYTICS,
                    label="Reportes",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.SENSORS_OUTLINED,
                    selected_icon=ft.Icons.SENSORS,
                    label="Monitoreo ESP32",
                ),
                ft.Divider(height=1, color=self.theme.DIVIDER),
                ft.Container(
                    content=ft.Text(
                        "CONFIGURACIÓN",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme.TEXT_SECONDARY,
                    ),
                    padding=ft.padding.only(left=20, top=10, bottom=5),
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Ajustes",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.PERSON_OUTLINED,
                    selected_icon=ft.Icons.PERSON,
                    label="Mi Perfil",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.LOGOUT,
                    selected_icon=ft.Icons.LOGOUT,
                    label="Cerrar Sesión",
                ),
            ],
            on_change=self.on_drawer_change,
            selected_index=selected,
        )
    
    def on_drawer_change(self, e):
        selected_index = e.control.selected_index
        
        view_map = {
            0: "dashboard",
            1: "inventario",
            2: "control_puerta",
            3: "almacenes",
            4: "reportes",
            5: "sensores",
            6: "ajustes",
            7: "perfil",
            8: "logout",
        }
        
        if selected_index in view_map:
            view_name = view_map[selected_index]
            
            if view_name == "logout":
                self.logout()
            else:
                self.current_view = view_name
                
                if view_name == "inventario":
                    if self.views["inventario"] is None:
                        self.views["inventario"] = InventarioView(self.page, self.user_data, self.theme, self.content_area)
                    self.content_area.content = self.views[view_name].build()
                else:
                    self.content_area.content = self.views[view_name].build()
                
                self.page.close(self.drawer)
                
                self.drawer = self.build_drawer()
                self.page.drawer = self.drawer
                
                self.page.update()
    
    def logout(self):
        from views.home_view import HomeView
        self.page.close(self.drawer)
        self.page.clean()
        HomeView(self.page)
