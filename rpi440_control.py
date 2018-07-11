# -*- coding: utf-8 -*-
"""
Command and control script for PulsON 440 via Pi.
"""

# Import the required modules
import sys
import argparse
from pulson440 import PulsON440
import config


def main(args):

    # Parse input arguments
    parsed_args = parse_args(args)

    print(parsed_args)

    # Create PulsON440 object
    radar = PulsON440()
    #hand radar object of to configurator
    config.RADAR_OBJ = radar
    #configure
    config.configure(args)


if __name__ == "__main__":
    """
    Standard Python alias for command line execution.
    """
    main(sys.argv[1:])
