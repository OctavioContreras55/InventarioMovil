import flet as ft

class InventarioView:
    def __init__(self, page: ft.Page, user_data: dict, theme):
        self.page = page
        self.user_data = user_data
        self.theme = theme        
        self.search_query = ""
        self.productos_data = []
        self.productos_filtrados = []       
        self.main_container = None
    
    #Función para cargar productos desde la base de datos
    def cargar_productos_bd(self):
        from models.connection import get_db_connection
        
        try:
            conn = get_db_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True) # Usar dictionary=True al crear el cursor para obtener resultados como diccionarios
            
            cursor.execute("""
                SELECT id, codigo, nombre, marca, descripcion, categoria, cantidad, precio_unitario, ubicacion 
                FROM productos 
                ORDER BY nombre
            """) # Consulta SQL para obtener productos ordenados por nombre
            
            productos = cursor.fetchall() # Obtener todos los productos como una lista de diccionarios
            cursor.close()
            conn.close()
            
            return productos
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            return []
    
    #Función para manejar cambios en la barra de búsqueda
    def on_search_change(self, e):
        self.search_query = e.control.value.lower()
        
        # Filtrar productos
        if self.search_query == "":
            self.productos_filtrados = self.productos_data.copy()
        else:
            self.productos_filtrados = [
                producto for producto in self.productos_data
                if self.search_query in producto['nombre'].lower()
                or self.search_query in producto['marca'].lower()
                or self.search_query in producto['codigo'].lower()
            ]
        
        # Reconstruir y actualizar la vista
        # Buscar el PrincipalView en el page para actualizar content_area
        self.rebuild_view()
    
    #Función para reconstruir la vista con los productos filtrados
    def rebuild_view(self):
        if self.main_container:
            tabla_rows = []
            for producto in self.productos_filtrados:
                tabla_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(producto['codigo'])),
                            ft.DataCell(ft.Text(producto['nombre'])),
                            ft.DataCell(ft.Text(producto['marca'])),
                            ft.DataCell(ft.Text(str(producto['cantidad']))),
                        ]
                    )
                )
            
            # Actualizar solo la tabla (el tercer control dentro de Column)
            tabla = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Código")),
                    ft.DataColumn(ft.Text("Producto")),
                    ft.DataColumn(ft.Text("Marca")),
                    ft.DataColumn(ft.Text("Cantidad")),
                ],
                rows=tabla_rows,
                border=ft.border.all(1, self.theme.DIVIDER),
                border_radius=8,
                heading_row_color=self.theme.BACKGROUND_SECONDARY,
            )
            
            # Actualizar la tabla en el contenedor
            self.main_container.content.controls[3].content.controls[0] = tabla
            self.page.update()
    
    def build_search_bar(self):
        """Crea la barra de búsqueda"""
        return ft.Row(
            controls=[
                ft.TextField(
                    hint_text="Buscar por nombre, marca o código...",
                    prefix_icon=ft.Icons.SEARCH,
                    expand=True,
                    on_change=self.on_search_change,
                    border_radius=8,
                    bgcolor=self.theme.BACKGROUND_SECONDARY,
                    border_color=self.theme.DIVIDER,
                    focused_border_color=self.theme.ACCENT_PRIMARY,
                ),
            ],
            spacing=10,
        )
    
    #Función para construir la vista completa del inventario
    def build(self):
        # Cargar productos la primera vez
        if not self.productos_data:
            self.productos_data = self.cargar_productos_bd()
            self.productos_filtrados = self.productos_data.copy()
        
        # Construir filas de la tabla con productos filtrados
        tabla_rows = []
        for producto in self.productos_filtrados:
            tabla_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(producto['codigo'])),
                        ft.DataCell(ft.Text(producto['nombre'])),
                        ft.DataCell(ft.Text(producto['marca'])),
                        ft.DataCell(ft.Text(str(producto['cantidad']))),
                    ]
                )
            )
        
        # Construir la tabla
        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Marca")),
                ft.DataColumn(ft.Text("Cantidad")),
            ],
            rows=tabla_rows,
            border=ft.border.all(1, self.theme.DIVIDER),
            border_radius=8,
            heading_row_color=self.theme.BACKGROUND_SECONDARY,
        )
        
        # Construir la vista completa
        self.main_container = ft.Container(
            content=ft.Column(
                controls=[
                    # Título
                    ft.Container(
                        content=ft.Text(
                            "Inventario",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=self.theme.TEXT_PRIMARY
                        ),
                        padding=ft.padding.only(top=30, bottom=10, left=20),
                        alignment=ft.alignment.center,
                    ),
                    
                    # Divisor
                    ft.Container(
                      content=ft.Divider(height=1, thickness=1, color=self.theme.DIVIDER),
                      margin=ft.margin.only(left=20, right=20)
                    ),
                    
                    # Barra de búsqueda
                    ft.Container(
                        content=self.build_search_bar(),
                        padding=20,
                    ),
                    
                    # Tabla (con scroll)
                    ft.Container(
                        content=ft.Row(
                          controls=[
                            ft.Column(
                                controls=[tabla],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                          ],
                          scroll=ft.ScrollMode.ALWAYS,
                        ),
                        padding=ft.padding.only(left=20, right=20, bottom=20),
                        expand=True,
                    ),
                ],
            ),
            expand=True,
        )
        
        return self.main_container
