import flet as ft

class InventarioView:
    def __init__(self, page: ft.Page, user_data: dict, theme, parent_container=None):
        self.page = page
        self.user_data = user_data
        self.theme = theme
        self.parent_container = parent_container
        self.search_query = ""
        self.productos_data = []
        self.productos_filtrados = []       
        self.main_container = None
        self.filtro_categoria = ""
        self.categorias = []
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(self.file_picker)
        self.producto_actual_imagen = None
    
    def cargar_productos_bd(self):
        from models.connection import get_db_connection
        
        try:
            conn = get_db_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT id, codigo, nombre, marca, descripcion, categoria, cantidad, precio_unitario, ubicacion 
                FROM productos 
                ORDER BY nombre
            """)
            
            productos = cursor.fetchall()
            
            cursor.execute("SELECT DISTINCT categoria FROM productos ORDER BY categoria")
            self.categorias = [row['categoria'] for row in cursor.fetchall() if row['categoria']]
            
            cursor.close()
            conn.close()
            
            return productos
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            return []
    
    def on_search_change(self, e):
        self.search_query = e.control.value.lower()
        self.aplicar_filtros()
    
    def on_categoria_change(self, e):
        self.filtro_categoria = e.control.value if e.control.value != "Todas" else ""
        self.aplicar_filtros()
    
    def aplicar_filtros(self):
        if not self.search_query and not self.filtro_categoria:
            self.productos_filtrados = self.productos_data.copy()
        else:
            self.productos_filtrados = []
            for producto in self.productos_data:
                cumple_busqueda = True
                cumple_categoria = True
                
                if self.search_query:
                    cumple_busqueda = (
                        self.search_query in producto['nombre'].lower() or
                        self.search_query in producto['marca'].lower() or
                        self.search_query in producto['codigo'].lower()
                    )
                
                if self.filtro_categoria:
                    cumple_categoria = producto.get('categoria', '') == self.filtro_categoria
                
                if cumple_busqueda and cumple_categoria:
                    self.productos_filtrados.append(producto)
        
        self.rebuild_view()
    
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
                            ft.DataCell(ft.Text(f"${producto['precio_unitario']:.2f}" if producto.get('precio_unitario') else "")),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.IMAGE,
                                        icon_color=self.theme.ACCENT_PRIMARY,
                                        tooltip="Ver/Agregar imagen",
                                        on_click=lambda e, p=producto: self.ver_imagen(p),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=ft.Colors.BLUE_400,
                                        tooltip="Editar producto",
                                        on_click=lambda e, p=producto: self.editar_producto(p),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color=ft.Colors.RED_400,
                                        tooltip="Eliminar producto",
                                        on_click=lambda e, p=producto: self.eliminar_producto(p),
                                    ),
                                ])
                            ),
                        ]
                    )
                )
            
            tabla = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Código")),
                    ft.DataColumn(ft.Text("Producto")),
                    ft.DataColumn(ft.Text("Marca")),
                    ft.DataColumn(ft.Text("Cantidad")),
                    ft.DataColumn(ft.Text("Precio")),
                    ft.DataColumn(ft.Text("Acciones")),
                ],
                rows=tabla_rows,
                border=ft.border.all(1, self.theme.DIVIDER),
                border_radius=8,
                heading_row_color=self.theme.BACKGROUND_SECONDARY,
            )
            
            self.main_container.content.controls[3].content.controls[0].controls[0] = tabla
            self.page.update()
    
    def build_search_bar(self):
        return ft.Column(
            controls=[
                ft.Row(
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
                ),
                ft.Container(height=10),
                ft.Row(
                    controls=[
                        ft.Dropdown(
                            hint_text="Filtrar por categoría",
                            width=250,
                            options=[ft.dropdown.Option("Todas")] + [
                                ft.dropdown.Option(cat) for cat in self.categorias
                            ],
                            on_change=self.on_categoria_change,
                            border_radius=8,
                            bgcolor=self.theme.BACKGROUND_SECONDARY,
                            border_color=self.theme.DIVIDER,
                            focused_border_color=self.theme.ACCENT_PRIMARY,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Icon(ft.Icons.ADD, color=self.theme.TEXT_PRIMARY, size=20),
                            bgcolor=self.theme.ACCENT_PRIMARY,
                            padding=10,
                            border_radius=8,
                            on_click=self.abrir_dialog_agregar,
                            tooltip="Agregar Producto",
                            ink=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            spacing=0,
        )
    
    def abrir_dialog_agregar(self, e):
        self.dialog_codigo = ft.TextField(label="Código", border_color=self.theme.DIVIDER)
        self.dialog_nombre = ft.TextField(label="Nombre", border_color=self.theme.DIVIDER)
        self.dialog_marca = ft.TextField(label="Marca", border_color=self.theme.DIVIDER)
        self.dialog_descripcion = ft.TextField(label="Descripción", multiline=True, border_color=self.theme.DIVIDER)
        self.dialog_categoria = ft.TextField(label="Categoría", border_color=self.theme.DIVIDER)
        self.dialog_cantidad = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER, border_color=self.theme.DIVIDER)
        self.dialog_precio = ft.TextField(label="Precio Unitario", keyboard_type=ft.KeyboardType.NUMBER, border_color=self.theme.DIVIDER)
        self.dialog_ubicacion = ft.TextField(label="Ubicación", border_color=self.theme.DIVIDER)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Agregar Producto"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.dialog_codigo,
                        self.dialog_nombre,
                        self.dialog_marca,
                        self.dialog_descripcion,
                        self.dialog_categoria,
                        self.dialog_cantidad,
                        self.dialog_precio,
                        self.dialog_ubicacion,
                    ],
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=500,
                height=400,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialog(dialog)),
                ft.ElevatedButton(
                    "Guardar", 
                    on_click=lambda e: self.guardar_producto(dialog),
                    bgcolor=self.theme.ACCENT_PRIMARY,
                ),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def cerrar_dialog(self, dialog):
        dialog.open = False
        self.page.update()
    
    def guardar_producto(self, dialog):
        from models.connection import get_db_connection
        
        try:
            codigo = self.dialog_codigo.value
            nombre = self.dialog_nombre.value
            marca = self.dialog_marca.value
            descripcion = self.dialog_descripcion.value
            categoria = self.dialog_categoria.value
            cantidad = int(self.dialog_cantidad.value) if self.dialog_cantidad.value else 0
            precio = float(self.dialog_precio.value) if self.dialog_precio.value else 0.0
            ubicacion = self.dialog_ubicacion.value
            
            if not codigo or not nombre:
                self.dialog_codigo.error_text = "Requerido" if not codigo else None
                self.dialog_nombre.error_text = "Requerido" if not nombre else None
                self.page.update()
                return
            
            self.dialog_codigo.error_text = None
            self.dialog_nombre.error_text = None
            
            conn = get_db_connection()
            if not conn:
                self.mostrar_snackbar("Error de conexión a la base de datos", error=True)
                return
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM productos WHERE codigo = %s", (codigo,))
            if cursor.fetchone():
                self.dialog_codigo.error_text = "Código ya existe"
                self.page.update()
                cursor.close()
                conn.close()
                return
            
            cursor.execute("""
                INSERT INTO productos (codigo, nombre, marca, descripcion, categoria, cantidad, precio_unitario, ubicacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (codigo, nombre, marca, descripcion, categoria, cantidad, precio, ubicacion))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            self.cerrar_dialog(dialog)
            
            self.productos_data = self.cargar_productos_bd()
            self.search_query = ""
            self.filtro_categoria = ""
            self.productos_filtrados = self.productos_data.copy()
            
            nuevo_contenido = self.build()
            
            if self.parent_container:
                self.parent_container.content = nuevo_contenido
                self.parent_container.update()
            else:
                self.main_container.content = nuevo_contenido.content
                self.page.update()
            
            self.mostrar_snackbar("Producto agregado exitosamente")
            
        except ValueError:
            self.mostrar_snackbar("Cantidad y precio deben ser números válidos", error=True)
        except Exception as e:
            self.mostrar_snackbar(f"Error al guardar: {e}", error=True)
    
    def mostrar_snackbar(self, mensaje, error=False):
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.Colors.RED_400 if error else ft.Colors.GREEN_400,
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()
    
    def ver_imagen(self, producto):
        from models.connection import get_db_connection
        
        try:
            conn = get_db_connection()
            if not conn:
                self.mostrar_snackbar("Error de conexión", error=True)
                return
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT imagen FROM productos WHERE id = %s", (producto['id'],))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            imagen_path = result['imagen'] if result and result['imagen'] else None
            
            if imagen_path and imagen_path.strip():
                self.mostrar_dialog_imagen(producto, imagen_path)
            else:
                self.mostrar_dialog_opciones_imagen(producto)
                
        except Exception as e:
            self.mostrar_snackbar(f"Error: {e}", error=True)
    
    def mostrar_dialog_imagen(self, producto, imagen_path):
        dialog = ft.AlertDialog(
            title=ft.Text(f"Imagen: {producto['nombre']}"),
            content=ft.Container(
                content=ft.Column([
                    ft.Image(
                        src=imagen_path,
                        width=400,
                        height=400,
                        fit=ft.ImageFit.CONTAIN,
                        error_content=ft.Text("Error al cargar imagen"),
                    ),
                ]),
                width=450,
                height=450,
            ),
            actions=[
                ft.TextButton("Cambiar imagen", on_click=lambda e: self.cambiar_imagen(dialog, producto)),
                ft.TextButton("Cerrar", on_click=lambda e: self.cerrar_dialog(dialog)),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def mostrar_dialog_opciones_imagen(self, producto):
        dialog = ft.AlertDialog(
            title=ft.Text(f"Agregar imagen: {producto['nombre']}"),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=100, color=self.theme.TEXT_SECONDARY),
                    ft.Text("Este producto no tiene imagen", text_align=ft.TextAlign.CENTER),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Tomar foto",
                        icon=ft.Icons.CAMERA_ALT,
                        on_click=lambda e: self.tomar_foto(dialog, producto),
                        bgcolor=self.theme.ACCENT_PRIMARY,
                        color=ft.Colors.WHITE,
                        width=300,
                    ),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Seleccionar de galería",
                        icon=ft.Icons.PHOTO_LIBRARY,
                        on_click=lambda e: self.seleccionar_imagen(dialog, producto),
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        width=300,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=350,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialog(dialog)),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def cambiar_imagen(self, dialog_anterior, producto):
        self.cerrar_dialog(dialog_anterior)
        self.mostrar_dialog_opciones_imagen(producto)
    
    def tomar_foto(self, dialog, producto):
        self.producto_actual_imagen = producto
        self.cerrar_dialog(dialog)
        
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"],
            dialog_title="Tomar foto o seleccionar imagen"
        )
    
    def seleccionar_imagen(self, dialog, producto):
        self.producto_actual_imagen = producto
        self.cerrar_dialog(dialog)
        
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"],
            dialog_title="Seleccionar imagen"
        )
    
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            archivo = e.files[0]
            self.guardar_imagen(archivo.path)
    
    def guardar_imagen(self, imagen_path):
        from models.connection import get_db_connection
        import shutil
        import os
        
        if not self.producto_actual_imagen:
            return
        
        try:
            assets_dir = "assets/productos"
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir)
            
            extension = os.path.splitext(imagen_path)[1]
            nuevo_nombre = f"{self.producto_actual_imagen['codigo']}{extension}"
            destino = os.path.join(assets_dir, nuevo_nombre)
            
            shutil.copy(imagen_path, destino)
            
            conn = get_db_connection()
            if not conn:
                self.mostrar_snackbar("Error de conexión", error=True)
                return
            
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE productos SET imagen = %s WHERE id = %s",
                (destino, self.producto_actual_imagen['id'])
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            self.mostrar_snackbar("Imagen guardada exitosamente")
            self.producto_actual_imagen = None
            
        except Exception as e:
            self.mostrar_snackbar(f"Error al guardar imagen: {e}", error=True)
    
    def editar_producto(self, producto):
        self.mostrar_snackbar("Función de editar en desarrollo")
    
    def eliminar_producto(self, producto):
        from models.connection import get_db_connection
        
        def confirmar_eliminar(e):
            try:
                conn = get_db_connection()
                if not conn:
                    self.mostrar_snackbar("Error de conexión", error=True)
                    return
                
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE id = %s", (producto['id'],))
                conn.commit()
                cursor.close()
                conn.close()
                
                self.productos_data = self.cargar_productos_bd()
                self.search_query = ""
                self.filtro_categoria = ""
                self.productos_filtrados = self.productos_data.copy()
                
                nuevo_contenido = self.build()
                if self.parent_container:
                    self.parent_container.content = nuevo_contenido
                    self.parent_container.update()
                else:
                    self.main_container.content = nuevo_contenido.content
                    self.page.update()
                
                self.cerrar_dialog(dialog)
                self.mostrar_snackbar("Producto eliminado")
                
            except Exception as e:
                self.mostrar_snackbar(f"Error al eliminar: {e}", error=True)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Seguro que deseas eliminar '{producto['nombre']}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialog(dialog)),
                ft.ElevatedButton(
                    "Eliminar",
                    on_click=confirmar_eliminar,
                    bgcolor=ft.Colors.RED_700,
                    color=ft.Colors.WHITE,
                ),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def build(self):
        if not self.productos_data:
            self.productos_data = self.cargar_productos_bd()
            self.productos_filtrados = self.productos_data.copy()
        
        tabla_rows = []
        for producto in self.productos_filtrados:
            tabla_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(producto['codigo'])),
                        ft.DataCell(ft.Text(producto['nombre'])),
                        ft.DataCell(ft.Text(producto['marca'])),
                        ft.DataCell(ft.Text(str(producto['cantidad']))),
                        ft.DataCell(ft.Text(f"${producto['precio_unitario']:.2f}" if producto.get('precio_unitario') else "")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.IMAGE,
                                    tooltip="Ver imagen",
                                    icon_color=ft.Colors.BLUE_400,
                                    on_click=lambda e, p=producto: self.ver_imagen(p)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    icon_color=ft.Colors.ORANGE_400,
                                    on_click=lambda e, p=producto: self.editar_producto(p)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color=ft.Colors.RED_400,
                                    on_click=lambda e, p=producto: self.eliminar_producto(p)
                                ),
                            ], spacing=5)
                        ),
                    ]
                )
            )
        
        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Marca")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=tabla_rows,
            border=ft.border.all(1, self.theme.DIVIDER),
            border_radius=8,
            heading_row_color=self.theme.BACKGROUND_SECONDARY,
        )
        
        self.main_container = ft.Container(
            content=ft.Column(
                controls=[
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
                    ft.Container(
                      content=ft.Divider(height=1, thickness=1, color=self.theme.DIVIDER),
                      margin=ft.margin.only(left=20, right=20)
                    ),
                    ft.Container(
                        content=self.build_search_bar(),
                        padding=20,
                    ),
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
