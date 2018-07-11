# -*- coding: utf-8 -*-
"""
PulsON 440 radar command and control class.
"""

# Import the required modules
# TIP Numpy will be very useful in converting received data into desired types.
import math
import numpy as np
import socket
from constants import SPEED_OF_LIGHT, MAX_PACKET_SIZE, CONTINUOUS_SCAN, \
    STOP_SCAN, DT_MIN, T_BIN, DN_BIN, SEG_NUM_BINS

# Communication protocol constants
MESSAGE_ID = "\x00\x01" # Message ID; static since only 1 radar is presumed

# Radar messages types; refer to API for details
# !!!

# Specific recommended radar configurations
REC_SCAN_RES = 32 # Scan resolution (bins)
REC_ANTENNA_MODE = 2 # Transmit/receive configuration of antennas
REC_PERSIST_FLAG = 1 # Configuration persistence flag

# Default user settings
# !!!
DT_0 = 10 # Path delay through antennas (ns)

# Status and control
# TIP A control and status files are recommended to provide traceability
CONTROL_FILE_NAME = "control"
STATUS_FILE_NAME = "status"

class PulsON440:
    """
    Class for command and control of PulsON 440 radar.
    TIP Use of a class is not required; this can all be done in script.
    TIP The host is the Raspberry Pi and the radar is the radar.
    """
    
    def __init__(self, udp_ip_host="192.168.1.1", udp_ip_radar="192.168.1.100", 
                 udp_port=21210):
        """
        Instance initialization.
        TIP You should include attributes to cover all settings, configurations, 
        status, and handles you want to use.
        TIP Check and assign defaults as you see fit.
        """
        # !!!
        self.udp_ip_host = udp_ip_host
        self.udp_ip_radar = udp_ip_radar
        self.udp_port = udp_port
        self.sock = []
        
    def connect(self):
        """
        Connect to radar and set up control and status files.
        TIP After connecting, update any needed status and control files/flags 
        to monitor how radar operation.
        """
        # Try to connect to radar
        # TIP Based on the UDP protocol, this is the recommended connection 
        # process
        try:
            self.sock = socket.socket(socket.AF_INET, 
                           socket.SOCK_DGRAM)
            self.sock.setblocking(False)
            self.sock.bind((self.udp_ip_host, self.udp_port))
        except:
            print("Failed to connect to radar!\n")
            exit()
        
    def read_config_file(self, config_file="radar_settings.cfg"):
        """
        Read user specified radar configuration file.
        TIP Recommend that your configuration file format readable and editable
        from a terminal.
        """
        # !!!
        
    def settings_to_config(self):
        """
        Translate user settings into radar configuration.
        TIP Whatever radar configuration settings you expose to the user via, 
        higher level abstractions, e.g., scan start via a start range, be sure
        to parse and validate them.
        """
        # !!!
        # TIP This section of code converts your derived scan start and stop
        # to a integer multiple of the radar's timing resolution
        N_bin = (scan_stop - scan_start) / T_BIN
        N_bin = DN_BIN * math.ceil(N_bin / DN_BIN)
        scan_start = math.floor(1000 * DT_MIN * 
                                math.floor(scan_start / DT_MIN))
        scan_stop = N_bin * T_BIN + scan_start / 1000
        scan_stop = math.floor(1000 * DT_MIN * 
                               math.ceil(scan_stop / DT_MIN))
        
    def get_radar_config(self):
        """
        Get configuration from radar.
        TIP Make sure you parse the received configuration in byte format into 
        a numeric format for inspection and validation.
        """
        # !!!
        
        # TIP This is how to receive data from the radar; the MAX_PACKET_SIZE 
        # is the recommended data packet size. You will need to parse data into
        # the fields and types you need.
        data, addr = self.sock.recvfrom(MAX_PACKET_SIZE)
        
    def set_radar_config(self):
        """
        Set radar configuration based on user settings.
        TIP Make sure you convert your configuration into a byte/character 
        format for proper passing to the radar.
        """
        # !!!
        
    def send_scan_request(self, scan_count):
        """
        Send scan request to radar.
        TIP The constants CONTINUOUS_SCAN and STOP_SCAN will help you control
        these requests.
        """
        # !!!
        
    def config_value_to_message(self, config_value, num_bytes):
        """
        Converts a integer configuration value to a message compatible byte 
        (character) format to be appended to set configuration request.
        TIP A helper function 
        """
        # !!!
        
    def save_radar_data(self, radar_scan_data, save_file_name=''):
        """
        Save radar scan data to file.
        TIP You should include information about the radar's configuration 
        while it was collecting this data for later reference/use.
        """
        # !!!
        
    def quick_look(self, save_file_name=''):
        """
        Executes quick-look with radar to confirm desired operation.
        TIP Your quick-look should provide you enough data to confirm that your
        radar is functional and your settings meet your expectations.
        TIP Be sure to use MRM_SCAN_INFO to retrieve the data from the radar.
        TIP If you choose to save the data, determine a format which you can
        unpack later.
        """
        # !!!
        
    def collect(self, save_file_name=''):
        """
        Collects radar data continuously until commanded to stop.
        TIP Be sure to use MRM_SCAN_INFO to retrieve the data from the radar.
        TIP If you choose to save the data, determine a format which you can
        unpack later.
        TIP Be sure to include some sort of interrupt mechanism to properly 
        stop the from radar scanning/collecting.
        """
        # !!!
        