import os
import time
import subprocess
from subprocess import PIPE
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from pulsonapplib import unpack, pulson
import socket

#matplotlib.use('TkAgg')

LARGE_FONT = ('Helvetica', 50, 'bold')
SMALLER_FONT = ('Helvetica', 20)
PRIMARY_COLOR = '#bcefff'
PRIMARY_HOVER_COLOR = '#a7e6f9'
PRIMARY_CLICK_COLOR = '#425f68'
NOT_PRIMARY_COLOR = '#ffbcbc'
HEAD_FOOT_COLOR = '#ffbce4'
HEAD_FOOT_HOVER_COLOR = '#f9a7d8'
HEAD_FOOT_CLICK_COLOR = '#684258'
SECONDARY_COLOR = '#3f3f3f'


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

    settings = open('./pulsonapplib/radar_parse_settings', 'r').read()
    settings = settings.replace('$dT_0$', dT_0)
    settings = settings.replace('$range_start$', range_start)
    settings = settings.replace('$range_stop$', range_stop)
    settings = settings.replace('$tx_gain_ind$', tx_gain_ind)
    settings = settings.replace('$pii$', pii)
    settings = settings.replace('$code_channel$', code_channel)

    file = open('./pulsonapplib/radar_settings', 'w')
    file.write(settings)


def get_unpack_binary_file():
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

        self.configure(bg=SECONDARY_COLOR)
        self.rowconfigure((0, 4), weight=1)
        self.rowconfigure((1, 2, 3), weight=2)
        self.columnconfigure((0, 1), weight=1)

        # All styles initialized here
        button_style = ttk.Style()
        button_style.configure('my.TButton', foreground=SECONDARY_COLOR, background=PRIMARY_COLOR, font=('Helvetica', 30))
        button_style.map('my.TButton', background=[('disabled', PRIMARY_COLOR),
                                                   ('pressed', PRIMARY_CLICK_COLOR),
                                                   ('active', PRIMARY_HOVER_COLOR)])
        back_button_style = ttk.Style()
        back_button_style.configure('back.TButton', foreground=SECONDARY_COLOR, background=HEAD_FOOT_COLOR,
                               font=('Helvetica', 30))
        back_button_style.map('back.TButton', background=[('disabled', HEAD_FOOT_COLOR),
                                                   ('pressed', HEAD_FOOT_CLICK_COLOR),
                                                   ('active', HEAD_FOOT_HOVER_COLOR)])

        label = tk.Label(self, text='PulsON440 Data Center', font=LARGE_FONT, bg=SECONDARY_COLOR, fg=HEAD_FOOT_COLOR)
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

        quit_button = ttk.Button(self, text='Quit', style='back.TButton', command=lambda: app.quit())
        quit_button.grid(padx=10, pady=10, row=3, column=0, columnspan=2, sticky='news')


# User entry boxes to change radar scan settings
class RadarSettingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg=SECONDARY_COLOR)
        self.rowconfigure((0, 1, 8), weight=1)
        self.rowconfigure((2, 3, 4, 5, 6, 7), weight=2)
        self.columnconfigure((0, 1), weight=1)

        label = tk.Label(self, text='Change Radar Settings', font=LARGE_FONT, bg=SECONDARY_COLOR, fg=HEAD_FOOT_COLOR)
        label.grid(row=0, column=0, columnspan=2)

        path_delay_label = tk.Label(self, text='Path Delay Through Antennae (ns)',
                                    font=SMALLER_FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        path_delay_label.grid(row=2, column=0, padx=10, pady=10, sticky='nes')
        path_delay_entry = tk.DoubleVar()
        path_delay_entry.set(10)
        path_delay_entry_box = tk.Entry(self, textvariable=path_delay_entry, font=('Helvetica', 20))
        path_delay_entry_box.grid(row=2, column=1, padx=10, pady=10, sticky='nws')

        range_start_label = tk.Label(self, text='Range Start (m)',
                                     font=SMALLER_FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        range_start_label.grid(row=3, column=0, padx=10, pady=10, sticky='nes')
        range_start_entry = tk.DoubleVar()
        range_start_entry.set(3)
        range_start_entry_box = tk.Entry(self, textvariable=range_start_entry, font=('Helvetica', 20))
        range_start_entry_box.grid(row=3, column=1, padx=10, pady=10, sticky='nws')

        range_end_label = tk.Label(self, text='Range End (m)',
                                   font=SMALLER_FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        range_end_label.grid(row=4, column=0, padx=10, pady=10, sticky='nes')
        range_end_entry = tk.DoubleVar()
        range_end_entry.set(15)
        range_end_entry_box = ttk.Entry(self, textvariable=range_end_entry, font=('Helvetica', 20))
        range_end_entry_box.grid(row=4, column=1, padx=10, pady=10, sticky='nws')

        transmit_gain_label = tk.Label(self, text='Transmit Gain Index',
                                       font=SMALLER_FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        transmit_gain_label.grid(row=5, column=0, padx=10, pady=10, sticky='nes')
        transmit_gain_entry = tk.IntVar()
        transmit_gain_entry.set(60)
        transmit_gain_entry_box = ttk.Entry(self, textvariable=transmit_gain_entry, font=('Helvetica', 20))
        transmit_gain_entry_box.grid(row=5, column=1, padx=10, pady=10, sticky='nws')

        pii_label = tk.Label(self, text='Pulse Integration Index',
                             font=SMALLER_FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        pii_label.grid(row=6, column=0, padx=10, pady=10, sticky='nes')
        pii_entry = tk.IntVar()
        pii_entry.set(11)
        pii_entry_box = ttk.Entry(self, textvariable=pii_entry, font=('Helvetica', 20))
        pii_entry_box.grid(row=6, column=1, padx=10, pady=10, sticky='nws')

        code_channel_label = tk.Label(self, text='Code Channel',
                                      font=SMALLER_FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        code_channel_label.grid(row=7, column=0, padx=10, pady=10, sticky='nes')
        code_channel_entry = tk.IntVar()
        code_channel_entry.set(0)
        code_channel_entry_box = ttk.Entry(self, font=('Helvetica', 20))
        code_channel_entry_box.grid(row=7, column=1, padx=10, pady=10, sticky='nws')

        submit_button = ttk.Button(self, text='SUBMIT', style='my.TButton',
                                   command=lambda: fetch_entries(path_delay_entry, range_start_entry, range_end_entry,
                                                                 transmit_gain_entry, pii_entry, code_channel_entry))
        submit_button.grid(row=8, column=0, columnspan=2)

        button0 = ttk.Button(self, text='Home', style='back.TButton',
                             command=lambda: controller.show_frame(StartPage))
        button0.grid(row=8, column=0, columnspan=2, sticky='news')


# This is where unpack would run
class DataCollection(tk.Frame):

    is_connected = False

    def start(self, a):
        run_type = '-' + str(a.get())

        cmds1 = ("sshpass -p 'TimHoward' ssh pi@192.168.2.1", "cd nile_bad_idea/pulsonapplib",
                "python control.py " + run_type + "")  # duplicate of below

        # process1 = subprocess.Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        process1 = subprocess.Popen('/bin/bash', stdin=PIPE)

        for cmd in cmds1:
            command = cmd + '\n'
            process1.stdin.write(command.encode(encoding='UTF-8'))
        process1.stdin.close()

        subprocess.Popen("python control.py " + run_type + "")

        # automatically stop after a minute
        # time.sleep(5)
        # DataCollection.stop()

    pulse_data_file_directory = r'../UAV-SAR-Radar/pulsonapplib/temp/untitled_data0'

    def save_binary_file(self, file_at_directory):
        file = filedialog.asksaveasfile(title="Save binary file as", initialdir='../UAV-SAR-Radar',
                                        filetypes=[('binary files', '*'), ('all files', '*.')], mode='wb')
        f = open(file_at_directory, 'rb')
        contents = f.read()
        file.write(contents)

        # make subprocess delete temporary file
        # subprocess.call('cd')

    def stop(self):
        cmds2 = ("sshpass -p 'TimHoward' ssh pi@192.168.2.1", "cd nile_bad_idea/pulsonapplib",
                 "echo 1 > control", "logout")

        # process2 = subprocess.Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        process2 = subprocess.Popen('/bin/bash', stdin=PIPE)

        for cmd in cmds2:
            command = cmd + '\n'
            process2.stdin.write(command.encode(encoding='UTF-8'))
        process2.stdin.close()

        scp = "sshpass -p 'TimHoward' scp pi@192.168.2.1:nile_bad_idea/pulsonapplib/temp/untitled_data0 /home/nilecamai/git/UAV-SAR-Radar/pulsonapplib/temp"
        subprocess.Popen(scp.encode('UTF-8'), shell=True)


    def try_connect(self):
        try:
            pulson.PulsON440.connection['sock'] = socket.socket(socket.AF_INET,
                           socket.SOCK_DGRAM)
            pulson.PulsON440.connection['sock'].setblocking(False)
            pulson.PulsON440.connection['sock'].bind((pulson.PulsON440.connection['udp_ip_host'],
                            pulson.PulsON440.connection['udp_port']))
            DataCollection.is_connected = False
        except:
            DataCollection.is_connected = False

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg=SECONDARY_COLOR)
        self.rowconfigure((0, 1, 8), weight=1)
        self.rowconfigure((2, 3, 4, 5, 6, 7), weight=2)
        self.columnconfigure((0, 1), weight=1)

        label = tk.Label(self, text='Data Collection', font=LARGE_FONT, bg=SECONDARY_COLOR, fg=HEAD_FOOT_COLOR)
        label.grid(row=0, column=0, columnspan=2)

        radio_button_frame = tk.Frame(self)
        radio_button_frame.configure(bg=SECONDARY_COLOR)
        radio_button_frame.rowconfigure((0, 1), weight=1)
        radio_button_frame.columnconfigure((0), weight=1)
        radio_button_frame.grid(row=2, column=0, rowspan=4, sticky='news')

        MODES = [
            ("Quick Scan", "q", 0),
            ("Collect", "c", 1),
        ]

        v = tk.StringVar()
        v.set("c")  # initialize

        for text, mode, iter in MODES:
            b = tk.Radiobutton(radio_button_frame, text=text,
                               variable=v, value=mode, indicatoron=0)
            b.configure(bg=PRIMARY_COLOR, foreground=SECONDARY_COLOR, font=('Helvetica', 30))
            b.grid(row=iter, sticky='news')

        start_button = ttk.Button(self, text='START', style='my.TButton',
                                       command=lambda: DataCollection.start(self, v))
        start_button.grid(row=2, column=1, rowspan=2, sticky='news')

        # while True:
        if DataCollection.is_connected == False:
            start_button.state(['disabled'])
        else:
            start_button.state(['!disabled'])

        stop_button = ttk.Button(self, text='STOP', style='my.TButton',
                                       command=lambda:
        DataCollection.save_binary_file(self, DataCollection.pulse_data_file_directory))
        stop_button.grid(row=4, column=1, rowspan=2, sticky='news')

        button0 = ttk.Button(self, text='Home', style='back.TButton',
                             command=lambda: controller.show_frame(StartPage))
        button0.grid(row=8, column=0, columnspan=2, sticky='news')


class UnpackExisting(tk.Frame):

    directory = None
    filename = None
    args_string = None

    def assign_directory(self, frame):
        UnpackExisting.directory = get_unpack_binary_file()

        index = None
        backslashed_directory = ''
        for f in range(0, len(UnpackExisting.directory)):
            if UnpackExisting.directory[f] == '/':
                index = f
            if UnpackExisting.directory[f] == ' ':
                backslashed_directory = backslashed_directory + '\ '
            else:
                backslashed_directory = backslashed_directory + UnpackExisting.directory[f]

        UnpackExisting.filename = UnpackExisting.directory[(index+1):]

        pulse_data_file_label = tk.Label(frame, text='', font=SMALLER_FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        pulse_data_file_label.grid(row=0, column=1, columnspan=2, sticky='news', padx=10, pady=10)

        pulse_data_file_label = tk.Label(frame, text='File Selected: ' + UnpackExisting.filename + '\n (' +
                                                    UnpackExisting.directory + ')',
                                         font=SMALLER_FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        pulse_data_file_label.grid(row=0, column=1, columnspan=2, sticky='news', padx=10, pady=10)

        UnpackExisting.args_string = 'python3 Pulson_Code/pulson440_unpack.py -f ' + UnpackExisting.directory + ' -v'
        print(UnpackExisting.args_string)

    def graph_unpack(self, data_file):
        unpack.main(UnpackExisting.directory)

        # Draws graph on window
        canvas = FigureCanvasTkAgg(unpack.f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=0, rowspan=2, columnspan=2)

        # Navigation tools
        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=6, column=0, columnspan=2, sticky='s')
        toolbar = NavigationToolbar2TkAgg(canvas, toolbar_frame)
        toolbar.update()

    def fetch_colormap_name(self, a):
        unpack.colormap_name = str(a.get())


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg=SECONDARY_COLOR)
        self.rowconfigure((0, 1, 8), weight=1)
        self.rowconfigure((2, 3, 4, 5, 6, 7), weight=2)
        self.columnconfigure((0, 1), weight=1)

        label = tk.Label(self, text='Unpack Existing', font=LARGE_FONT, bg=SECONDARY_COLOR, fg=HEAD_FOOT_COLOR)
        label.grid(row=0, column=0, columnspan=2)

        control_bar = tk.Frame(self)
        control_bar.configure(bg=SECONDARY_COLOR)
        control_bar.grid(row=2, column=0, columnspan=2)
        control_bar.rowconfigure((0, 1), weight=1)
        control_bar.columnconfigure((0, 1, 2, 3), weight=1)

        # Select pulse code directory
        pulse_data_file_button = ttk.Button(control_bar, text='Select Data File...', style='my.TButton',
                                            command=lambda: self.assign_directory(control_bar))
        pulse_data_file_button.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # Display string as label
        pulse_data_unpack_button = ttk.Button(control_bar, text='Unpack!', style='my.TButton',
                                              command=lambda: self.graph_unpack(UnpackExisting.directory))
        pulse_data_unpack_button.grid(row=0, column=3, rowspan=2, padx=10, pady=10, sticky='news')

        colormap_name_label = tk.Label(control_bar, text='Select a colormap:',
                                       font=SMALLER_FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        colormap_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='news')
        colormap_name_entry = tk.StringVar()
        colormap_name_entry.set('viridis')
        colormap_name_entry_box = tk.Entry(control_bar, textvariable=colormap_name_entry, font=('Helvetica', 20))
        colormap_name_entry_box.grid(row=1, column=1, padx=10, pady=10, sticky='news')
        submit_colormap_button = ttk.Button(control_bar, text='SUBMIT', style='my.TButton',
                                   command=lambda: UnpackExisting.fetch_colormap_name(self, colormap_name_entry))
        submit_colormap_button.grid(row=1, column=2, padx=10, pady=10, sticky='news')

        button0 = ttk.Button(self, text='Home', style='back.TButton',
                             command=lambda: controller.show_frame(StartPage))
        button0.grid(row=8, column=0, columnspan=2, sticky='news', padx=10, pady=10)

        """
        __init__ is run by the GUI appears EXCEPT the lambda functions -- triggered by user interaction
        """


app = PulsOnDataApp()
app.geometry('1920x1080')
app.mainloop()
