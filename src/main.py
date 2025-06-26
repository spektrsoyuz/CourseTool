import flet as ft
from flet.core.page import Page
from flet.core.types import ThemeMode, AppView


def main(page: Page) -> None:
    page.title = 'Course Tool'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ThemeMode.DARK

    page.update()


if __name__ == '__main__':
    ft.app(target=main)
