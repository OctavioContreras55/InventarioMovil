import flet as ft
from views import HomeView
from models.model_colors import DarkTheme

def main(page: ft.Page):
    page.window.width = 408
    page.window.height = 831
    page.window.resizable = False
    page.padding = 0
    page.bgcolor = DarkTheme.BACKGROUND_PRIMARY
    HomeView(page)

ft.app(target=main)