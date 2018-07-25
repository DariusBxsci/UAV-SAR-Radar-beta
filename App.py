import matplotlib.pyplot as plt
import tkinter as tk
import os
from tkinter import ttk, filedialog, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
# import Pulson_Code.pulson440_unpack as unpack

#matplotlib.use('TkAgg')

LARGE_FONT = ('Helvetica', 50, 'bold')
SMALLER_FONT = ('Helvetica', 20)


class PulsOnDataApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Nile's Horrible Idea")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand='true')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, RadarSettingPage, DataCollection, UnpackExisting):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


# Takes user input and writes to radar_settings
def fetch_entries(a, b, c, d, e, f):

    dT_0 = str(a.get())
    range_start = str(b.get())
    range_stop = str(c.get())
    tx_gain_ind = str(d.get())
    pii = str(e.get())
    code_channel = str(f.get())

    print([dT_0, range_start, range_stop, tx_gain_ind, pii, code_channel])

    settings = open('./Pulson_Code/radar_parse_settings', 'r').read()
    settings = settings.replace('$dT_0$', dT_0)
    settings = settings.replace('$range_start$', range_start)
    settings = settings.replace('$range_stop$', range_stop)
    settings = settings.replace('$tx_gain_ind$', tx_gain_ind)
    settings = settings.replace('$pii$', pii)
    settings = settings.replace('$code_channel$', code_channel)

    file = open('./Pulson_Code/radar_settings', 'w')
    file.write(settings)

    '''

    error_message = 'Checking for errors...'

    if type(a) == tk.DoubleVar():
        path_delay = a.get()
    else:
        error_message = edit_error_message('\n Path Delay should be a floating-point value')

    range_start = b.get()
    range_stop = c.get()
    tx_gain_ind = d.get()
    pii = e.get()
    code_channel = f.get()

    print(path_delay)

    error_label = tk.Label(text=error_message)
    error_label.pack()

    '''


'''
def edit_error_message(string, error_message):
    error_message = error_message + string
    return error_message
'''


def get_data_file():
    data_file_directory = filedialog.askopenfilename(initialdir="../UAV-SAR-Radar", title="Select pulse array file",
                                                     filetypes=(("binary files", "*"),
                                                                ("comma-separated values", "*.csv")))
    return data_file_directory


def unpack_pulse_data(directory):
    print(directory)


# Opens this page on start
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='#3f3f3f')
        self.rowconfigure((0, 4), weight=1)
        self.rowconfigure((1, 2, 3), weight=2)
        self.columnconfigure((0, 1), weight=1)

        button_style = ttk.Style()
        button_style.configure('my.TButton', foreground='#3f3f3f', background='#bcefff', font=('Helvetica', 30))
        button_style.map('my.TButton', background=[('disabled', '#bcefff'),
                                                   ('pressed', '#425f68'),
                                                   ('active', '#a7e6f9')])

        label = tk.Label(self, text='PulsON440 Data Center', font=LARGE_FONT, bg='#3f3f3f', fg='#bcefff')
        label.grid(row=0, column=0, columnspan=2)

        button1 = ttk.Button(self, text='Change Radar\n     Settings', style='my.TButton',
                             command=lambda: controller.show_frame(RadarSettingPage))
        button1.grid(padx=10, pady=10, row=1, column=0, sticky='news')

        button2 = ttk.Button(self, text='Data Collection', style='my.TButton',
                             command=lambda: controller.show_frame(DataCollection))
        button2.grid(padx=10, pady=10, row=1, column=1, sticky='news')

        button3 = ttk.Button(self, text='Unpack Existing', style='my.TButton',
                             command=lambda: controller.show_frame(UnpackExisting))
        button3.grid(padx=10, pady=10, row=2, column=0, sticky='news')

        button4 = ttk.Button(self, text='Back Projection', style='my.TButton',
                             command=lambda: controller.show_frame(UnpackExisting))
        button4.grid(padx=10, pady=10, row=2, column=1, sticky='news')

        quit_button = ttk.Button(self, text='Quit', style='my.TButton', command=lambda: app.quit())
        quit_button.grid(padx=10, pady=10, row=3, column=0, columnspan=2, sticky='news')


# User entry boxes to change radar scan settings
class RadarSettingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='#3f3f3f')
        self.rowconfigure((0, 9), weight=1)
        self.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=2)
        self.columnconfigure((0, 1), weight=1)

        button_style = ttk.Style()
        button_style.configure('my.TButton', foreground='#3f3f3f', background='#bcefff', font=('Helvetica', 30))
        button_style.map('my.TButton', background=[('disabled', '#bcefff'),
                                                   ('pressed', '#425f68'),
                                                   ('active', '#a7e6f9')])

        label = tk.Label(self, text='Change Radar Settings', font=LARGE_FONT, bg='#3f3f3f', fg='#bcefff')
        label.grid(row=0, column=0, columnspan=2)

        path_delay_label = tk.Label(self, text='Path Delay Through Antennae (ns)',
                                    font=SMALLER_FONT, bg='#3f3f3f', fg='#bcefff')
        path_delay_label.grid(row=1, column=0, padx=10, pady=10, sticky='nes')
        path_delay_entry = tk.DoubleVar()
        path_delay_entry.set(10)
        path_delay_entry_box = tk.Entry(self, textvariable=path_delay_entry, font=('Helvetica', 20))
        path_delay_entry_box.grid(row=1, column=1, padx=10, pady=10, sticky='nws')

        range_start_label = tk.Label(self, text='Range Start (m)',
                                     font=SMALLER_FONT, bg='#3f3f3f', fg='#bcefff')
        range_start_label.grid(row=2, column=0, padx=10, pady=10, sticky='nes')
        range_start_entry = tk.DoubleVar()
        range_start_entry.set(3)
        range_start_entry_box = tk.Entry(self, textvariable=range_start_entry, font=('Helvetica', 20))
        range_start_entry_box.grid(row=2, column=1, padx=10, pady=10, sticky='nws')

        range_end_label = tk.Label(self, text='Range End (m)',
                                   font=SMALLER_FONT, bg='#3f3f3f', fg='#bcefff')
        range_end_label.grid(row=3, column=0, padx=10, pady=10, sticky='nes')
        range_end_entry = tk.DoubleVar()
        range_end_entry.set(15)
        range_end_entry_box = ttk.Entry(self, textvariable=range_end_entry, font=('Helvetica', 20))
        range_end_entry_box.grid(row=3, column=1, padx=10, pady=10, sticky='nws')

        transmit_gain_label = tk.Label(self, text='Transmit Gain Index',
                                       font=SMALLER_FONT, bg='#3f3f3f', fg='#bcefff')
        transmit_gain_label.grid(row=4, column=0, padx=10, pady=10, sticky='nes')
        transmit_gain_entry = tk.IntVar()
        transmit_gain_entry.set(60)
        transmit_gain_entry_box = ttk.Entry(self, textvariable=transmit_gain_entry, font=('Helvetica', 20))
        transmit_gain_entry_box.grid(row=4, column=1, padx=10, pady=10, sticky='nws')

        pii_label = tk.Label(self, text='Pulse Integration Index',
                             font=SMALLER_FONT, bg='#3f3f3f', fg='#bcefff')
        pii_label.grid(row=5, column=0, padx=10, pady=10, sticky='nes')
        pii_entry = tk.IntVar()
        pii_entry.set(11)
        pii_entry_box = ttk.Entry(self, textvariable=pii_entry, font=('Helvetica', 20))
        pii_entry_box.grid(row=5, column=1, padx=10, pady=10, sticky='nws')

        code_channel_label = tk.Label(self, text='Code Channel',
                                      font=SMALLER_FONT, bg='#3f3f3f', fg='#bcefff')
        code_channel_label.grid(row=6, column=0, padx=10, pady=10, sticky='nes')
        code_channel_entry = tk.IntVar()
        code_channel_entry.set(0)
        code_channel_entry_box = ttk.Entry(self, font=('Helvetica', 20))
        code_channel_entry_box.grid(row=6, column=1, padx=10, pady=10, sticky='nws')

        submit_button = ttk.Button(self, text='SUBMIT', style='my.TButton',
                                   command=lambda: fetch_entries(path_delay_entry, range_start_entry, range_end_entry,
                                                                 transmit_gain_entry, pii_entry, code_channel_entry))
        submit_button.grid(row=7, column=0, columnspan=2)

        button0 = ttk.Button(self, text='Home', style='my.TButton',
                             command=lambda: controller.show_frame(StartPage))
        button0.grid(row=8, column=0, columnspan=2, sticky='news')


# This is where unpack would run
class DataCollection(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='#3f3f3f')
        self.rowconfigure((0, 9), weight=1)
        self.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=2)
        self.columnconfigure((0, 1), weight=1)

        button_style = ttk.Style()
        button_style.configure('my.TButton', foreground='#3f3f3f', background='#bcefff', font=('Helvetica', 30))
        button_style.map('my.TButton', background=[('disabled', '#bcefff'),
                                                   ('pressed', '#425f68'),
                                                   ('active', '#a7e6f9')])

        label = tk.Label(self, text='Data Collection', font=LARGE_FONT, bg='#3f3f3f', fg='#bcefff')
        label.grid(row=0, column=0, columnspan=2)

        button0 = ttk.Button(self, text='Home', style='my.TButton',
                             command=lambda: controller.show_frame(StartPage))
        button0.grid(row=8, column=0, columnspan=2, sticky='news')

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7])

        # Draws graph on window
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=1, rowspan=3, sticky='news')

        # Navigation tools
        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=5, column=1, sticky='news')
        toolbar = NavigationToolbar2TkAgg(canvas, toolbar_frame)
        toolbar.update()


class UnpackExisting(tk.Frame):

    directory = None

    filename = None

    string_args = None

    def assign_directory(self):
        UnpackExisting.directory = get_data_file()

        index = None
        for f in range(0, len(UnpackExisting.directory)):
            if UnpackExisting.directory[f] == '/':
                index = f

        UnpackExisting.filename = UnpackExisting.directory[(index+1):]

        pulse_data_file_label = tk.Label(self, text='File Selected: ' + UnpackExisting.filename + '\n (' +
                                                    UnpackExisting.directory + ')',
                                         font=SMALLER_FONT, bg='#3f3f3f', fg='#bcefff')
        pulse_data_file_label.grid(row=1, column=1, sticky='nws', padx=10, pady=10)

        UnpackExisting.string_args = 'python3 Pulson_Code/pulson440_unpack.py -f ' + UnpackExisting.directory + ' -v'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg='#3f3f3f')
        self.rowconfigure((0, 9), weight=1)
        self.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=2)
        self.columnconfigure((0, 1), weight=1)

        label = tk.Label(self, text='Unpack Existing', font=LARGE_FONT, bg='#3f3f3f', fg='#bcefff')
        label.grid(row=0, column=0, columnspan=2)

        # Select pulse code directory
        pulse_data_file_button = ttk.Button(self, text='Select Data File...', style='my.TButton',
                                            command=lambda: self.assign_directory())
        pulse_data_file_button.grid(row=1, column=0, sticky='nes', padx=10, pady=10)

        # Display string as label
        pulse_data_file_label = tk.Label(self, text='', font=SMALLER_FONT, bg='#3f3f3f', fg='#bcefff')
        pulse_data_file_label.grid(row=1, column=1, sticky='nws', padx=10, pady=10)

        pulse_data_unpack_button = ttk.Button(self, text='Unpack!', style='my.TButton',
                                              command=lambda: os.system(UnpackExisting.string_args))
        pulse_data_unpack_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        button0 = ttk.Button(self, text='Home', style='my.TButton',
                             command=lambda: controller.show_frame(StartPage))
        button0.grid(row=8, column=0, columnspan=2, sticky='news', padx=10, pady=10)

        """
        __init__ is run by the GUI appears EXCEPT the lambda functions -- triggered by user interaction
        """


app = PulsOnDataApp()
app.geometry('1920x1080')
app.mainloop()
