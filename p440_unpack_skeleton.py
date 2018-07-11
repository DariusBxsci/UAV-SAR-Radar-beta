# -*- coding: utf-8 -*-
"""
PulsON 440 radar data unpacking module 
"""

import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from constants import SPEED_OF_LIGHT, MAX_PACKET_SIZE, CONTINUOUS_SCAN, \
    STOP_SCAN, DT_MIN, T_BIN, DN_BIN, SEG_NUM_BINS



def unpack(file):
    """
    Unpacks PulsOn 440 radar data from input file.
    TIP Follow the format you defined when saving the data.
    TIP You will need to unpack or provide the radar configuration that was 
    used to collect htis data.
    """
    # !!!
        
        # Compute number of range bins in data
        DT_0 = 10
        scan_start_time = float(config['scan_start'])
        scan_end_time = float(config['scan_end'])
        num_range_bins = DN_BIN * math.ceil((scan_end_time - scan_start_time) /
                                           (T_BIN * 1000 * DN_BIN))
        num_packets_per_scan = math.ceil(num_range_bins / 350)
        start_range = (SPEED_OF_LIGHT * ((scan_start_time * 1e-12) - DT_0 * 
                                         1e-9) / 2)
        drange_bins = SPEED_OF_LIGHT * T_BIN * 1e-9 / 2
        range_bins = start_range + drange_bins * np.arange(0, num_range_bins, 
                                                           1)
        
        # TIP Stack scan data into 2-D array 
        # (rows -> pulses, columns -> range bins)
        
def parse_args(args):
    """
    Input argument parser.
    TIP Recommend use of argparse module.
    """
    # !!!
    
def main(args):
    """
    Top-level function; parses input arguments, unpacks, data, visualizes, and
    saves as specified.
    """
    # !!!
    
    # TIP Visualize RTI of unpacked data
    if args.visualize:
        rti_ax = plt.imshow(20 * np.log10(np.abs(data['scan_data'])))
        rti_ax.axes.set_aspect('auto')
        plt.title('Range-Time Intensity')
        plt.xlabel('Range Bins')
        plt.ylabel('Pulse Index')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('dB')
        plt.show()

if __name__ == "__main__":
    """
    Standard Python alias for command line execution.
    """
    main(sys.argv[1:])