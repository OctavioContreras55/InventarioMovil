import flet as ft
import requests

class ControlPuertaView:
    def __init__(self, page: ft.Page, user_data: dict, theme):
        self.page = page
        self.user_data = user_data
        self.theme = theme
        self.codigo_ingresado = ""
        self.codigo_display = None
        self.status_text = None
        self.API_URL = "http://192.168.100.34"
    
    def agregar_digito(self, digito):
        if len(self.codigo_ingresado) < 4:
            self.codigo_ingresado += str(digito)
            self.codigo_display.value = "•" * len(self.codigo_ingresado)
            self.page.update()
    
    def borrar_digito(self):
        if len(self.codigo_ingresado) > 0:
            self.codigo_ingresado = self.codigo_ingresado[:-1]
            self.codigo_display.value = "•" * len(self.codigo_ingresado)
            self.page.update()
    
    def limpiar_codigo(self):
        self.codigo_ingresado = ""
        self.codigo_display.value = ""
        self.page.update()
    
    def abrir_puerta(self, e):
        if len(self.codigo_ingresado) != 4:
            self.mostrar_estado("Ingresa un código de 4 dígitos", error=True)
            return
        
        try:
            response = requests.post(
                f"{self.API_URL}/puerta/abrir",
                json={"codigo": self.codigo_ingresado},
                timeout=5
            )
            
            data = response.json()
            
            if response.status_code == 200:
                if data.get("success"):
                    self.mostrar_estado("✓ Código correcto - Puerta abierta", error=False)
                    self.limpiar_codigo()
                else:
                    self.mostrar_estado("✗ Código incorrecto", error=True)
                    self.limpiar_codigo()
            else:
                self.mostrar_estado("Error al comunicarse con el ESP32", error=True)
                
        except requests.exceptions.Timeout:
            self.mostrar_estado("Tiempo de espera agotado", error=True)
        except requests.exceptions.ConnectionError:
            self.mostrar_estado("No se puede conectar con el ESP32", error=True)
        except Exception as e:
            self.mostrar_estado(f"Error: {str(e)}", error=True)
    
    def cerrar_puerta(self, e):
        try:
            response = requests.post(
                f"{self.API_URL}/puerta/cerrar",
                timeout=5
            )
            
            if response.status_code == 200:
                self.mostrar_estado("Puerta cerrada", error=False)
            else:
                self.mostrar_estado("Error al cerrar puerta", error=True)
                
        except Exception as e:
            self.mostrar_estado(f"Error: {str(e)}", error=True)
    
    def mostrar_estado(self, mensaje, error=False):
        self.status_text.value = mensaje
        self.status_text.color = ft.Colors.RED_400 if error else ft.Colors.GREEN_400
        self.page.update()
    
    def crear_boton_numero(self, numero):
        return ft.Container(
            content=ft.Text(str(numero), size=24, weight=ft.FontWeight.BOLD),
            width=80,
            height=80,
            bgcolor=self.theme.BACKGROUND_SECONDARY,
            border_radius=10,
            alignment=ft.alignment.center,
            on_click=lambda e: self.agregar_digito(numero),
            ink=True,
        )
    
    def build(self):
        self.codigo_display = ft.TextField(
            value="",
            text_align=ft.TextAlign.CENTER,
            text_size=32,
            password=True,
            read_only=True,
            border_color=self.theme.ACCENT_PRIMARY,
            focused_border_color=self.theme.ACCENT_PRIMARY,
            hint_text="Ingresa código",
            width=250,
        )
        
        self.status_text = ft.Text(
            "",
            size=16,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        
        teclado = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.crear_boton_numero(1),
                        self.crear_boton_numero(2),
                        self.crear_boton_numero(3),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
                ft.Row(
                    controls=[
                        self.crear_boton_numero(4),
                        self.crear_boton_numero(5),
                        self.crear_boton_numero(6),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
                ft.Row(
                    controls=[
                        self.crear_boton_numero(7),
                        self.crear_boton_numero(8),
                        self.crear_boton_numero(9),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.BACKSPACE, color=self.theme.TEXT_PRIMARY),
                            width=80,
                            height=80,
                            bgcolor=self.theme.BACKGROUND_SECONDARY,
                            border_radius=10,
                            alignment=ft.alignment.center,
                            on_click=lambda e: self.borrar_digito(),
                            ink=True,
                        ),
                        self.crear_boton_numero(0),
                        ft.Container(
                            content=ft.Icon(ft.Icons.CLEAR, color=self.theme.TEXT_PRIMARY),
                            width=80,
                            height=80,
                            bgcolor=self.theme.BACKGROUND_SECONDARY,
                            border_radius=10,
                            alignment=ft.alignment.center,
                            on_click=lambda e: self.limpiar_codigo(),
                            ink=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
            ],
            spacing=15,
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=20),
                    ft.Icon(
                        ft.Icons.LOCK,
                        size=60,
                        color=self.theme.ACCENT_PRIMARY
                    ),
                    ft.Text(
                        "Control de Puerta",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme.TEXT_PRIMARY
                    ),
                    ft.Container(height=15),
                    self.codigo_display,
                    ft.Container(height=5),
                    self.status_text,
                    ft.Container(height=20),
                    teclado,
                    ft.Container(height=20),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Desbloquear",
                                icon=ft.Icons.LOCK_OPEN,
                                on_click=self.abrir_puerta,
                                bgcolor=ft.Colors.GREEN_700,
                                color=ft.Colors.WHITE,
                                width=180,
                                height=50,
                            ),
                            ft.ElevatedButton(
                                "Bloquear",
                                icon=ft.Icons.LOCK,
                                on_click=self.cerrar_puerta,
                                bgcolor=ft.Colors.RED_700,
                                color=ft.Colors.WHITE,
                                width=180,
                                height=50,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Container(height=20),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=20,
        )
