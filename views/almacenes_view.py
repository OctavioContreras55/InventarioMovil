import flet as ft
import flet_map as map

class AlmacenesView:
    def __init__(self, page: ft.Page, user_data: dict, theme):
        self.page = page
        self.user_data = user_data
        self.theme = theme
        self.marker_layer_ref = ft.Ref[map.MarkerLayer]()
        
        # Coordenadas de tres almacenes ficticios en México
        self.almacenes = [
            {
                "nombre": "Almacén Central",
                "direccion": "Av. Revolución 1500, CDMX",
                "coordenadas": map.MapLatitudeLongitude(19.4326, -99.1332),  # Ciudad de México
                "telefono": "+52 55 1234 5678",
                "icon_color": ft.Colors.RED_700,
            },
            {
                "nombre": "Almacén Norte",
                "direccion": "Blvd. Díaz Ordaz 500, Monterrey",
                "coordenadas": map.MapLatitudeLongitude(25.6866, -100.3161),  # Monterrey
                "telefono": "+52 81 9876 5432",
                "icon_color": ft.Colors.BLUE_700,
            },
            {
                "nombre": "Almacén Occidente",
                "direccion": "Av. Vallarta 2000, Guadalajara",
                "coordenadas": map.MapLatitudeLongitude(20.6597, -103.3496),  # Guadalajara
                "telefono": "+52 33 5555 1234",
                "icon_color": ft.Colors.GREEN_700,
            },
        ]
    
    def mostrar_info_almacen(self, almacen):
        """Muestra un diálogo con la información del almacén"""
        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.WAREHOUSE, color=almacen["icon_color"]),
                ft.Text(almacen["nombre"], weight=ft.FontWeight.BOLD),
            ]),
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, size=20, color=self.theme.TEXT_SECONDARY),
                        ft.Text(almacen["direccion"], size=14),
                    ], spacing=10),
                    ft.Divider(),
                    ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=20, color=self.theme.TEXT_SECONDARY),
                        ft.Text(almacen["telefono"], size=14),
                    ], spacing=10),
                    ft.Divider(),
                    ft.Row([
                        ft.Icon(ft.Icons.MAP, size=20, color=self.theme.TEXT_SECONDARY),
                        ft.Text(
                            f"Lat: {almacen['coordenadas'].latitude:.4f}, Lon: {almacen['coordenadas'].longitude:.4f}",
                            size=12,
                            color=self.theme.TEXT_SECONDARY,
                        ),
                    ], spacing=10),
                ], spacing=15),
                padding=20,
            ),
            actions=[
                ft.TextButton(
                    "Ver en Google Maps",
                    icon=ft.Icons.MAP,
                    on_click=lambda e: self.abrir_google_maps(almacen)
                ),
                ft.TextButton("Cerrar", on_click=lambda e: self.cerrar_dialog(dialog)),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def abrir_google_maps(self, almacen):
        """Abre Google Maps con las coordenadas del almacén"""
        lat = almacen["coordenadas"].latitude
        lon = almacen["coordenadas"].longitude
        url = f"https://www.google.com/maps?q={lat},{lon}"
        self.page.launch_url(url)
    
    def cerrar_dialog(self, dialog):
        """Cierra el diálogo"""
        dialog.open = False
        self.page.update()
    
    def crear_marcador(self, almacen):
        """Crea un marcador personalizado para un almacén"""
        return map.Marker(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(
                        ft.Icons.WAREHOUSE,
                        size=40,
                        color=almacen["icon_color"],
                    ),
                    ft.Container(
                        content=ft.Text(
                            almacen["nombre"].split()[0],  # Solo primera palabra
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        bgcolor=almacen["icon_color"],
                        padding=ft.padding.symmetric(horizontal=5, vertical=2),
                        border_radius=5,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                on_click=lambda e, alm=almacen: self.mostrar_info_almacen(alm),
            ),
            coordinates=almacen["coordenadas"],
        )
    
    def build(self):
        # Crear marcadores para todos los almacenes
        marcadores = [self.crear_marcador(alm) for alm in self.almacenes]
        
        # Calcular el centro del mapa (promedio de coordenadas)
        lat_promedio = sum(alm["coordenadas"].latitude for alm in self.almacenes) / len(self.almacenes)
        lon_promedio = sum(alm["coordenadas"].longitude for alm in self.almacenes) / len(self.almacenes)
        
        # Crear el mapa
        mapa = map.Map(
            expand=True,
            initial_center=map.MapLatitudeLongitude(lat_promedio, lon_promedio),
            initial_zoom=5,
            interaction_configuration=map.MapInteractionConfiguration(
                flags=map.MapInteractiveFlag.ALL
            ),
            on_init=lambda e: print("Mapa inicializado"),
            layers=[
                # Capa de tiles (el mapa base)
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("Error al cargar tile del mapa"),
                ),
                # Atribución (requerida por OpenStreetMap)
                map.RichAttribution(
                    attributions=[
                        map.TextSourceAttribution(
                            text="OpenStreetMap Contributors",
                            on_click=lambda e: e.page.launch_url(
                                "https://openstreetmap.org/copyright"
                            ),
                        ),
                    ]
                ),
                # Capa de marcadores
                map.MarkerLayer(
                    ref=self.marker_layer_ref,
                    markers=marcadores,
                ),
            ],
        )
        
        # Crear cards de almacenes
        cards_almacenes = []
        for almacen in self.almacenes:
            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.WAREHOUSE, color=almacen["icon_color"], size=30),
                        ft.Column([
                            ft.Text(
                                almacen["nombre"],
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=self.theme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                almacen["direccion"],
                                size=11,
                                color=self.theme.TEXT_SECONDARY,
                            ),
                        ], spacing=2, expand=True),
                    ], spacing=10),
                    ft.Container(height=5),
                    ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=14, color=self.theme.TEXT_SECONDARY),
                        ft.Text(
                            almacen["telefono"],
                            size=11,
                            color=self.theme.TEXT_SECONDARY,
                        ),
                    ], spacing=5),
                ], spacing=5),
                padding=12,
                bgcolor=self.theme.BACKGROUND_SECONDARY,
                border_radius=8,
                border=ft.border.all(1, self.theme.DIVIDER),
                on_click=lambda e, alm=almacen: self.mostrar_info_almacen(alm),
                ink=True,
            )
            cards_almacenes.append(card)
        
        # Layout principal
        contenido = ft.Container(
            content=ft.Column([
                # Título
                ft.Container(
                    content=ft.Text(
                        "Mapa Almacenes",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme.TEXT_PRIMARY
                    ),
                    padding=ft.padding.only(top=20, bottom=10),
                    alignment=ft.alignment.center,
                ),
                ft.Divider(height=1, thickness=1, color=self.theme.DIVIDER),
                # Contenido principal: Lista arriba + Mapa abajo
                ft.Container(
                    content=ft.Column([
                        # Lista de almacenes (horizontal)
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    "Nuestros Almacenes",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.theme.TEXT_PRIMARY,
                                ),
                                ft.Container(height=10),
                                ft.Row(
                                    controls=cards_almacenes,
                                    spacing=15,
                                    scroll=ft.ScrollMode.AUTO,
                                ),
                            ]),
                            padding=15,
                        ),
                        # Mapa
                        ft.Container(
                            content=mapa,
                            expand=True,
                            border=ft.border.all(2, self.theme.DIVIDER),
                            border_radius=10,
                        ),
                    ], spacing=10),
                    padding=ft.padding.only(left=20, right=20, bottom=20),
                    expand=True,
                ),
            ]),
            expand=True,
        )
        
        return contenido
