# -*- coding: utf-8 -*-
"""
Command and control script for PulsON 440 via Pi.
"""

# Import the required modules
import os
import sys
import argparse
from pulson import PulsON440


def is_valid_file(parser, arg, mode):
    """
    Check if specified argument is a valid file for read or write.
    """
    if mode == 'r':
        try:
            f = open(arg, 'r')
            f.close()
        except:
            parser.error("The file %s does not exist or cannot be read!" % arg)
    elif mode == 'w' and arg is not None:
        try:
            f = open(arg, 'w')
            f.close()
            os.remove(arg)
        except:
            parser.error("The file %s does not exist or cannot be written " +
                         "to!" % arg)


def parse_args(args):
    """
    Input argument parser.
    """
    parser = argparse.ArgumentParser(
        description=('PulsON 440 command and control script; on Unix ' +
                     'systems it is recommended that users run this ' +
                     'script as a background process by appending ' +
                     '\" &\" to the end of the command line call'))
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-q', '--quick', action='store_true',
                            help='Quick-look mode')
    mode_group.add_argument('-c', '--collect', action='store_true',
                            help='Collect mode')
    parser.add_argument('-i', '--input', nargs='?', const="radar_settings",
                        default="radar_settings", help='Radar settings file')
    parser.add_argument('-o', '--output', nargs='?', const=None, default=None,
                        help='File to store data to')

    parsed_args = parser.parse_args(args)

    # Check the file inputs
    is_valid_file(parser, parsed_args.input, 'r')
    is_valid_file(parser, parsed_args.output, 'w')

    return parsed_args


def main(args):
    """
    Top level method.
    """

    # Parse input arguments
    parsed_args = parse_args(args)

    # Create PulsON440 object
    radar = PulsON440()

    # Get the user settings
    radar.read_settings_file(parsed_args.input)

    # Connect to the radar
    radar.connect()

    # Get current radar configuration
    radar.get_radar_config()

    # Set and get radar configuration
    radar.set_radar_config()

    # Perform specified mode
    if parsed_args.quick:
        radar.quick_look()
    elif parsed_args.collect:
        radar.collect()
    else:
        raise ValueError('unrecognized mode')
        exit()


if __name__ == "__main__":
    """
    Standard Python alias for command line execution.
    """
    main(sys.argv[1:])