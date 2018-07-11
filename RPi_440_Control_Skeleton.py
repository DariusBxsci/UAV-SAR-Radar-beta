# -*- coding: utf-8 -*-
"""
RPi_440_Control_Skeleton.py
Skeleton for script for controlling the PulsON 440 radar over ethernet using a 
Raspberry Pi.

Functionality that should be implemented includes:
    - Setting the radar configuration
    - Getting the radar's current configuration
    - Commanding the radar to execute a series of scans
    - Getting the data produced by the radar from a series of scans
    - Saving the received scan data from the radar to file
    - Performing a "quick-look" to confirm desired radar operation
    - Producing a "live" status check/file to confirm radar functionality

Sections that must be completed are denoted by the !!! codetag. TIP will be 
used to highlight additional information. This  script will not compile 
completely until at least all required sections have been filled in. It is 
recommended that as sections are completed they be tested for errors by 
commenting out incomplete sections. Students are welcome to only use this 
skeleton as a guide and architect their code as they see fit, e.g., breaking it
into methods and additional modules to be imported.
"""

# -----------------------------------------------------------------------------
# SETUP
# -----------------------------------------------------------------------------

# Import the recommended modules
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import socket
import struct
import sys

# Set the constants needed for radar calculations
SPEED_OF_LIGHT = 299792458
DT_MIN = 1 / (512 * 1.024) # Time sample resolution/bin size of the radar (ns)
T_BIN = 32 * DT_MIN # Rake receiver time sample/bin size (ns)
DN_BIN = 96 # Radar scan time segment/quanta size (ps)
DT_0 = 10 # Time/path delay through antenna (ns); Tx and Rx assumed the same

# !!! Define the radar messages types' codes
"""
TIP
Refer to the PulsON 440's API documentation about the available message types.
Defining them as constants will improve readability and ensure your code sends
and receives the expected messages to and from the radar. Please note that the
message types are sent to and from the radar over as part of byte stream over 
UDP. This means that you need to format the message to be sent as the byte 
representation of the actual message, e.g., INT32 -> 4 bytes. Suggestion is to 
represent a message type with a hexadecimal value of 0x1234 as 
MESSAGE_TYPE = \x12\x34'
"""

# !!! Set the various IPs and ports
UDP_IP_RX = "192.168.1.1" # Host (Raspberry Pi) IP address; can be reconfigured
UDP_IP_TX = # TIP Radar IP address; refer to documentation for value
UDP_PORT = # TIP Radar port; refer to documentation for value

# Set the default values of the radar
"""
TIP
These are only suggested values; tune to support recommended quick-look 
capability.
"""
num_pulses = 500
range_start = 4
range_stop = 14.5
tx_gain = 63
pii = 11
    
# Load in the radar configuration
with open("radar_params.conf", "r") as config_file:
    config_data = config_file.readlines()
for data_line in config_data:
    data_line = data_line.strip()
    if len(data_line) != 0:
        if data_line[0] != "#":
            data_line = data_line.split('=')
            if data_line[0] == "range_start":
                range_start = data_line[1]
            elif data_line[0] == "range_stop":
                range_stop = data_line[1]
            elif data_line[0] == "tx_gain":
                tx_gain = data_line[1]
            elif data_line[0] == "pii":
                pii = data_line[1]
            else:
                pass
del config_data
del data_line

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
    
# Open the control file
control_file = open("control", "w")
control_file.write("0")
control_file.close()
control_file = open("control", "r")

# Open the status file
status_file = open("status", "w")

# Open the save file if needed
if save_flag:
    save_file = open(save_file_name, 'wb')

# Setup the UDP socket for receiving
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind((UDP_IP_RX, UDP_PORT))

# Request the current radar configuration
status_file.write("Requesting radar configuration...\n")
MESSAGE = MRM_GET_CONFIG_REQUEST + '\x00\x01'
sock.sendto(MESSAGE, (UDP_IP_TX, UDP_PORT))
while True:
    # Try to read a packet if available
    try:
        data, addr = sock.recvfrom(1500)
        status_file.write("Received radar configuration!\n\n")
        break
    except:
        pass
message_type = np.uint16(int(data[0:2].encode("hex"),16))
message_id = np.uint16(int(data[2:4].encode("hex"),16))
node_id = np.uint32(int(data[4:8].encode("hex"),16))
scan_start = np.int32(int(data[8:12].encode("hex"),16))
scan_stop = np.int32(int(data[12:16].encode("hex"),16))
scan_res = np.uint16(int(data[16:18].encode("hex"),16))
bii = np.uint16(int(data[18:20].encode("hex"),16))
seg_1_samp = np.uint16(int(data[20:22].encode("hex"),16))
seg_2_samp = np.uint16(int(data[22:24].encode("hex"),16))
seg_3_samp = np.uint16(int(data[24:26].encode("hex"),16))
seg_4_samp = np.uint16(int(data[26:28].encode("hex"),16))
seg_1_int = np.uint8(int(data[28:29].encode("hex"),16))
seg_2_int = np.uint8(int(data[29:30].encode("hex"),16))
seg_3_int = np.uint8(int(data[30:31].encode("hex"),16))
seg_4_int = np.uint8(int(data[31:32].encode("hex"),16))
ant_mode = np.uint8(int(data[32:33].encode("hex"),16))
gain = np.uint8(int(data[33:34].encode("hex"),16))
status_file.write("Message Type: " + hex(message_type) + "\n")
status_file.write("Message ID: " + str(message_id) + "\n")
status_file.write("Node ID: " + str(node_id) + "\n")
status_file.write("Scan Start (ps): " + str(scan_start) + "\n")
status_file.write("Scan Stop (ps): " + str(scan_stop) + "\n")
status_file.write("Scan Resolution: " + str(scan_res) + "\n")
status_file.write("Pulse Integration Index: " + str(bii) + "\n")
status_file.write("Antenna Mode: " + str(ant_mode) + "\n")
status_file.write("Gain Index: " + str(gain) + "\n\n")

# Set the desired radar configuration parameters
scan_start = 2*float(range_start)/(SPEED_OF_LIGHT/1e9) + DT_0
scan_stop = 2*float(range_stop)/(SPEED_OF_LIGHT/1e9) + DT_0
Nbin = (scan_stop - scan_start)/T_BIN
Nseg = math.ceil(Nbin/DN_BIN)
Nbin = DN_BIN*Nseg
scan_start = math.floor(1000*DT_MIN*math.floor(scan_start/DT_MIN))/1000
scan_stop = Nbin*T_BIN + scan_start
scan_stop = math.floor(1000*DT_MIN*math.ceil(scan_stop/DT_MIN))/1000
bii = pii
gain = tx_gain

# Create the message to set the new configuration
MESSAGE = MRM_SET_CONFIG_REQUEST + '\x00\x01' + data[4:8]
scan_start_hex = hex(int(scan_start*1000))
scan_start_hex = '0'*(8-len(scan_start_hex[2:])) + scan_start_hex[2:]
MESSAGE = MESSAGE + chr(int(scan_start_hex[:2],16)) + chr(int(scan_start_hex[2:4],16)) + chr(int(scan_start_hex[4:6],16)) + chr(int(scan_start_hex[6:8],16))
scan_stop_hex = hex(int(scan_stop*1000))
scan_stop_hex = '0'*(8-len(scan_stop_hex[2:])) + scan_stop_hex[2:]
MESSAGE = MESSAGE + chr(int(scan_stop_hex[:2],16)) + chr(int(scan_stop_hex[2:4],16)) + chr(int(scan_stop_hex[4:6],16)) + chr(int(scan_stop_hex[6:8],16))
MESSAGE = MESSAGE + data[16:18]
bii_hex = hex(int(bii))
bii_hex = '0'*(4-len(bii_hex[2:])) + bii_hex[2:]
MESSAGE = MESSAGE + chr(int(bii_hex[:2],16)) + chr(int(bii_hex[2:],16))
MESSAGE = MESSAGE + data[20:33]
gain_hex = hex(int(gain))
gain_hex = '0'*(2-len(gain_hex[2:])) + gain_hex[2:]
MESSAGE = MESSAGE + chr(int(gain_hex,16))
MESSAGE = MESSAGE + chr(0) + chr(1)

# Send the desired radar configuration
status_file.write("Setting radar configuration...\n")
sock.sendto(MESSAGE, (UDP_IP_TX, UDP_PORT))
while True:
    # Try to read a packet if available
    try:
        data, addr = sock.recvfrom(1500)
        succ_flag = int(data[4:].encode("hex"),16)
        if succ_flag != 0:
            status_file.write("Error setting radar configuration!\n\n")
            exit()
        else:
            status_file.write("Successfully set radar configuration!\n\n")
        break
    except:
        pass
    
# Request the current radar configuration
status_file.write("Requesting radar configuration...\n")
MESSAGE = MRM_GET_CONFIG_REQUEST + '\x00\x01'
sock.sendto(MESSAGE, (UDP_IP_TX, UDP_PORT))
while True:
    # Try to read a packet if available
    try:
        data, addr = sock.recvfrom(1500)
        status_file.write("Received radar configuration!\n\n")
        break
    except:
        pass
message_type = np.uint16(int(data[0:2].encode("hex"),16))
message_id = np.uint16(int(data[2:4].encode("hex"),16))
node_id = np.uint32(int(data[4:8].encode("hex"),16))
scan_start = np.int32(int(data[8:12].encode("hex"),16))
scan_stop = np.int32(int(data[12:16].encode("hex"),16))
scan_res = np.uint16(int(data[16:18].encode("hex"),16))
bii = np.uint16(int(data[18:20].encode("hex"),16))
seg_1_samp = np.uint16(int(data[20:22].encode("hex"),16))
seg_2_samp = np.uint16(int(data[22:24].encode("hex"),16))
seg_3_samp = np.uint16(int(data[24:26].encode("hex"),16))
seg_4_samp = np.uint16(int(data[26:28].encode("hex"),16))
seg_1_int = np.uint8(int(data[28:29].encode("hex"),16))
seg_2_int = np.uint8(int(data[29:30].encode("hex"),16))
seg_3_int = np.uint8(int(data[30:31].encode("hex"),16))
seg_4_int = np.uint8(int(data[31:32].encode("hex"),16))
ant_mode = np.uint8(int(data[32:33].encode("hex"),16))
gain = np.uint8(int(data[33:34].encode("hex"),16))
status_file.write("Message Type: " + hex(message_type) + "\n")
status_file.write("Message ID: " + str(message_id) + "\n")
status_file.write("Node ID: " + str(node_id) + "\n")
status_file.write("Scan Start (ps): " + str(scan_start) + "\n")
status_file.write("Scan Stop (ps): " + str(scan_stop) + "\n")
status_file.write("Scan Resolution: " + str(scan_res) + "\n")
status_file.write("Pulse Integration Index: " + str(bii) + "\n")
status_file.write("Antenna Mode: " + str(ant_mode) + "\n")
status_file.write("Gain Index: " + str(gain) + "\n\n")
if save_flag:
    save_file.write(data)

# Start the radar in the specified mode
# Continuous mode
if op_mode == "c":
    
    # Start the radar
    status_file.write("Starting radar in continuous operation mode...\n")
    MESSAGE = MRM_CONTROL_REQUEST + '\x00\x01'
    num_pulses_hex = hex(65535)
    num_pulses_hex = '0'*(4-len(num_pulses_hex[2:])) + num_pulses_hex[2:]
    MESSAGE = MESSAGE + chr(int(num_pulses_hex[:2],16)) + chr(int(num_pulses_hex[2:],16))
    MESSAGE = MESSAGE + chr(0) + chr(0) + chr(0) + chr(0) + chr(0) + chr(0)
    sock.sendto(MESSAGE, (UDP_IP_TX, UDP_PORT))
    while True:
        # Try to read a packet if available
        try:
            data, addr = sock.recvfrom(1500)
            succ_flag = int(data[4:].encode("hex"),16)
            if succ_flag != 0:
                status_file.write("Error starting radar!\n\n")
                exit()
            else:
                status_file.write("Successfully started radar!\n\n")
            break
        except:
            pass
        
    # Read the streaming data and save
    status_file.write("Reading the data...\n")
    status_file.flush()
    while True:
    
        # Try to read a packet if available
        try:
            data, addr = sock.recvfrom(1500)
            if save_flag:
                save_file.write(data)
        except:
            pass
        
        # Check the status of the control file and quit if signaled
        exit_flag = control_file.read()
        if exit_flag != "0":
            break
        control_file.seek(0)
        
    # Stop the radar
    status_file.write("Successfully read all the data!\n\n")
    status_file.write("Stopping radar...\n")
    MESSAGE = MRM_CONTROL_REQUEST + '\x00\x01'
    num_pulses_hex = hex(0)
    num_pulses_hex = '0'*(4-len(num_pulses_hex[2:])) + num_pulses_hex[2:]
    MESSAGE = MESSAGE + chr(int(num_pulses_hex[:2],16)) + chr(int(num_pulses_hex[2:],16))
    MESSAGE = MESSAGE + chr(0) + chr(0) + chr(0) + chr(0) + chr(0) + chr(0)
    sock.sendto(MESSAGE, (UDP_IP_TX, UDP_PORT))
    while True:
        # Try to read a packet if available
        try:
            data, addr = sock.recvfrom(1500)
            succ_flag = int(data[4:].encode("hex"),16)
            if succ_flag != 0:
                status_file.write("Error stopping radar!\n\n")
                exit()
            else:
                status_file.write("Successfully stopped radar!\n\n")
            break
        except:
            pass
    
# Quick look mode
elif op_mode == "q":
    
    # Open the temporary file
    temp_file = open("temp", "wb")
    
    # Start the radar
    status_file.write("Starting radar in quick look operation mode...\n")
    print("Starting radar in quick look operation mode...")
    MESSAGE = MRM_CONTROL_REQUEST + '\x00\x01'
    num_pulses_hex = hex(num_pulses)
    num_pulses_hex = '0'*(4-len(num_pulses_hex[2:])) + num_pulses_hex[2:]
    MESSAGE = MESSAGE + chr(int(num_pulses_hex[:2],16)) + chr(int(num_pulses_hex[2:],16))
    MESSAGE = MESSAGE + chr(0) + chr(0) + chr(0) + chr(0) + chr(0) + chr(0)
    sock.sendto(MESSAGE, (UDP_IP_TX, UDP_PORT))
    while True:
        # Try to read a packet if available
        try:
            data, addr = sock.recvfrom(1500)
            succ_flag = int(data[4:].encode("hex"),16)
            if succ_flag != 0:
                status_file.write("Error starting radar!\n\n")
                print("Error starting radar!\n")
                exit()
            else:
                status_file.write("Successfully started radar!\n\n")
                print("Successfully started radar!\n")
            break
        except:
            pass
        
    # Read the streaming data and save if desired
    status_file.write("Reading the data...\n")
    print("Reading the data...")
    count = 0
    max_packets = math.ceil(float(Nbin)/350.0)*num_pulses
    while True:
        # Try to read a packet if available
        try:
            data, addr = sock.recvfrom(1500)
            temp_file.write(data)
            if save_flag:
                save_file.write(data)
            count = count + 1
            if count == max_packets:
                status_file.write("Successfully read all the data!\n\n")
                print("Successfully read all the data!\n")
                break
        except:
            pass
        
    # Read back in the data for plotting
    temp_file.close()
    temp_file = open("temp", "rb")
    max_messages =  math.ceil(float(Nbin)/350.0)
    rti = np.zeros((num_pulses, int(350*max_messages)))
    for packet_ind in range(0, int(max_packets)):
        junk = temp_file.read(52)
        for range_ind in range(0, 350):
            range_data = temp_file.read(4)
            rti[int(math.floor(packet_ind/max_messages)), range_ind + int(packet_ind % max_messages)*350] = struct.unpack(">l", range_data)[0]
    temp_file.close()
    os.remove("temp")
    
    # Plot the data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('RTI')
    plt.imshow(20*np.log10(np.abs(rti[:, :int(Nbin)])))
    plt.colorbar(orientation='vertical')
    ax.set_aspect('equal')
    plt.show()
    
# Somehow the operating mode flag was messed up        
else:
    pass
    
# Close the files
status_file.write("Closing files and ending program!\n")
print("Closing files and ending program!")
control_file.close()
status_file.close()
if save_flag:
    save_file.close()

# -----------------------------------------------------------------------------

def get_radar_config():
    """
    !!! Get radar configuration.
    """
    # TIP 
# -----------------------------------------------------------------------------

def set_radar_config():
    """
    !!! Set radar configuration.
    """

# -----------------------------------------------------------------------------

def quick_look():
    """
    !!! Executes quick-look with radar to confirm desired operation.
    """
    # TIP This should only collect and present/visualize a small set of data.

# -----------------------------------------------------------------------------
    
def collect():
    """
    !!! Collects radar data continuously until commanded to stop.
    """
    return 2

# -----------------------------------------------------------------------------

def parse_args(args):
    """
    !!! Input argument parser.
    """
    # TIP Suggest use of argparse module.

# -----------------------------------------------------------------------------
    
def main(args):
    """
    !!! Top-level method to execute all stages of data unpacking.
    """
    # TIP Basic recommended (not required) program flow shown.
    parsed_args = parse_args(args)
    
    if parsed_args.mode == "quick":
        quick_look()
    elif parsed_args.mode == "collect":
        collect()
    else:
        raise ValueError('mode argument must be either quick or collect')

# -----------------------------------------------------------------------------
    
if __name__ == "__main__":
    """
    Standard Python conditional script stanza for command line usage.
    """
    main(sys.argv[1:])