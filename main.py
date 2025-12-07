import sys
import os

# Agregar el directorio actual al path para que encuentre los módulos locales
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Importar después de agregar al path
import flet as ft
from views.home_view import HomeView
from models.model_colors import DarkTheme

def main(page: ft.Page):
    page.window.width = 408
    page.window.height = 831
    page.window.resizable = False
    page.padding = 0
    page.bgcolor = DarkTheme.BACKGROUND_PRIMARY
    HomeView(page)

ft.app(target=main)