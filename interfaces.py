#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: interfaces.py
Author: Seth Christie
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import course_functions
import main


# ----------------------------------------------------- classes --------------------------------------------------------

class MainFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.lift()

        # create string vars
        self.STR_TERM = tk.StringVar(value=parent.DEFAULT_TERM)
        self.STR_LEVEL = tk.StringVar(value=parent.DEFAULT_LEVEL)
        self.STR_URL = tk.StringVar(value=parent.DEFAULT_URL)
        self.STR_FILE = tk.StringVar(value='')
        self.STR_FILETYPE = tk.StringVar(value=parent.DEFAULT_FILETYPE)
        self.CHECK_EXPORT_ALL = tk.BooleanVar(value=False)
        self.CHECK_EXPORT_ME = tk.BooleanVar(value=False)
        self.CHECK_EXPORT_ADV = tk.BooleanVar(value=False)
        self.CHECK_EXPORT_CS = tk.BooleanVar(value=False)

        options = {'padx': 10, 'pady': 5}
        options_cb = {'padx': 10, 'pady': 5, 'column': 0, 'sticky': 'w', 'columnspan': 2}

        # create title
        self.title_label = ttk.Label(self, text=self.parent.APP_TITLE, style='Heading.TLabel')
        self.title_label.grid(row=0, column=0, pady=20, columnspan=3)

        # create term field
        self.term_label = ttk.Label(self, text="Term: ", style='Heading2.TLabel')
        self.term_entry = ttk.Entry(self, font=(parent.APP_FONT, '11'), width=35, textvariable=self.STR_TERM)
        self.term_label.grid(row=1, column=0, **options, sticky='e')
        self.term_entry.grid(row=1, column=1, **options, sticky='e')

        # create level field
        self.level_label = ttk.Label(self, text="Level: ", style='Heading2.TLabel')
        self.level_entry = ttk.Entry(self, font=(parent.APP_FONT, '11'), width=35, textvariable=self.STR_LEVEL)
        self.level_label.grid(row=2, column=0, **options, sticky='e')
        self.level_entry.grid(row=2, column=1, **options, sticky='e')

        # create url field
        self.url_label = ttk.Label(self, text="URL: ", style='Heading2.TLabel')
        self.url_entry = ttk.Entry(self, font=(parent.APP_FONT, '11'), width=35, textvariable=self.STR_URL)
        self.url_label.grid(row=3, column=0, **options, sticky='e')
        self.url_entry.grid(row=3, column=1, **options, sticky='e')

        # create csv file selection
        self.file_label = ttk.Label(self, text='CSV File:', style='Heading2.TLabel')
        self.file_entry = ttk.Entry(self, font=(parent.APP_FONT, '11'), width=35, textvariable=self.STR_FILE)
        self.file_browse = main.AppButton(self, text='Browse', command=self.browse, width=90, height=30,
                                          style='Normal.TButton', state='normal')
        self.file_label.grid(row=4, column=0, **options, sticky='e')
        self.file_entry.grid(row=4, column=1, **options, sticky='e')
        self.file_browse.grid(row=4, column=2, **options)

        # create export dropdown
        self.option_add("*TCombobox*Listbox*Font", (parent.APP_FONT, '12'))
        self.filetype_label = ttk.Label(self, text='Export Filetype:', style='Heading2.TLabel')
        self.filetype_check = ttk.Combobox(self, state='readonly', font=(parent.APP_FONT, '12'),
                                           values=parent.FILETYPES,
                                           style='Combobox.TCombobox',
                                           textvariable=self.STR_FILETYPE, width=10)
        self.filetype_label.grid(row=6, column=0, **options, sticky='w')
        self.filetype_check.grid(row=6, column=1, **options, sticky='w')

        # add spacing
        self.spacing1 = ttk.Label(self, text='', style='Normal.TLabel')
        self.spacing1.grid(row=7, column=0, pady=10)

        # create checkboxes
        self.exportall_checkbox = ttk.Checkbutton(self, text='Export All', variable=self.CHECK_EXPORT_ALL,
                                                  style='Normal.TCheckbutton')
        self.exportall_checkbox.grid(row=8, **options_cb)

        self.exportme_checkbox = ttk.Checkbutton(self, text='Export MECH Electives', variable=self.CHECK_EXPORT_ME,
                                                 style='Normal.TCheckbutton')
        self.exportme_checkbox.grid(row=9, **options_cb)

        self.exportadv_checkbox = ttk.Checkbutton(self, text='Export Advanced Electives',
                                                  variable=self.CHECK_EXPORT_ADV,
                                                  style='Normal.TCheckbutton')
        self.exportadv_checkbox.grid(row=10, **options_cb)

        self.exportcs_checkbox = ttk.Checkbutton(self, text='Export CS Electives',
                                                  variable=self.CHECK_EXPORT_CS,
                                                  style='Normal.TCheckbutton')
        self.exportcs_checkbox.grid(row=11, **options_cb)

        # add spacing
        self.spacing2 = ttk.Label(self, text='', style='Normal.TLabel')
        self.spacing2.grid(row=12, column=0, pady=10)

        # add run button
        self.run_button = main.AppButton(self, text='Run Course Tool', command=self.run, width=220, height=70,
                                         style='Large.TButton', state='normal')
        self.run_button.grid(row=13, column=0, **options, columnspan=3, sticky='s')

    def show_frame(self):
        """
        Function to display the current frame
        :return: None
        """
        self.pack(padx=10, pady=10)

    def hide_frame(self):
        """
        Function to hide the current frame
        :return: None
        """
        self.pack_forget()

    def browse(self):
        """
        Function to create a file browse window
        :return: None
        """
        file = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        if file.endswith('.csv'):
            self.STR_FILE.set(file)

    def run(self):
        """
        Run the Course Tool
        :return: None
        """
        tags = self.parent.TAGS
        catalog_url = self.STR_URL.get() + 'undergrad/'
        term = self.STR_TERM.get().replace(' ', '')

        # select correct filetype
        match self.STR_FILETYPE.get():
            case 'Excel':
                filetype = 'xlsx'
            case 'YAML':
                filetype = 'yml'
            case 'JSON':
                filetype = 'json'
            case _:
                filetype = 'xlsx'

        # print selected options
        print(f'[CourseTool] Term: {term}')
        print(f'[CourseTool] Level: {self.STR_LEVEL.get()}')
        print(f'[CourseTool] URL: {catalog_url}')
        print(f'[CourseTool] CSV File: {self.STR_FILE.get()}')
        print(f'[CourseTool] Export Filetype: {filetype}')
        print(f'[CourseTool] Export All? {self.CHECK_EXPORT_ALL.get()}')
        print(f'[CourseTool] Export MECH Electives? {self.CHECK_EXPORT_ME.get()}')
        print(f'[CourseTool] Export Adv. Electives? {self.CHECK_EXPORT_ADV.get()}')
        print(f'[CourseTool] Export CS Electives? {self.CHECK_EXPORT_CS.get()}')

        # retrieve course data
        data = course_functions.get_course_data(self.STR_FILE.get(), tags, catalog_url, self.CHECK_EXPORT_ALL.get())
        export_filename = f'{term}_{self.STR_LEVEL.get()}.{filetype}'

        # export course data
        course_functions.export_courses(data, filetype, f'exports/{export_filename}')

        # other options
        if self.CHECK_EXPORT_ME.get():
            mech_dict = course_functions.get_mech_electives(self, data)
            course_functions.export_courses(mech_dict, filetype, f'exports/{term}_MECH.{filetype}')

        if self.CHECK_EXPORT_ADV.get():
            adv_dict = course_functions.get_adv_electives(self, data)
            course_functions.export_courses(adv_dict, filetype, f'exports/{term}_ADV.{filetype}')

        if self.CHECK_EXPORT_CS.get():
            pass  # TODO export cs electives

        return data