# -*- coding: utf-8 -*-
"""
PulsON 440 radar data unpacking module 
"""

# Import the required modules
import os
import sys
import argparse
import pickle
import math
import matplotlib.pyplot as plt
import numpy as np
from pulson440_formats import CONFIG_MSG_FORMAT
from pulson440_constants import SPEED_OF_LIGHT, T_BIN, DN_BIN

# Constants
DT_0 = 10 # Path delay through antennas (ns)

def read_config_data(file_handle, legacy=False):
    """
    Read in configuration data based on platform.
    """
    config = dict.fromkeys(CONFIG_MSG_FORMAT.keys())
    
    if legacy:
        config_msg = file_handle.read(44)
        config['node_id'] = np.frombuffer(config_msg[4:8], dtype='>u4')[0]
        config['scan_start'] = np.frombuffer(config_msg[8:12], dtype='>i4')[0]
        config['scan_stop'] = np.frombuffer(config_msg[12:16], dtype='>i4')[0]
        config['scan_res'] = np.frombuffer(config_msg[16:18], dtype='>u2')[0]
        config['pii'] = np.frombuffer(config_msg[18:20], dtype='>u2')[0]
        config['ant_mode'] = np.uint16(config_msg[32])
        config['tx_gain_ind'] = np.uint16(config_msg[33])
        config['code_channel'] = np.uint16(config_msg[34])
        config['persist_flag'] = np.uint16(config_msg[35])
        
    else:
        config_msg = file_handle.read(32)
        byte_counter = 0
        for config_field in CONFIG_MSG_FORMAT.keys():
            num_bytes = CONFIG_MSG_FORMAT[config_field].itemsize
            config_data = config_msg[byte_counter:(byte_counter + num_bytes)]
            config[config_field] = np.frombuffer(config_data,
                  dtype=CONFIG_MSG_FORMAT[config_field])[0]
            config[config_field] = config[config_field].byteswap()
            byte_counter += num_bytes
            
    return config

def unpack(file, legacy=False):
    """
    Unpacks PulsOn 440 radar data from input file
    """
    with open(file, 'rb') as f:
        
        # Read configuration part of data
        config = read_config_data(f, legacy)
        
        # Compute number of range bins in datas
        scan_start_time = float(config['scan_start'])
        scan_end_time = float(config['scan_stop'])
        num_range_bins = DN_BIN * math.ceil((scan_end_time - scan_start_time) /
                                           (T_BIN * 1000 * DN_BIN))
        num_packets_per_scan = math.ceil(num_range_bins / 350)
        start_range = SPEED_OF_LIGHT * ((scan_start_time * 1e-12) - DT_0 * 1e-9) / 2
        drange_bins = SPEED_OF_LIGHT * T_BIN * 1e-9 / 2
        range_bins = start_range + drange_bins * np.arange(0, num_range_bins, 1)
        
        # Read data
        data = dict()
        data= {'scan_data': [],
               'time_stamp': [],
               'packet_ind': [],
               'packet_pulse_ind': [],
               'range_bins': range_bins}
        single_scan_data = []
        packet_count = 0
        pulse_count = 0
        
        while True:
            
            # Read a single data packet and break loop if not a complete packet
            # (in terms of size)
            packet = f.read(1452)
            if len(packet) < 1452:
                break            
            packet_count += 1
            
            # Packet index
            data['packet_ind'].append(np.frombuffer(packet[48:50], dtype='u2'))
            
            # Extract radar data samples from current packet; process last 
            # packet within a scan seperately to get all data
            if packet_count % num_packets_per_scan == 0:
                num_samples = num_range_bins % 350
                packet_data = np.frombuffer(packet[52:(52 + 4 * num_samples)], 
                                                   dtype='>i4')
                single_scan_data.append(packet_data)
                data['scan_data'].append(np.concatenate(single_scan_data))
                data['time_stamp'].append(np.frombuffer(packet[8:12], 
                    dtype='>u4'))
                single_scan_data = []
                pulse_count += 1
            else:
                num_samples = 350
                packet_data = np.frombuffer(packet[52:(52 + 4 * num_samples)], 
                                                   dtype='>i4')
                single_scan_data.append(packet_data)
            
        # Add last partial scan if present
        if single_scan_data:
            single_scan_data = np.concatenate(single_scan_data)
            num_pad = data['scan_data'][0].size - single_scan_data.size
            single_scan_data = np.pad(single_scan_data, (0, num_pad), 
                                      'constant', constant_values=0)
            data['scan_data'].append(single_scan_data)
                
        # Stack scan data into 2-D array 
        # (rows -> pulses, columns -> range bins)
        data['scan_data'] = np.stack(data['scan_data'])
        
        # Finalize remaining entries in data
        data['time_stamp']

        return data

def parse_args(args):
    """
    Input argument parser.
    """
    parser = argparse.ArgumentParser(
            description='PulsON 440 radar data unpacker')
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')
    parser.add_argument('-o', '--output', nargs='?', const='data.dat', default='',
                        dest='output', help='Output file; data will be pickled')
    parser.add_argument('-v', '--visualize', action='store_true', dest='visualize',
                        help='Plot RTI of unpacked data; will block computation')
    parser.add_argument('-l --legacy', action='store_true', dest='legacy',
                        help='Load legacy format of file')
    
    return parser.parse_args(args)

def main(args):
    """
    Top-level function; parses input arguments, unpacks, data, visualizes, and
    saves as specified.
    """
    args = parse_args(args)
    
    data = unpack(args.file, args.legacy)
    
    # Save (pickle) unpacked data
    if args.output:
        with open(args.output, 'wb') as o:
            pickle.dump(data, o)

    # Visualize RTI of unpacked data
    plt.ioff()
    if args.visualize:
        rti_ax = plt.imshow(20 * np.log10(np.abs(data['scan_data'])))
        rti_ax.axes.set_aspect('auto')
        plt.title('Range-Time Intensity')
        plt.xlabel('Range Bins')
        plt.ylabel('Pulse Index')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('dB')
        
        # Try to display to screen if available otherwise save to file
        try:
            plt.show()
        except:
            plt.savefig('%s.png' % os.path.splitext(args.file)[0])

if __name__ == "__main__":
    """
    Standard Python alias for command line execution.
    """
    main(sys.argv[1:])