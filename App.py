import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import subprocess
from subprocess import PIPE
import filecmp
import threading
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from pulsonapplib import unpack, sar
# matplotlib.use('TkAgg')
"""
'fixed', 'clearlyu alternate glyphs', 'times', 'courier 10 pitch', 'newcenturyschlbk', 'open look glyph',
'bitstream charter', 'song ti', 'zapf dingbats', 'itc zapf dingbats', 'helvetica', 'avantgarde', 'nimbus roman no9 l',
'open look cursor', 'newspaper', 'clearlyu ligature', 'mincho', 'clearlyu devangari extra', 'nimbus sans l',
'clearlyu pua', 'palatino', 'urw gothic l', 'courier', 'urw bookman l', 'century schoolbook l', 'clearlyu',
'itc avant garde gothic', 'avant garde gothic', 'nimbus mono l', 'clean', 'nil', 'clearlyu arabic',
'clearlyu devanagari', 'dingbats', 'zapfdingbats', 'zapf chancery', 'symbol', 'itc zapf chancery',
'standard symbols l', 'gothic', 'new century schoolbook', 'itc bookman', 'bookman', 'urw chancery l',
'clearlyu arabic extra'
"""
# avantgarde, urw gothic l, zapf chancery,

x_pad = 10
y_pad = 10


"""
# Blues
BUTTON_COLOR = '#bcefff'
BUTTON_HOVER_COLOR = '#a7e6f9'
BUTTON_CLICK_COLOR = '#425f68'
# Red
ERROR_COLOR = '#ffbcbc'
# Green
SUCCESS_COLOR = '#bcffc8'
# Oranges

# CONTRAST_BUTTON_COLOR = '#ffe8bc'
# CONTRAST_BUTTON_HOVER_COLOR = '#f9dca7'
# CONTRAST_BUTTON_CLICK_COLOR = '#685a42'

# Pinks
CONTRAST_BUTTON_COLOR = '#ffbce4'
CONTRAST_BUTTON_HOVER_COLOR = '#f9a7d8'
CONTRAST_BUTTON_CLICK_COLOR = '#684258'
# Grey
INTERFACE_COLOR = '#3f3f3f'
"""

# -----------------------------------------------------------------
#                           CLEAN THEME
# -----------------------------------------------------------------
# -----------------------------Fonts-------------------------------
# Title
LARGE_FONT = ('avantgarde', 50, 'bold')
# Labels
SMALLER_FONT = ('helvetica', 20)
# Buttons and Medium Text
BODY_FONT = ('avantgarde', 30)
# -----------------------------Colors------------------------------
# Title
TITLE_COLOR = '#a9a9a9'  # light grey
# Title Background
TITLE_BACKGROUND = '#ffffff'  # white
# Interface
INTERFACE_COLOR = '#efefef'  # dark white (thisthecolorofmypants?)
# Label
LABEL_COLOR = '#545454'  # dark grey
# Button
BUTTON_COLOR = '#c1e8f0'  # sky blue
BUTTON_HOVER_COLOR = '#ade1eb'
BUTTON_CLICK_COLOR = '#98d9e6'
# Contrast Button
CONTRAST_BUTTON_COLOR = '#ff3336'  # watermelon pink
CONTRAST_BUTTON_HOVER_COLOR = '#ff1a1d'
CONTRAST_BUTTON_CLICK_COLOR = '#ff0004'
# Disabled Color
DISABLED_COLOR = '#e6e6e6'  # grey
# Error
ERROR_COLOR = '#ff9999'  # pastel red
ERROR_HOVER_COLOR = '#ff8080'
ERROR_CLICK_COLOR = '#ff6666'
# Success
SUCCESS_COLOR = '#99ffac'  # pastel green
SUCCESS_HOVER_COLOR = '#80ff97'
SUCCESS_CLICK_COLOR = '#66ff82'
"""

# -----------------------------------------------------------------
#                          CLASSY THEME
# -----------------------------------------------------------------
# -----------------------------Fonts-------------------------------
# Title
LARGE_FONT = ('zapf chancery', 50, 'bold')
# Labels
SMALLER_FONT = ('palatino', 20)
# Buttons and Medium Text
BODY_FONT = ('new century schoolbook', 30)
# -----------------------------Colors------------------------------
# Title
TITLE_COLOR = '#8c8c8c'  # light grey
# Title Background
TITLE_BACKGROUND = '#ffffff'  # white
# Interface
INTERFACE_COLOR = '#d9d9d9'  # paper grey
# Label
LABEL_COLOR = '#393939'  # dark grey
# Button
BUTTON_COLOR = '#aca0a7'  # dusty
BUTTON_HOVER_COLOR = '#a0929a'
BUTTON_CLICK_COLOR = '#96858f'
# Contrast Button
CONTRAST_BUTTON_COLOR = '#6d7993'  # lavender
CONTRAST_BUTTON_HOVER_COLOR = '#626c84'
CONTRAST_BUTTON_CLICK_COLOR = '#576075'
# Disabled Color
DISABLED_COLOR = '#cccccc'  # grey
# Error
ERROR_COLOR = '#ff9999'  # pastel red
ERROR_HOVER_COLOR = '#ff8080'
ERROR_CLICK_COLOR = '#ff6666'
# Success
SUCCESS_COLOR = '#99ffac'  # pastel green
SUCCESS_HOVER_COLOR = '#80ff97'
SUCCESS_CLICK_COLOR = '#66ff82'
"""

class PulsOnDataApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Nile's Horrible Idea")
        img = tk.Image("photo", file="pulsonapplib/fuego.png")
        self.tk.call('wm', 'iconphoto', self._w, img)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand='true')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, RadarSettingPage, DataCollection, UnpackExisting, BackProjection, AboutApp):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def blank_message(self):
        self.error_success_label = tk.Label(self, text='', font=SMALLER_FONT, bg=INTERFACE_COLOR,
                                            fg=INTERFACE_COLOR)
        self.error_success_label.grid(row=1, column=0, columnspan=2, sticky="news")

    def show_error_message(self, message):
        self.error_success_label['text'] = message
        self.error_success_label['fg'] = ERROR_COLOR

    def show_success_message(self, message):
        self.error_success_label['text'] = message
        self.error_success_label['fg'] = SUCCESS_COLOR

    def clear_message(self):
        self.error_success_label['text'] = ''
        self.error_success_label['fg'] = INTERFACE_COLOR

    def default_config(self, controller, title):
        self.configure(bg=INTERFACE_COLOR)
        self.rowconfigure((0, 1, 8), weight=1)
        self.rowconfigure((2, 3, 4, 5, 6, 7), weight=2)
        self.columnconfigure((0, 1), weight=1)
        title_label = ttk.Label(self, text=title, style='title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, sticky='news')
        PulsOnDataApp.blank_message(self)
        back_button = ttk.Button(self, text='Back', style='back.TButton',
                                 command=lambda: controller.show_frame(StartPage))
        back_button.grid(row=8, column=0, columnspan=2, sticky='news')

    host_directory = ''

    def get_host_dir(self):
        output = str(subprocess.check_output('pwd', shell=True))
        PulsOnDataApp.host_directory = output[2:(len(output)-3)]

    colormaps = 'viridis plasma inferno magma Greys Purples Blues Greens Oranges Reds YlOrBr YlOrRd OrRd PuRd RdPu' \
                ' BuPu GnBu PuBu YlGnBu PuBuGn BuGn YlGn binary gist_yarg gist_gray gray bone pink spring summer' \
                ' autumn winter cool Wistia hot afmhot gist_heat copper Pastel1 Pastel2 Paired Accent Dark2 Set1' \
                ' Set2 Set3 tab10 tab20 tab20b tab20c flag prism ocean gist_earth terrain gist_stern gnuplot gnuplot2' \
                ' CMRmap cubehelix brg hsv gist_rainbow rainbow jet nipy_spectral gist_ncar'


# Opens this page on start
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg=INTERFACE_COLOR)
        self.rowconfigure(0, weight=4)
        self.rowconfigure(4, weight=1)
        self.rowconfigure((1, 2, 3), weight=8)
        self.columnconfigure((0, 1), weight=1)

        # All styles initialized here
        button_style = ttk.Style()
        button_style.configure('default.TButton', foreground=LABEL_COLOR, background=BUTTON_COLOR,
                               font=BODY_FONT, relief='flat')
        button_style.map('default.TButton', background=[('disabled', DISABLED_COLOR),
                                                        ('pressed', BUTTON_CLICK_COLOR),
                                                        ('active', BUTTON_HOVER_COLOR)])
        start_button_style = ttk.Style()
        start_button_style.configure('start_scan.TButton', foreground=LABEL_COLOR, background=BUTTON_COLOR,
                                     font=BODY_FONT, relief='flat')
        start_button_style.map('start_scan.TButton', background=[('disabled', DISABLED_COLOR),
                                                                 ('pressed', SUCCESS_CLICK_COLOR),
                                                                 ('active', SUCCESS_HOVER_COLOR)])
        stop_button_style = ttk.Style()
        stop_button_style.configure('stop_scan.TButton', foreground=LABEL_COLOR, background=BUTTON_COLOR,
                                    font=BODY_FONT, relief='flat')
        stop_button_style.map('stop_scan.TButton', background=[('disabled', DISABLED_COLOR),
                                                               ('pressed', ERROR_CLICK_COLOR),
                                                               ('active', ERROR_HOVER_COLOR)])
        back_button_style = ttk.Style()
        back_button_style.configure('back.TButton', foreground=INTERFACE_COLOR, background=CONTRAST_BUTTON_COLOR,
                                    font=BODY_FONT, relief='flat')
        back_button_style.map('back.TButton', background=[('disabled', 'red'),
                                                          ('pressed', CONTRAST_BUTTON_CLICK_COLOR),
                                                          ('active', CONTRAST_BUTTON_HOVER_COLOR)])
        blended_button_style = ttk.Style()
        blended_button_style.configure('blended.TButton', foreground=CONTRAST_BUTTON_COLOR, background=INTERFACE_COLOR,
                                       font=SMALLER_FONT, relief='flat')
        blended_button_style.map('blended.TButton', foreground=[('disabled', CONTRAST_BUTTON_COLOR),
                                                                ('pressed', CONTRAST_BUTTON_CLICK_COLOR),
                                                                ('active', CONTRAST_BUTTON_HOVER_COLOR)])
        title_label_style = ttk.Style()
        title_label_style.configure('title.TLabel', foreground=TITLE_COLOR, background=TITLE_BACKGROUND,
                                    font=LARGE_FONT, anchor='tk.Center')
        body_label_style = ttk.Style()
        body_label_style.configure('body.TLabel', foreground=LABEL_COLOR, background=INTERFACE_COLOR,
                                   font=SMALLER_FONT, anchor='tk.Center', wraplength=1200)
        progressbar_style = ttk.Style()
        progressbar_style.configure('default.Horizontal.TProgressbar', background=SUCCESS_COLOR, troughcolor=INTERFACE_COLOR)
        entry_style = ttk.Style()
        entry_style.configure('default.TEntry', relief='flat', font=SMALLER_FONT, foreground=LABEL_COLOR)
        combobox_style = ttk.Style()
        combobox_style.configure('default.TCombobox', relief='flat', font=SMALLER_FONT, foreground=LABEL_COLOR)

        title_label = ttk.Label(self, text='PulsON440 Data Center', style='title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, sticky='news')

        PulsOnDataApp.blank_message(self)

        button1 = ttk.Button(self, text='Change Radar\n     Settings', style='default.TButton',
                             command=lambda: controller.show_frame(RadarSettingPage))
        button1.grid(padx=x_pad, pady=y_pad, row=1, column=0, sticky='news')

        button2 = ttk.Button(self, text='Data Collection', style='default.TButton',
                             command=lambda: controller.show_frame(DataCollection))
        button2.grid(padx=x_pad, pady=y_pad, row=1, column=1, sticky='news')

        button3 = ttk.Button(self, text='Unpack Existing', style='default.TButton',
                             command=lambda: controller.show_frame(UnpackExisting))
        button3.grid(padx=x_pad, pady=y_pad, row=2, column=0, sticky='news')

        button4 = ttk.Button(self, text='Back Projection', style='default.TButton',
                             command=lambda: controller.show_frame(BackProjection))
        button4.grid(padx=x_pad, pady=y_pad, row=2, column=1, sticky='news')

        quit_button = ttk.Button(self, text='Quit', style='back.TButton', command=lambda: app.quit())
        quit_button.grid(padx=x_pad, pady=y_pad, row=3, column=0, columnspan=2, sticky='news')

        about_button = ttk.Button(self, text='About App', style='blended.TButton',
                                  command=lambda: controller.show_frame(AboutApp))
        about_button.grid(padx=x_pad, pady=y_pad, row=4, column=0, columnspan=2, sticky='')


# About app; template for help page
class AboutApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        PulsOnDataApp.default_config(self, controller, 'About PulsON440 Data Center')

        body_text = 'The PulsON440 Data Center was created by Nile Camai with help from his more mentally stable team' \
                    'members from UAS-SAR Team 2, "SAR-ry Not Sorry". '
        # ipsum_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas iaculis nisi ut urna pellentesque sollicitudin. Nunc tempor, nibh non posuere ullamcorper, sapien enim convallis lectus, et porta lorem tortor ac libero. Nullam sodales lectus vel felis hendrerit rutrum. Pellentesque convallis lectus risus, vel auctor dui fermentum congue. Proin sodales, est vel hendrerit blandit, magna lorem ullamcorper libero, ac porttitor mauris nisi sit amet magna. Maecenas mollis eros risus, ac egestas ligula fringilla eget. Nam velit urna, dapibus quis ipsum eget, pellentesque facilisis nisi. Quisque vestibulum mi malesuada nisl faucibus imperdiet. Sed nec nisi nisl. Quisque molestie nulla ac lectus imperdiet, non sollicitudin justo rhoncus. Aliquam erat volutpat. Integer a ex erat.\n Sed ut vestibulum elit. Nam augue velit, hendrerit id mollis at, euismod ut libero. Nunc sed mi sapien. Etiam erat leo, ultrices vitae vestibulum et, porttitor quis lorem. Nulla fringilla enim id velit congue efficitur. Vivamus pretium nulla nec est ultricies lobortis non non ipsum. Proin in eros nec tortor placerat dignissim id vel nibh.\n Aliquam ac sapien tempor, dictum ante vel, volutpat odio. Cras vestibulum ipsum in libero aliquet sollicitudin. Aliquam erat volutpat. Mauris sagittis tellus nunc, sit amet imperdiet lorem molestie a. Aenean sed velit non sem pellentesque mollis at sit amet enim. Etiam molestie efficitur neque. Duis ut urna nec sapien malesuada maximus sit amet quis nulla. Curabitur a libero eget lectus mollis pellentesque quis et nisi. Praesent sit amet elit in ante vehicula varius et ac purus. Vestibulum interdum, ex molestie pellentesque eleifend, magna mauris fermentum mi, id condimentum nunc justo et est.\n Nullam quis volutpat nibh. Sed eget auctor augue, vitae interdum sapien. Nulla facilisi. Donec vitae lobortis ipsum. Phasellus tempor augue id faucibus tincidunt. Aliquam orci nibh, ultrices nec tincidunt at, dignissim nec augue. Maecenas placerat arcu id venenatis aliquam. Praesent porttitor elit lacus, ac laoreet turpis dignissim ac. Donec posuere in enim sed porttitor. Nullam at tellus sed dolor sollicitudin pellentesque at eget nulla. Nulla rutrum odio dolor, dignissim mattis sapien dignissim ut. Phasellus nec fermentum lectus. Sed sodales mi eget metus scelerisque, ac blandit dolor iaculis.\n Fusce tempus rhoncus tristique. Sed pretium varius turpis vitae semper. Nulla commodo leo augue, id commodo dui tempor in. Curabitur maximus velit nunc, vel facilisis nisi tempor sit amet. Aliquam malesuada fringilla nisl, a maximus purus ornare sed. Maecenas et eros et magna congue tempor vel ac lectus. Praesent tristique, leo nec lobortis mattis, mauris mauris ultrices magna, a dictum nulla ante a sapien. '
        body_label = ttk.Label(self, text=body_text, style='body.TLabel')
        body_label.grid(row=2, column=0, columnspan=2)


# User entry boxes to change radar scan settings
class RadarSettingPage(tk.Frame):

    def pass_back(self):
        scp2 = "sshpass -p 'TimHoward' scp pi@192.168.2.1:nile_bad_idea/pulsonapplib/radar_settings " + PulsOnDataApp.host_directory + "/pulsonapplib/temp "
        subprocess.Popen(scp2.encode('UTF-8'), shell=True)

    def push_to(self):
        scp = "sshpass -p 'TimHoward' scp " + PulsOnDataApp.host_directory + "/pulsonapplib/radar_settings pi@192.168.2.1:nile_bad_idea/pulsonapplib/radar_settings "
        subprocess.Popen(scp.encode('UTF-8'), shell=True)

    def is_the_same(self):
        return filecmp.cmp('./pulsonapplib/temp/radar_settings', './pulsonapplib/radar_settings')

    def write_duplicate(self):
        read_file = open('./pulsonapplib/radar_settings', 'r').read()
        duplicate_file = open('./pulsonapplib/temp/duplicate_radar_settings', 'w')
        duplicate_file.write(read_file)
        duplicate_file.close()

    # Takes user input and writes to radar_settings
    def fetch_entries(self, a, b, c, d, e, f):
        try:
            dT_0 = str(a.get())
            range_start = str(b.get())
            range_stop = str(c.get())
            tx_gain_ind = str(d.get())
            pii = str(e.get())
            code_channel = str(f.get())

            range_error = False
            if float(b.get()) < 0 or float(c.get()) < 0 or int(d.get()) > 63 or int(d.get()) < 0 or int(e.get()) > 15 or int(e.get()) < 6 or float(b.get() > float(c.get())):
                range_error = True

            print([dT_0, range_start, range_stop, tx_gain_ind, pii, code_channel])

            self.write_duplicate()
            settings = open('./pulsonapplib/radar_parse_settings', 'r').read()
            settings = settings.replace('$dT_0$', dT_0)
            settings = settings.replace('$range_start$', range_start)
            settings = settings.replace('$range_stop$', range_stop)
            settings = settings.replace('$tx_gain_ind$', tx_gain_ind)
            settings = settings.replace('$pii$', pii)
            settings = settings.replace('$code_channel$', code_channel)
            file = open('./pulsonapplib/radar_settings', 'w')
            file.write(settings)
            file.close()

            self.push_to()

            PulsOnDataApp.clear_message(self)

            self.pass_back()

            iteration = 0
            while True:
                if self.is_the_same():
                    if filecmp.cmp('./pulsonapplib/temp/duplicate_radar_settings', './pulsonapplib/radar_settings'):
                        if range_error:
                            PulsOnDataApp.show_error_message(self, 'WTF are you doing, multiple errors')
                            break
                        PulsOnDataApp.show_error_message(self,
                                                         'Rewrite ignored: radar settings are the same or one or more entries are of the incorrect type ')
                        break
                    elif range_error:
                        PulsOnDataApp.show_error_message(self, 'Wrote settings to radar. WARNING: one or more entries out of acceptable range')
                        break
                    else:
                        PulsOnDataApp.clear_message(self)
                        PulsOnDataApp.show_success_message(self, 'Successfully wrote settings to radar! No issues detected.')
                        break
                else:
                    # Shell ping-pongs between radar settings and temporary settings file every 0.25s until they match
                    iteration += 1
                    self.push_to()
                    time.sleep(0.25)
                    self.pass_back()
                    print('Ping-pong iteration #' + str(iteration))
                    # Tries 20 iterations * 0.25s = 20s max waiting time before error raised
                    if iteration >= 20:
                        PulsOnDataApp.show_error_message(self, 'Did not successfully write settings to radar, check connection. ')
                        break
        except:
            PulsOnDataApp.show_error_message(self, 'You are bad, please enter numbers. ')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        PulsOnDataApp.default_config(self, controller, 'Change Radar Settings')

        self.write_duplicate()

        path_delay_label = ttk.Label(self, text='Path Delay Through Antennae (ns)', style='body.TLabel')
        path_delay_label.grid(row=2, column=0, padx=x_pad, pady=y_pad, sticky='nes')
        path_delay_entry = tk.DoubleVar()
        path_delay_entry.set(10)
        path_delay_entry_box = ttk.Entry(self, textvariable=path_delay_entry, style='default.TEntry', font=SMALLER_FONT)
        path_delay_entry_box.grid(row=2, column=1, padx=x_pad, pady=y_pad, sticky='nws')

        range_start_label = ttk.Label(self, text='Range Start (m)', style='body.TLabel')
        range_start_label.grid(row=3, column=0, padx=x_pad, pady=y_pad, sticky='nes')
        range_start_entry = tk.DoubleVar()
        range_start_entry.set(3)
        range_start_entry_box = ttk.Entry(self, textvariable=range_start_entry, style='default.TEntry', font=SMALLER_FONT)
        range_start_entry_box.grid(row=3, column=1, padx=x_pad, pady=y_pad, sticky='nws')

        range_end_label = ttk.Label(self, text='Range End (m)', style='body.TLabel')
        range_end_label.grid(row=4, column=0, padx=x_pad, pady=y_pad, sticky='nes')
        range_end_entry = tk.DoubleVar()
        range_end_entry.set(15)
        range_end_entry_box = ttk.Entry(self, textvariable=range_end_entry, style='default.TEntry', font=SMALLER_FONT)
        range_end_entry_box.grid(row=4, column=1, padx=x_pad, pady=y_pad, sticky='nws')

        transmit_gain_label = ttk.Label(self, text='Transmit Gain Index', style='body.TLabel')
        transmit_gain_label.grid(row=5, column=0, padx=x_pad, pady=y_pad, sticky='nes')
        transmit_gain_entry = tk.IntVar()
        transmit_gain_entry.set(60)
        transmit_gain_entry_box = ttk.Entry(self, textvariable=transmit_gain_entry, style='default.TEntry', font=SMALLER_FONT)
        transmit_gain_entry_box.grid(row=5, column=1, padx=x_pad, pady=y_pad, sticky='nws')

        pii_label = ttk.Label(self, text='Pulse Integration Index', style='body.TLabel')
        pii_label.grid(row=6, column=0, padx=x_pad, pady=y_pad, sticky='nes')
        pii_entry = tk.IntVar()
        pii_entry.set(11)
        pii_entry_box = ttk.Entry(self, textvariable=pii_entry, style='default.TEntry', font=SMALLER_FONT)
        pii_entry_box.grid(row=6, column=1, padx=x_pad, pady=y_pad, sticky='nws')

        code_channel_label = ttk.Label(self, text='Code Channel', style='body.TLabel')
        # code_channel_label.grid(row=7, column=0, padx=x_pad, pady=y_pad, sticky='nes')
        code_channel_entry = tk.IntVar()
        code_channel_entry.set(0)
        code_channel_entry_box = ttk.Entry(self, textvariable=code_channel_entry, style='default.TEntry', font=SMALLER_FONT)
        # code_channel_entry_box.grid(row=7, column=1, padx=x_pad, pady=y_pad, sticky='nws')

        submit_button = ttk.Button(self, text='SUBMIT', style='default.TButton',
                                   command=lambda: self.fetch_entries(path_delay_entry, range_start_entry,
                                                                      range_end_entry,  transmit_gain_entry, pii_entry,
                                                                      code_channel_entry))
        submit_button.grid(row=7, column=0, columnspan=2)


# Start and stop scanning and prompt user to save scan data
class DataCollection(tk.Frame):

    def start(self, v, enabled_button, disabled_button):
        run_type = '-' + str(v.get())
        print(run_type)
        shoot_pulses = "python control.py " + run_type + " &"
        if run_type == '-q' or run_type == '-c':
            cmds1 = ("sshpass -p 'TimHoward' ssh pi@192.168.2.1", "cd nile_bad_idea/pulsonapplib",
                     "python control.py " + run_type + " &")

            process1 = subprocess.Popen('/bin/bash', stdin=PIPE, shell=True)

            for cmd in cmds1:
                command = cmd + '\n'
                process1.stdin.write(command.encode(encoding='UTF-8'))
            process1.stdin.close()
            print(str(subprocess.check_output('cat status', shell=True)))
            enabled_button.config(state='disabled')
            disabled_button.config(state='enabled')
            PulsOnDataApp.blank_message(self)
        else:
            PulsOnDataApp.show_error_message(self, 'Please specify a run type. ')

    pulse_data_file_directory = r'../UAV-SAR-Radar/pulsonapplib/temp/untitled_data0'

    def save_binary_file(self, file_at_directory):
        file = filedialog.asksaveasfile(title="Save binary file as", initialdir='../UAV-SAR-Radar',
                                        filetypes=[('binary files', '*'), ('all files', '*.')], mode='wb')
        f = open(file_at_directory, 'rb')
        contents = f.read()
        file.write(contents)

    def stop(self, disabled_button, enabled_button):
        cmds2 = ("sshpass -p 'TimHoward' ssh pi@192.168.2.1", "cd nile_bad_idea/pulsonapplib",
                 "echo 1 > control", "logout")

        process2 = subprocess.Popen('/bin/bash', stdin=PIPE)

        for cmd in cmds2:
            command = cmd + '\n'
            process2.stdin.write(command.encode(encoding='UTF-8'))
        process2.stdin.close()

        print(PulsOnDataApp.host_directory)
        scp = "sshpass -p 'TimHoward' scp pi@192.168.2.1:nile_bad_idea/pulsonapplib/temp/untitled_data0 " + PulsOnDataApp.host_directory + "/pulsonapplib/temp"
        subprocess.Popen(scp.encode('UTF-8'), shell=True)
        time.sleep(6)
        try:
            self.save_binary_file(self.pulse_data_file_directory)
        except:
            PulsOnDataApp.show_error_message(self, 'Did not specify a save directory. Aborting')
        enabled_button.config(state='disabled')
        disabled_button.config(state='enabled')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        PulsOnDataApp.default_config(self, controller, 'Data Collection')

        PulsOnDataApp.get_host_dir(self)

        radio_button_frame = tk.Frame(self)
        radio_button_frame.configure(bg=INTERFACE_COLOR)
        radio_button_frame.rowconfigure((0, 1), weight=1)
        radio_button_frame.columnconfigure((0), weight=1)
        radio_button_frame.grid(row=3, column=0, rowspan=4, sticky='news')

        MODES = [
            ("Quick Scan", "q", 0),
            ("Collect", "c", 1),
        ]

        v = tk.StringVar()
        # v.set("c")  # initialize
        for text, mode, this_row in MODES:
            b = tk.Radiobutton(radio_button_frame, text=text,
                               variable=v, value=mode, indicatoron=0, selectcolor=SUCCESS_COLOR, overrelief='flat')
            b.configure(bg=BUTTON_COLOR, foreground=LABEL_COLOR, font=BODY_FONT)
            b.grid(row=this_row, padx=x_pad, sticky='news')

        start_button = ttk.Button(self, text='START SCAN', style='start_scan.TButton',
                                  command=lambda: self.start(v, start_button, stop_button))
        start_button.grid(row=3, column=1, rowspan=2, padx=x_pad, sticky='news')
        start_button.config(state='enabled')
        stop_button = ttk.Button(self, text='STOP SCAN', style='stop_scan.TButton',
                                 command=lambda: self.stop(start_button, stop_button))
        stop_button.grid(row=5, column=1, rowspan=2, padx=x_pad, sticky='news')
        stop_button.config(state='disabled')


# Unpack scans vs range
class UnpackExisting(tk.Frame):

    def get_unpack_binary_file(self):
        data_file_directory = filedialog.askopenfilename(initialdir="../UAV-SAR-Radar", title="Select pulse array file",
                                                         filetypes=(("binary files", "*"),
                                                                    ("comma-separated values", "*.csv")))
        return data_file_directory

    directory = None
    filename = None
    args_string = None

    def assign_directory(self, frame):
        self.directory = self.get_unpack_binary_file()
        if self.directory == ():
            return
        # backslashed_directory = ''
        index = 0
        for f in range(0, len(self.directory)):
            if self.directory[f] == '/':
                index = f + 1
            """ #  backslashed directory not necessary with Linux
            if self.directory[f] == ' ':
                backslashed_directory = backslashed_directory + '\ '
            else:
                backslashed_directory = backslashed_directory + self.directory[f]
            """

        self.filename = self.directory[(index):]

        pulse_data_file_label = ttk.Label(frame, text='', style='body.TLabel')
        pulse_data_file_label.grid(row=0, column=1, columnspan=2, sticky='news', padx=x_pad, pady=y_pad)

        pulse_data_file_label = ttk.Label(frame, text='File Selected: ' + self.filename + '\n (' + self.directory + ')',
                                          style='body.TLabel')
        pulse_data_file_label.grid(row=0, column=1, columnspan=2, sticky='news', padx=x_pad, pady=y_pad)

    def graph_unpack(self, data_file, pickle_it):
        pickle_dir_string = None
        try:
            if pickle_it:
                pickle_directory = filedialog.asksaveasfile(title="Save pickle file as", initialdir='../UAV-SAR-Radar',
                                                filetypes=[('Pickle files', '*.pkl'), ('all files', '*.')], mode='wb')
                pickle_dir_string = str(pickle_directory)
                start_index = None
                for i in range(0, len(pickle_dir_string)):
                    if pickle_dir_string[i] == "'" and start_index is None:
                        start_index = i + 1
                    elif pickle_dir_string[i] == "'":
                        end_index = i
                pickle_dir_string = pickle_dir_string[start_index: end_index]
            PulsOnDataApp.blank_message(self)
            unpack.main(self.directory, pickle_dir_string)

            # Draws graph on window
            canvas = FigureCanvasTkAgg(unpack.f, self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=5, column=0, rowspan=2, columnspan=2)

            # Navigation tools
            toolbar_frame = tk.Frame(self)
            toolbar_frame.grid(row=6, column=0, columnspan=2, sticky='s')
            toolbar = NavigationToolbar2TkAgg(canvas, toolbar_frame)
            toolbar.update()
        except:
            if pickle_dir_string is None:
                PulsOnDataApp.show_error_message(self, 'Please select a valid file.')

    def fetch_colormap_name(self, a):
        try:
            unpack.colormap_name = str(a.get())
        except:
            PulsOnDataApp.show_error_message(self, 'Please select a valid colormap.')

    def do_both(self, data_file, a, b):
        self.fetch_colormap_name(a)
        self.graph_unpack(data_file, b)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        PulsOnDataApp.default_config(self, controller, 'Unpack Existing')

        control_bar = tk.Frame(self)
        control_bar.configure(bg=INTERFACE_COLOR)
        control_bar.grid(row=2, column=0, columnspan=2)
        control_bar.rowconfigure((0, 1), weight=1)
        control_bar.columnconfigure((0, 1, 2, 3), weight=1)

        settings_bar = tk.Frame(control_bar)
        settings_bar.configure(bg=INTERFACE_COLOR)
        settings_bar.grid(row=1, column=1, columnspan=2)
        settings_bar.rowconfigure((0), weight=1)
        settings_bar.columnconfigure((0, 1, 2), weight=1)

        # Select pulse code directory
        pulse_data_file_button = ttk.Button(control_bar, text='Select Data File...', style='default.TButton',
                                            command=lambda: self.assign_directory(control_bar))
        pulse_data_file_button.grid(row=0, column=0, rowspan=2, sticky='news', padx=x_pad, pady=y_pad)

        # Display string as label
        pulse_data_unpack_button = ttk.Button(control_bar, text='Unpack!', style='default.TButton',
                                              command=lambda: self.do_both(self.directory,
                                                                           colormap_name_entry, pickle_checkbox_entry.get()))
        pulse_data_unpack_button.grid(row=0, column=3, rowspan=2, padx=x_pad, pady=y_pad, sticky='news')

        pickle_checkbox_entry = tk.BooleanVar()
        pickle_checkbox_entry.set(False)
        pickle_checkbox = tk.Checkbutton(settings_bar, text='Pickle my file', font=SMALLER_FONT, bg=BUTTON_COLOR,
                                         fg=LABEL_COLOR, indicatoron=0, selectcolor=SUCCESS_COLOR,
                                         overrelief='flat', variable=pickle_checkbox_entry)
        pickle_checkbox.grid(row=0, column=2, padx=x_pad, pady=y_pad, sticky='news')

        colormap_name_label = ttk.Label(settings_bar, text='Select a colormap:', style='body.TLabel')
        colormap_name_label.grid(row=0, column=0, padx=x_pad, pady=y_pad, sticky='news')
        colormap_name_entry = tk.StringVar()
        colormap_name_entry.set('viridis')
        colormap_name_entry_box = ttk.Combobox(settings_bar, textvariable=colormap_name_entry, font=SMALLER_FONT,
                                               values=PulsOnDataApp.colormaps)
        colormap_name_entry_box.grid(row=0, column=1, padx=x_pad, pady=y_pad, sticky='news')


# Create a SAR image with a pickle file
class BackProjection(tk.Frame):

    def get_bproj_pkl(self):
        data_file_directory = filedialog.askopenfilename(initialdir="../UAV-SAR-Radar", title="Select pickled data",
                                                         filetypes=(("pickle files", "*.pkl"),
                                                                    ("comma-separated values", "*.csv")))
        return data_file_directory

    directory = None
    filename = None
    args_string = None

    def assign_directory(self, frame):
        self.directory = self.get_bproj_pkl()
        if self.directory == ():
            return
        # backslashed_directory = ''
        index = 0
        for f in range(0, len(self.directory)):
            if self.directory[f] == '/':
                index = f + 1
            """ # backslashed directory not necessary with Linux
            if self.directory[f] == ' ':
                backslashed_directory = backslashed_directory + '\ '
            else:
                backslashed_directory = backslashed_directory + self.directory[f]
            """

        self.filename = self.directory[index:]

        pulse_data_file_label = ttk.Label(frame, text='', style='body.TLabel')
        pulse_data_file_label.grid(row=0, column=1, columnspan=2, sticky='news', padx=x_pad, pady=y_pad)
        pulse_data_file_label = ttk.Label(frame, text='File Selected: ' + self.filename + '\n (' +
                                          self.directory + ')', style='body.TLabel')
        pulse_data_file_label.grid(row=0, column=1, columnspan=2, sticky='news', padx=x_pad, pady=y_pad)

    def run_progress_bar(self):
        time.sleep(0.2)
        print(sar.ProgressValues.is_running)
        self.sar_progress_bar['maximum'] = sar.ProgressValues.total_length - 2  # buffer because image renders too fast
        while sar.ProgressValues.is_running:
            time.sleep(0.05)
            self.sar_progress_bar['value'] = sar.ProgressValues.iteration
            self.sar_progress_bar.update()
            self.pulse_data_bproj_button.config(state='disabled')

    def graph_bproj(self, file, size, pixels, mode):
        try:
            PulsOnDataApp.blank_message(self)
            s = size.get()
            p = pixels.get()
            m = mode.get()
            if file is None:
                PulsOnDataApp.show_error_message(self, 'Please select a valid file.')
                return
            pixel_resolution_ceiling = 500
            if m is True:
                pixel_resolution_ceiling = 150

            if p > pixel_resolution_ceiling:
                if not messagebox.askokcancel("Pixel Resolution Warning", 'The selected pixel resolution, ' + str(p) +
                                              ', is higher than the recommended pixel resolution for this setting, ' +
                                              str(pixel_resolution_ceiling) + '. Continue back projection?'):
                    PulsOnDataApp.show_error_message(self, 'Cancelled back projection.')
                    return

            sar_thread = threading.Thread(target=sar.main, args=(file, s, p, m))
            sar_thread.start()
            sar_progress_bar_control_var = tk.IntVar()
            sar_progress_bar_control_var.set(sar.ProgressValues.iteration)

            time.sleep(0.5)

            self.sar_progress_bar = ttk.Progressbar(self, length=100, mode='determinate',
                                                    style='default.Horizontal.TProgressbar')
            self.sar_progress_bar.grid(row=1, column=0, columnspan=2, sticky='news', padx=50)
            self.run_progress_bar()
            self.pulse_data_bproj_button.config(state='enabled')

            # Draws graph on window
            canvas = FigureCanvasTkAgg(sar.fluffy, self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=5, column=0, rowspan=2, columnspan=2)

            # Navigation tools
            toolbar_frame = tk.Frame(self)
            toolbar_frame.grid(row=6, column=0, columnspan=2, sticky='s')
            toolbar = NavigationToolbar2TkAgg(canvas, toolbar_frame)
            toolbar.update()
        except:
            PulsOnDataApp.show_error_message(self, 'An unknown error occurred.')

    def fetch_colormap_name(self, a):
        try:
            sar.colormap_name = str(a.get())
        except:
            PulsOnDataApp.show_error_message(self, 'Please select a valid colormap.')

    def do_both(self, data_file, size, pixels, mode, a):
        self.fetch_colormap_name(a)
        self.graph_bproj(data_file, size, pixels, mode)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        PulsOnDataApp.default_config(self, controller, 'Back Projection')

        control_bar = tk.Frame(self)
        control_bar.configure(bg=INTERFACE_COLOR)
        control_bar.grid(row=2, column=0, columnspan=2)
        control_bar.rowconfigure((0, 1), weight=1)
        control_bar.columnconfigure((0, 1, 2, 3), weight=1)

        settings_bar = tk.Frame(control_bar)
        settings_bar.configure(bg=INTERFACE_COLOR)
        settings_bar.grid(row=1, column=1, columnspan=2)
        settings_bar.rowconfigure((0, 1), weight=1)
        settings_bar.columnconfigure((0, 1, 2, 3), weight=1)

        # Select pulse code directory
        pulse_data_file_button = ttk.Button(control_bar, text='Select Data File...', style='default.TButton',
                                            command=lambda: self.assign_directory(control_bar))
        pulse_data_file_button.grid(row=0, column=0, rowspan=2, sticky='news', padx=x_pad, pady=y_pad)

        # Display string as label
        self.pulse_data_bproj_button = ttk.Button(control_bar, text='Generate Image!', style='default.TButton',
                                                  command=lambda: self.do_both(self.directory, bproj_size_entry,
                                                  bproj_pixels_entry, fourier_checkbox_entry, colormap_name_entry))
        self.pulse_data_bproj_button.grid(row=0, column=3, rowspan=2, padx=x_pad, pady=y_pad, sticky='news')

        fourier_checkbox_entry = tk.BooleanVar()
        fourier_checkbox_entry.set(False)
        fourier_checkbox = tk.Checkbutton(settings_bar, text='Fourier', variable=fourier_checkbox_entry,
                                          font=SMALLER_FONT, bg=BUTTON_COLOR, fg=LABEL_COLOR, indicatoron=0,
                                          selectcolor=SUCCESS_COLOR, overrelief='flat')
        fourier_checkbox.grid(row=0, column=2, columnspan=2, padx=x_pad, pady=y_pad, sticky='news')

        bproj_size_label = ttk.Label(settings_bar, text='Size:', style='body.TLabel')
        bproj_size_label.grid(row=0, column=0, padx=x_pad, pady=y_pad, sticky='news')
        bproj_size_entry = tk.DoubleVar()
        bproj_size_entry.set(5.0)
        bproj_size_entry_box = ttk.Entry(settings_bar, textvariable=bproj_size_entry, style='default.TEntry', font=SMALLER_FONT)
        bproj_size_entry_box.grid(row=0, column=1, padx=x_pad, pady=y_pad, sticky='news')
        bproj_pixels_label = ttk.Label(settings_bar, text='Pixels:', style='body.TLabel')
        bproj_pixels_label.grid(row=1, column=0, padx=x_pad, pady=y_pad, sticky='news')
        bproj_pixels_entry = tk.IntVar()
        bproj_pixels_entry.set(250)
        bproj_pixels_entry_box = ttk.Entry(settings_bar, textvariable=bproj_pixels_entry, style='default.TEntry', font=SMALLER_FONT)
        bproj_pixels_entry_box.grid(row=1, column=1, padx=x_pad, pady=y_pad, sticky='news')

        colormap_name_label = ttk.Label(settings_bar, text='Select a colormap:', style='body.TLabel')
        colormap_name_label.grid(row=1, column=2, padx=x_pad, pady=y_pad, sticky='news')
        colormap_name_entry = tk.StringVar()
        colormap_name_entry.set('viridis')
        colormap_name_entry_box = ttk.Combobox(settings_bar, textvariable=colormap_name_entry, font=SMALLER_FONT,
                                               values=PulsOnDataApp.colormaps)
        colormap_name_entry_box.grid(row=1, column=3, padx=x_pad, pady=y_pad, sticky='news')


app = PulsOnDataApp()
app.geometry('1920x1080')
app.mainloop()
