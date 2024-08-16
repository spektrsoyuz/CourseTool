#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: main.py
Author: Seth Christie
"""
import tkinter as tk
from tkinter import ttk
from ctypes import windll
import yaml
import sv_ttk

import interfaces

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


def read_config(filename):
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

        # read config.yml into vars
        self.config = read_config('data/config.yml')

        self.APP_TITLE = self.config['app']['title']
        self.APP_VERSION = self.config['app']['version']
        self.APP_LANG = self.config['app']['lang']
        self.APP_FONT = self.config['app']['font']
        self.DEFAULT_TERM = self.config['defaults']['term']
        self.DEFAULT_LEVEL = self.config['defaults']['level']
        self.DEFAULT_URL = self.config['defaults']['url']
        self.DEFAULT_FILETYPE = self.config['defaults']['filetype']
        self.FILETYPES = self.config['app']['filetypes']
        self.TAGS = self.config['app']['tags']

        self.MISC_CFILTER = self.config['misc']['cfilter']
        self.MISC_CAFILTER = self.config['misc']['cafilter']

        # set theme to dark theme
        sv_ttk.set_theme('dark')

        # determine geometry
        self.attributes('-alpha', 0.0)
        self.update_idletasks()
        x = int((self.winfo_screenwidth() / 2) - (APP_WIDTH / 2))
        y = int((self.winfo_screenheight() / 2) - (APP_HEIGHT / 2))
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}')

        # configure the root window
        self.resizable(False, False)
        self.title(self.APP_TITLE)
        self.iconbitmap('data/icon.ico')

        # configure style
        self.style = ttk.Style()
        self.style.configure('Heading.TLabel', font=(self.APP_FONT, 18, 'bold'))
        self.style.configure('Heading2.TLabel', font=(self.APP_FONT, 12, 'bold'))
        self.style.configure('Normal.TLabel', font=(self.APP_FONT, 12))
        self.style.configure('Normal.TButton', font=(self.APP_FONT, 12))
        self.style.configure('Normal.TCheckbutton', font=(self.APP_FONT, 12))
        self.style.configure('Combobox.TCombobox', selectbackground='#222222')
        self.style.configure('Version.TLabel', font=(self.APP_FONT, 10))
        self.style.configure('Large.TButton', font=(self.APP_FONT, 16))

        # add frames to container
        self.mainframe = interfaces.MainFrame(self)

        # display main frame on instantiation of app
        self.mainframe.show_frame()
        self.attributes('-alpha', 1.0)
        self.lift()


class AppButton(ttk.Frame):
    def __init__(self, parent, height=None, width=None, text="", command=None, style=None, state='disabled'):
        ttk.Frame.__init__(self, parent, height=height, width=width, style=style)

        self.pack_propagate(False)
        self._btn = ttk.Button(self, text=text, command=command, style=style, state=state)
        self._btn.pack(fill=tk.BOTH, expand=1)

    def enable(self):
        self._btn.config(state=tk.NORMAL)

    def disable(self):
        self._btn.config(state=tk.DISABLED)


# ------------------------------------------------------- main ---------------------------------------------------------

if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)
    app = Application()
    app.protocol("WM_DELETE_WINDOW", close_window)

    # start app
    app.mainloop()
