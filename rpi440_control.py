# -*- coding: utf-8 -*-
"""
Command and control script for PulsON 440 via Pi.
"""

# Import the required modules
import sys
import argparse
from pulson440 import PulsON440

def parse_args(args):
    """
    Input argument parser.
    TIP Recommend use of argparse module
    """
    # !!!

def main(args):
    """
    Top level method.
    TIP This is just a suggested program flow.
    """
    #!!!
    
    # Parse input arguments
    parsed_args = parse_args(args)
    
    print(parsed_args)
    
    # Create PulsON440 object
    radar = PulsON440()
    
    # Get the user settings
    radar.read_config_file()
    
    # Connect to the radar
    radar.connect()
    
    # Get current radar configuration
    radar.get_radar_config()
    
    # Set and get radar configuration
    radar.set_radar_config()
    
    if parsed_args.mode == "quick":
        radar.quick_look()
    elif parsed_args.mode == "collect":
        radar.collect()
    else:
        raise ValueError('mode argument must be either quick or collect')

if __name__ == "__main__":
    """
    Standard Python alias for command line execution.
    """
    main(sys.argv[1:])