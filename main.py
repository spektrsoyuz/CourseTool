"""
CourseTool
Created by Seth Christie

Module main.py
"""
import tkinter as tk
import sv_ttk
from tkinter import ttk
from ctypes import windll

import yaml

import interfaces

# App constants
APP_WIDTH = 850
APP_HEIGHT = 800
APP_TITLE = 'Course Tool'
APP_VERSION = 'v1.0'
APP_FONT = 'Helvetica'
EXPORT_FILETYPES = ['Excel', 'JSON', 'YAML']

# String defaults
DEFAULT_TERM = 'Winter 2024'
DEFAULT_ARGOS = 'C:/Users/schri/OneDrive/Documents/Code Projects/CourseTool_Demo/summer24_all.csv'
DEFAULT_EXPORT = 'Excel'
DEFAULT_LEVEL = 'Undergrad'


# ---------------------------------------------------- functions -------------------------------------------------------

def close_window():
    """
    Function to close the application window
    :return: None
    """
    app.destroy()


def readConfig(filename):
    """
    Function to read the config file and output parameters
    :param filename: Name of the config file
    :return: List of config parameters
    """
    with open(filename, 'r') as file:
        cfg = yaml.safe_load(file)
        undergrad_catalog = cfg['catalog']['undergrad']['tags']
        grad_catalog = cfg['catalog']['undergrad']['tags']
        undergrad_url = cfg['catalog']['undergrad']['url']
        grad_url = cfg['catalog']['grad']['url']
    return [undergrad_catalog, grad_catalog, undergrad_url, grad_url]


# ----------------------------------------------------- classes --------------------------------------------------------

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set theme to dark
        sv_ttk.set_theme('dark')

        # Determine geometry
        self.attributes('-alpha', 0.0)
        self.update_idletasks()
        x = int((self.winfo_screenwidth() / 2) - (APP_WIDTH / 2))
        y = int((self.winfo_screenheight() / 2) - (APP_HEIGHT / 2))
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}')

        # Configure the root window
        self.resizable(False, False)
        self.title(APP_TITLE)
        self.iconbitmap('images/icon.ico')

        # Configure style
        self.style = ttk.Style()
        self.style.configure('Heading.TLabel', font=(APP_FONT, 18, 'bold'))
        self.style.configure('Heading2.TLabel', font=(APP_FONT, 12, 'bold'))
        self.style.configure('Normal.TLabel', font=(APP_FONT, 12))
        self.style.configure('Normal.TButton', font=(APP_FONT, 12))
        self.style.configure('Normal.TCheckbutton', font=(APP_FONT, 12))
        self.style.configure('Version.TLabel', font=(APP_FONT, 10))

        # Add frames to container
        self.mainframe = interfaces.MainFrame(self)

        # Show the main frame on app start
        self.mainframe.show_frame()
        self.attributes('-alpha', 1.0)
        self.lift()


class AppButton(ttk.Frame):
    def __init__(self, parent, height=None, width=None, text="", command=None, style=None):
        ttk.Frame.__init__(self, parent, height=height, width=width, style=style)

        self.pack_propagate(False)
        self._btn = ttk.Button(self, text=text, command=command, style=style)
        self._btn.pack(fill=tk.BOTH, expand=1)


# ------------------------------------------------------- main ---------------------------------------------------------

if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)
    app = Application()
    app.protocol("WM_DELETE_WINDOW", close_window)

    # start app
    app.mainloop()
