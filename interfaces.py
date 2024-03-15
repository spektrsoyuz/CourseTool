"""
CourseTool
Created by Seth Christie

Module interfaces.py
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import warnings

import course_functions
import main

warnings.filterwarnings("ignore", category=DeprecationWarning)


# ----------------------------------------------------- classes --------------------------------------------------------

class MainFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.lift()

        # Create StringVars
        self.STR_TERM = tk.StringVar(value=parent.DEFAULT_TERM)
        self.STR_ARGOS = tk.StringVar(value='')
        self.STR_ARGOS_STS = tk.StringVar(value='')
        self.STR_EXPORT_FILETYPE = tk.StringVar(value=parent.DEFAULT_EXPORT)
        self.STR_LEVEL = tk.StringVar(value=parent.DEFAULT_LEVEL)
        self.CHECK_EXPORTALL = tk.BooleanVar(value=True)
        self.CHECK_EXPORTME = tk.BooleanVar(value=False)
        self.CHECK_EXPORTIDV = tk.BooleanVar(value=False)
        self.CHECK_EXPORTADV = tk.BooleanVar(value=False)

        options = {'padx': 10, 'pady': 5}
        options_cb = {'padx': 10, 'pady': 5, 'column': 0, 'sticky': 'w', 'columnspan': 2}

        # Title
        self.title_label = ttk.Label(self, text=parent.APP_TITLE, style='Heading.TLabel')
        self.title_label.grid(row=0, column=0, pady=20, columnspan=3)

        # Term selection
        self.term_label = ttk.Label(self, text='Term:', style='Heading2.TLabel')
        self.term_entry = ttk.Entry(self, font=(parent.APP_FONT, '11'), width=35, textvariable=self.STR_TERM)
        self.term_label.grid(row=1, column=0, **options, sticky='w')
        self.term_entry.grid(row=1, column=1, **options, sticky='e')

        # Argos file selection
        self.argos_label = ttk.Label(self, text='Argos File:', style='Heading2.TLabel')
        self.argos_entry = ttk.Entry(self, font=(parent.APP_FONT, '11'), width=35, textvariable=self.STR_ARGOS)
        self.argos_browse = main.AppButton(self, text='Browse', command=self.browse_argos, width=120, height=40,
                                           style='Normal.TButton')
        self.argos_label.grid(row=2, column=0, **options, sticky='w')
        self.argos_entry.grid(row=2, column=1, **options, sticky='e')
        self.argos_browse.grid(row=2, column=2, **options)

        # Argos status label
        self.argos_sts_label = ttk.Label(self, textvariable=self.STR_ARGOS_STS, style='Normal.TLabel')
        self.argos_sts_label.grid(row=3, column=1, **options)

        # Export Filetype
        self.option_add("*TCombobox*Listbox*Font", (parent.APP_FONT, '12'))
        self.filetype_label = ttk.Label(self, text='Export Filetype:', style='Heading2.TLabel')
        self.filetype_check = ttk.Combobox(self, state='readonly', font=(parent.APP_FONT, '12'),
                                           values=parent.EXPORT_FILETYPES,
                                           textvariable=self.STR_EXPORT_FILETYPE, width=30)
        self.filetype_label.grid(row=4, column=0, **options, sticky='w')
        self.filetype_check.grid(row=4, column=1, **options, sticky='e')

        # Spacing
        self.spacing1 = ttk.Label(self, text='', style='Normal.TLabel')
        self.spacing1.grid(row=5, column=0, pady=10)

        # Checkboxes
        self.exportall_check = ttk.Checkbutton(self, text='Export All', style='Normal.TCheckbutton',
                                               variable=self.CHECK_EXPORTALL)
        self.exportall_check.grid(row=6, **options_cb)
        self.exportme_check = ttk.Checkbutton(self, text='Export MECH Electives', style='Normal.TCheckbutton',
                                              variable=self.CHECK_EXPORTME)
        self.exportme_check.grid(row=8, **options_cb)
        self.exportidv_check = ttk.Checkbutton(self, text='Export by Subject', style='Normal.TCheckbutton',
                                               variable=self.CHECK_EXPORTIDV)
        self.exportidv_check.grid(row=7, **options_cb)
        self.exportadv_check = ttk.Checkbutton(self, text='Export Adv. Electives', style='Normal.TCheckbutton',
                                               variable=self.CHECK_EXPORTADV)
        self.exportadv_check.grid(row=9, **options_cb)

        # Spacing
        self.spacing2 = ttk.Label(self, text='', style='Normal.TLabel')
        self.spacing2.grid(row=10, column=0, pady=10)

        # Main buttons
        self.run_button = main.AppButton(self, text='Run Tool', command=self.run, style='Large.TButton', width=220,
                                         height=70)
        self.run_button.grid(row=11, column=0, **options, columnspan=3, sticky='s')

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

    def browse_argos(self):
        """
        Function to create a file browse window for the Argos file
        :return: None
        """
        file = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        if file.endswith('.csv'):
            self.STR_ARGOS.set(file)
            self.STR_ARGOS_STS.set('Argos File Selected')
            self.argos_sts_label.configure(foreground='lime green')

    def run(self):
        """
        Run the Course Tool
        :return: None
        """
        catalog = []
        catalog_url = ''
        term = self.STR_TERM.get().replace('Summer', 'S').replace('Winter', 'W')
        term = term.replace(' ', '')
        filetype = 'xlsx'

        # Print options
        print(self.STR_ARGOS.get())
        print(self.STR_TERM.get())
        print(self.STR_LEVEL.get())
        print(self.CHECK_EXPORTALL.get())
        print(self.CHECK_EXPORTADV.get())
        print(self.CHECK_EXPORTIDV.get())
        print(self.CHECK_EXPORTME.get())

        # Select correct filetype
        match self.STR_EXPORT_FILETYPE.get():
            case 'Excel':
                filetype = 'xlsx'
            case 'YAML':
                filetype = 'yml'
            case 'JSON':
                filetype = 'json'

        # Select correct course level
        match self.STR_LEVEL.get():
            case 'Undergrad':
                catalog = self.parent.UNDERGRAD_TAGS
                catalog_url = self.parent.UNDERGRAD_URL
            case 'Grad':
                catalog = self.parent.GRAD_TAGS
                catalog_url = self.parent.GRAD_URL

        # Get course data
        data = course_functions.get_course_data(self.STR_ARGOS.get(), catalog, catalog_url, self.CHECK_EXPORTALL.get())
        export_name = f'{term}_{self.STR_LEVEL.get()}.{filetype}'

        # Export initial course data
        course_functions.export_courses(data, filetype, f'exports/{export_name}')

        # Special options
        if self.CHECK_EXPORTME.get():
            mech_dict = course_functions.get_mech_electives(data)
            course_functions.export_courses(mech_dict, filetype, f'exports/{term}_MECH.{filetype}')

        if self.CHECK_EXPORTADV.get():
            pass  # TODO export advanced electives
            # course_functions.getAdvElectives(f'exports/{export_name}')

        if self.CHECK_EXPORTIDV.get():
            pass  # TODO export in multiple files

        return data
