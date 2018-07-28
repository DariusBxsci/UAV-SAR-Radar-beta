# -*- coding: utf-8 -*-
"""
PulsON 440 radar command and control class.
"""

# Import the required modules
import os
import time
import math
import socket
import datetime
from formats import CONFIG_MSG_FORMAT
from constants import SPEED_OF_LIGHT, MAX_PACKET_SIZE, \
    CONTINUOUS_SCAN, STOP_SCAN, DT_MIN, T_BIN, DN_BIN, SEG_NUM_BINS

running = False

# Communication protocol constants
MESSAGE_ID = "\x00\x01" # Message ID; static since only 1 radar is presumed

# Radar messages types; refer to API for details
MRM_SET_CONFIG_REQUEST = '\x10\x01'
MRM_SET_CONFIG_CONFIRM = '\x11\x01'
MRM_GET_CONFIG_REQUEST = '\x10\x02'
MRM_GET_CONFIG_CONFIRM = '\x11\x02'
MRM_CONTROL_REQUEST = '\x10\x03'
MRM_CONTROL_CONFIRM = '\x11\x03'
MRM_REBOOT_REQUEST = '\xF0\x02'
MRM_REBOOT_CONFIRM = '\xF1\x02'
MRM_SCAN_INFO = '\xF2\x01'

# Specific recommended radar configurations
REC_SCAN_RES = 32 # Scan resolution (bins)
REC_ANTENNA_MODE = 2 # Transmit/receive configuration of antennas
RESERVED = 0 # Value for reserved fields

# Quick-look settings
QUICK_LOOK_NUM_SCANS = 500

# Streaming data settings
STREAM_TIMEOUT = 5 # Time (s) to read residual streaming data before dropping scans

# Default user settings
DT_0 = 10 # Path delay through antennas (ns)
RANGE_START = 4 # (m)
RANGE_STOP = 14.5 # (m)
TX_GAIN_IND = 63 # 0 -> 63
PII = 11 # Pulse integration index, 6 -> 15
CODE_CHANNEL = 0 # 0 -> 10
NODE_ID = 1 # 1 -> 2^32 - 2
PERSIST_FLAG = 1 # {0, 1}

# Status and control
CONTROL_FILE_NAME = "control"
STATUS_FILE_NAME = "status"

class PulsON440:
    """
    Class for command and control of PulsON 440 radar.
    """
    
    def __init__(self, udp_ip_host="192.168.1.1", udp_ip_radar="192.168.1.100", 
                 udp_port=21210, verbose=False):
        """
        Instance initialization.
        """
        # Radar status indicators
        self.connected = False
        self.collecting = False
        
        # Radar system parameters
        self.N_bin = [] # Number of bins in scan
        
        # Connection settings
        self.connection = {
                'udp_ip_host': udp_ip_host, # Host (computer) IP address
                'udp_ip_radar': udp_ip_radar, # Radar IP address
                'udp_port': udp_port, # Radar port
                'sock': []} # UDP socket
        
        # User radar settings; partially higher abstraction than the radar's
        # internal configuration; initialize to defaults; bounds are inclusive
        self.settings = {
                'dT_0': # Path delay through antennas (ns)
                    {'value': DT_0, 'bounds': (0, float("inf"))}, 
                'range_start': # Start range (m)
                    {'value': RANGE_START, 'bounds':(0, float("inf"))},
                'range_stop': # Stop range (m)
                    {'value': RANGE_STOP, 'bounds': (0, float("inf"))},
                'tx_gain_ind': # Transmit gain index
                    {'value': TX_GAIN_IND, 'bounds': (0, 63)},
                'pii': # Pulse integration index
                    {'value': PII, 'bounds': (6, 15)},
                'code_channel': # Code channel
                    {'value': CODE_CHANNEL, 'bounds': (0, 10)},
                'node_id': # Node ID
                    {'value': NODE_ID, 'bounds': (1, 2**32 - 2)},
                'persist_flag': # Persist flag
                    {'value': PERSIST_FLAG, 'bounds': (0, 1)}}
        
        # Radar internal configuration
        self.config = dict.fromkeys(CONFIG_MSG_FORMAT.keys())
        
        # Control and status file handles
        self.status_file = open(STATUS_FILE_NAME, "w")
        self.control_file = []
        
        # Miscellaneous
        self.verbose = verbose
                
    def update_status(self, message):
        """
        Add update to status file and print to command line if specified.
        """
        message = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
                   " - " + message + "\n")
        self.status_file.write(message)
        self.status_file.flush()
        if self.verbose:
            print(message[:-1])
            
    def value_to_message(self, value, num_bytes):
        """
        Converts a integer configuration value to a message compatible byte 
        (character) format to be appended to set configuration request.
        """
        num_nibbles = 2 * num_bytes
        hex_rep = hex(int(value))
        hex_rep = ('0' * (num_nibbles - len(hex_rep[2:])) + hex_rep[2:])
        message = ''
        for ii in range(0, num_nibbles, 2):
            message += chr(int(hex_rep[ii:(ii + 2)], 16))
        return message
            
    def read_settings_file(self, settings_file="radar_settings"):
        """
        Read user specified radar settings file.
        """
        self.update_status("Reading user settings file...")
        with open(settings_file, "r") as f:
            settings_data = f.readlines()
            
        # Iterate over each user setting and check bounds if applicable
        setting_status = 'Successfully read user configuration file!\n'
        for data_line in settings_data:
            data_line = "".join(data_line.split())
            if len(data_line) != 0:
                if data_line[0] != "#":
                    [setting, value] = data_line.split('=')
                    value = float(value)
                    if setting in self.settings.keys():
                        if self.settings[setting]['bounds'] is not None:
                            bounds = self.settings[setting]['bounds']
                            if not (bounds[0] <= value <= bounds[1]):
                                self.update_status("User setting %s is out " + 
                                                   ("of bounds" % setting))
                                exit()
                        self.settings[setting]['value'] = value
                        setting_status += '\t%s: %f\n' % (setting, value)
                    else:
                        pass

        # Update radar configuration
        self.update_status(setting_status[:-1])
        self.settings_to_config()

    def settings_to_config(self):
        """
        Translate user settings into radar configuration.
        """
        # Based on the specified start and stop ranges determine the scan start
        # and stop times
        scan_start = (2 * float(self.settings['range_start']['value']) /
                      (SPEED_OF_LIGHT / 1e9) + self.settings['dT_0']['value'])
        scan_stop = (2 * float(self.settings['range_stop']['value']) /
                     (SPEED_OF_LIGHT / 1e9) + self.settings['dT_0']['value'])
        N_bin = (scan_stop - scan_start) / T_BIN
        N_bin = DN_BIN * math.ceil(N_bin / DN_BIN)
        scan_start = math.floor(1000 * DT_MIN *
                                math.floor(scan_start / DT_MIN))
        scan_stop = N_bin * T_BIN + scan_start / 1000
        scan_stop = math.floor(1000 * DT_MIN *
                               math.ceil(scan_stop / DT_MIN))

        # Update radar configuration
        self.N_bin = N_bin
        self.config['scan_start'] = scan_start
        self.config['scan_stop'] = scan_stop
        self.config['pii'] = self.settings['pii']['value']
        self.config['tx_gain_ind'] = self.settings['tx_gain_ind']['value']
        self.config['code_channel'] = self.settings['code_channel']['value']
        self.config['node_id'] = self.settings['node_id']['value']
        self.config['persist_flag'] = self.settings['persist_flag']['value']

    def connect(self):
        """
        Connect to radar and set up control and status files.
        """
        # Try to connect to radar
        self.update_status("Trying to connect to radar...")
        try:
            self.connection['sock'] = socket.socket(socket.AF_INET,
                           socket.SOCK_DGRAM)
            self.connection['sock'].setblocking(False)
            self.connection['sock'].bind((self.connection['udp_ip_host'],
                            self.connection['udp_port']))
            self.connected = True
        except:
            self.update_status("Failed to connect to radar!")
            self.status_file.close()
            exit()

        # Set up the control file; 0 -> continue, 1 -> stop
        self.control_file = open(CONTROL_FILE_NAME, "w")
        self.control_file.write("0")
        self.control_file.close()
        self.control_file = open(CONTROL_FILE_NAME, "r")
        self.update_status("Connected to radar!")

    def get_radar_config(self):
        """
        Get configuration from radar.
        """
        self.update_status("Requesting radar configuration...")

        # Make sure radar is connected
        if self.connected:
            # Request the current radar configuration
            message = MRM_GET_CONFIG_REQUEST + MESSAGE_ID
            self.connection['sock'].sendto(message,
                           (self.connection['udp_ip_radar'],
                            self.connection['udp_port']))

            # Parse the configuration from the received packet if available
            while True:
                try:
                    data, addr = self.connection['sock'].recvfrom(MAX_PACKET_SIZE)
                    break
                except:
                    pass

            byte_counter = 4
            config_status = "Received radar configuration!\n"
            for config_field in CONFIG_MSG_FORMAT.keys():
                num_bytes = CONFIG_MSG_FORMAT[config_field].itemsize
                config_data = data[byte_counter:(byte_counter + num_bytes)]
                hex_rep = config_data.encode("hex")
                int_rep = int(hex_rep, 16)
                self.config[config_field] = (
                        CONFIG_MSG_FORMAT[config_field].type(int_rep))
                config_status += ('\t' + config_field + ": " +
                                  str(self.config[config_field]) + "\n")
                byte_counter += num_bytes

            # Return received configuration in case needed
            self.update_status(config_status[:-1])
            return data

        else:
            self.update_status("Radar not connected!\n")
            exit()

    def set_radar_config(self):
        """
        Set radar configuration based on user settings.
        """
        # Make sure radar is connected
        self.update_status("Setting radar configuration...")
        if self.connected:

            # Determine desired configuration from user settings
            self.settings_to_config()

            # Scan resolution; API states that any value aside from 32 will
            # likely cause undesired behavior so overwrite it
            if self.config['scan_res'] != REC_SCAN_RES:
                self.update_status("Overriding scan resolution with " +
                                   "recommended value...")
                self.config['scan_res'] = REC_SCAN_RES

            # Configuration persistence flag
            if self.config['persist_flag'] != PERSIST_FLAG:
                self.update_status("WARNING: Configuration persistence flag " +
                                   "not set to recommended value...")

            # Initialize message to set new configuration
            message = MRM_SET_CONFIG_REQUEST + MESSAGE_ID

            # Add all configuration values to message
            for config_field in CONFIG_MSG_FORMAT.keys():
                num_bytes = CONFIG_MSG_FORMAT[config_field].itemsize
                message += self.value_to_message(self.config[config_field],
                                                 num_bytes)

            # Send configuration to radar
            self.connection['sock'].sendto(message,
                           (self.connection['udp_ip_radar'],
                            self.connection['udp_port']))

            # Check for configuration set confirmation from radar
            while True:
                try:
                    data, addr = self.connection['sock'].recvfrom(
                            MAX_PACKET_SIZE)
                    succ_flag = int(data[4:8].encode("hex"), 16)
                    if succ_flag != 0:
                        self.update_status("Error code " + str(succ_flag) +
                                           " encountered while setting " +
                                           "radar configuration!")
                        exit()
                    else:
                        self.update_status("Successfully set radar " +
                                           "configuration!")
                    break
                except:
                    pass

            # Get and return the latest radar configuration
            return self.get_radar_config()
        else:
            self.update_status("Radar not connected!")
            exit()

    def scan_request(self, num_scans, scan_interval=0):
        """
        Initiate a set of scans by the radar.
        """
        # Check if radar is connected and not already collecting data
        if self.connected:

            self.update_status("Requesting radar scan with %d scans..." %
                               num_scans)

            # Create scan request
            message = MRM_CONTROL_REQUEST + MESSAGE_ID
            message += self.value_to_message(num_scans, 2)
            message += self.value_to_message(RESERVED, 2)
            message += self.value_to_message(scan_interval, 4)

            # Send scan request to radar
            self.connection['sock'].sendto(message,
                           (self.connection['udp_ip_radar'],
                            self.connection['udp_port']))

            # Check if scan request was successful or not
            while True:
                try:
                    data, addr = self.connection['sock'].recvfrom(MAX_PACKET_SIZE)
                    succ_flag = int(data[4:8].encode("hex"), 16)
                    if succ_flag != 0:
                        self.update_status("Error code " + str(succ_flag) +
                                           " encountered while sending scan " +
                                           "request!")
                        exit()
                    else:
                        self.update_status("Successfully sent radar scan request!")
                        self.collecting = True
                    break
                except:
                    pass

        else:
            self.update_status("Radar not connected!")
            exit()

    def read_scan_data(self, save_file_name=None, num_packets=None):
        """
        Read data returned from radar scans.
        """
        # Create save file
        if save_file_name is not None:
            save_file = open('temp/' + save_file_name, "wb")

            # Add all configuration values to save file
            config = ""
            for config_field in CONFIG_MSG_FORMAT.keys():
                num_bytes = CONFIG_MSG_FORMAT[config_field].itemsize
                config += self.value_to_message(self.config[config_field],
                                                num_bytes)
            save_file.write(config)

        # Read fixed length or streaming data off radar
        self.update_status("Reading data from the radar...")
        packet_count = 0
        while True:
            try:
                data, addr = self.connection['sock'].recvfrom(MAX_PACKET_SIZE)
                if save_file_name is not None:
                    save_file.write(data)
                packet_count += 1

                # Read the specified number of packets
                if num_packets is not None:
                    if packet_count == num_packets:
                        break

                # Read until stop flag has been posted to the control file
                else:
                    stop_flag = self.control_file.read()
                    if stop_flag != "0":
                        break
                    self.control_file.seek(0)
            except:
                pass

        # Read any remaining streaming radar data
        start = time.time()
        while (time.time() - start) < STREAM_TIMEOUT:
            try:
                data, addr = self.connection['sock'].recvfrom(MAX_PACKET_SIZE)
                if save_file_name is not None:
                    save_file.write(data)
            except:
                pass

        self.update_status("Successfully read all the data!")

        # Close save file
        if save_file_name is not None:
            save_file.close()

    def quick_look(self, save_file_name="quick_look_data"):
        """
        Executes quick-look with radar to confirm desired operation.
        """
        # Compute number of expected data packets in quick-look
        num_quick_look_packets = (math.ceil(float(self.N_bin) / SEG_NUM_BINS) *
                                  QUICK_LOOK_NUM_SCANS)
        self.update_status("Starting quick-look mode...")

        # Check if radar is connected and not already collecting data
        if self.connected and not self.collecting:

            # Send a scan request
            self.scan_request(QUICK_LOOK_NUM_SCANS)
            self.collecting = True

            # Read scan data
            self.read_scan_data(save_file_name, num_quick_look_packets)

            # Complete quick-look
            self.update_status("Completed quick-look mode!")
            self.collecting = False

        else:
            self.update_status("Radar not connected or is already " +
                               "collecting data")
            exit()

    def collect(self, save_file_name=None):
        """
        Collects radar data continuously until commanded to stop.
        """
        # Create a save file name if not specified
        if save_file_name is None:
            ii = 0
            while os.path.exists('untitled_data%d' % ii):
                ii += 1
            save_file_name = 'untitled_data%d' % ii

        self.update_status("Starting collection mode...")

        # Check if radar is connected and not already collecting data
        if self.connected and not self.collecting:

            # Send a scan request to start collection
            self.scan_request(CONTINUOUS_SCAN)
            self.collecting = True
            running = True

            # Read streaming data from radar and save if desired
            self.read_scan_data(save_file_name)

            # Create scan request
            self.scan_request(STOP_SCAN)
            self.collecting = False
            running = False

        else:
            self.update_status("Radar not yet connected or is already " +
                               "collecting data")
            exit()