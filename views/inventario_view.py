import flet as ft

class InventarioView:
    def __init__(self, page: ft.Page, user_data: dict, theme):
        self.page = page
        self.user_data = user_data
        self.theme = theme
        
        # Variables para búsqueda y filtrado
        self.search_query = ""
        self.productos_data = []
        self.productos_filtrados = []
        
        # Referencia al contenedor principal (se establece al construir)
        self.main_container = None
    
    def cargar_productos_bd(self):
        """Carga todos los productos desde la base de datos"""
        from models.connection import get_db_connection
        
        try:
            conn = get_db_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT id, codigo, nombre, marca, categoria, cantidad, precio, ubicacion 
                FROM productos 
                ORDER BY nombre
            """)
            
            productos = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return productos
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            return []
    
    def on_search_change(self, e):
        """Se ejecuta cada vez que el usuario escribe en la búsqueda"""
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
    
    def rebuild_view(self):
        """Reconstruye solo la tabla sin regenerar todo"""
        if self.main_container:
            # Reconstruir tabla con productos filtrados
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
    
    def build(self):
        """Construye y retorna la vista de Inventario"""
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
                            "Gestión de Inventario",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=self.theme.TEXT_PRIMARY
                        ),
                        padding=ft.padding.only(top=30, bottom=10),
                        alignment=ft.alignment.center,
                    ),
                    
                    # Divisor
                    ft.Divider(height=1, thickness=1, color=self.theme.DIVIDER),
                    
                    # Barra de búsqueda
                    ft.Container(
                        content=self.build_search_bar(),
                        padding=20,
                    ),
                    
                    # Tabla (con scroll)
                    ft.Container(
                        content=ft.Column(
                            controls=[tabla],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        padding=ft.padding.only(left=20, right=20, bottom=20),
                        expand=True,
                    ),
                ],
            ),
            expand=True,
        )
        
        return self.main_container
