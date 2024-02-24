"""
CourseTool
Created by Seth Christie

Module main.py
"""
import tkinter as tk
from tkinter import ttk
from ctypes import windll
import yaml
import warnings
import sv_ttk

import interfaces

warnings.filterwarnings("ignore", category=DeprecationWarning)

# App constants
APP_WIDTH = 850
APP_HEIGHT = 800


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

    return cfg


# ----------------------------------------------------- classes --------------------------------------------------------

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Read config file
        self.config = readConfig('data/config.yml')

        # Load config into constants
        self.APP_TITLE = self.config['settings']['title']
        self.APP_VERSION = self.config['settings']['version']
        self.APP_LANG = self.config['settings']['lang']
        self.APP_FONT = self.config['settings']['font']
        self.EXPORT_FILETYPES = self.config['settings']['export_filetypes']
        self.UNDERGRAD_URL = self.config['catalog']['undergrad']['url']
        self.UNDERGRAD_TAGS = self.config['catalog']['undergrad']['tags']
        self.GRAD_URL = self.config['catalog']['grad']['url']
        self.GRAD_TAGS = self.config['catalog']['grad']['tags']
        self.DEFAULT_TERM = self.config['defaults']['term']
        self.DEFAULT_EXPORT = self.config['defaults']['export_type']
        self.DEFAULT_LEVEL = self.config['defaults']['level']

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
        self.title(self.APP_TITLE)
        self.iconbitmap('images/icon.ico')

        # Configure style
        self.style = ttk.Style()
        self.style.configure('Heading.TLabel', font=(self.APP_FONT, 18, 'bold'))
        self.style.configure('Heading2.TLabel', font=(self.APP_FONT, 12, 'bold'))
        self.style.configure('Normal.TLabel', font=(self.APP_FONT, 12))
        self.style.configure('Normal.TButton', font=(self.APP_FONT, 12))
        self.style.configure('Normal.TCheckbutton', font=(self.APP_FONT, 12))
        self.style.configure('Version.TLabel', font=(self.APP_FONT, 10))
        self.style.configure('Large.TButton', font=(self.APP_FONT, 16))

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
