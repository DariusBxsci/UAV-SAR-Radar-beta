# -*- coding: utf-8 -*-
"""
Command and control script for PulsON 440 via Pi.
"""

# !!! Set the various IPs and ports
UDP_IP_RX = "192.168.1.1"  # Host (Raspberry Pi) IP address; can be reconfigured
UDP_IP_TX = "192.168.1.151"  # TIP Radar IP address; refer to documentation for value (found on page 5)
UDP_PORT = "21210"  # TIP Radar port; refer to documentation for value (found on page 5)


# Import the required modules
import sys
import argparse
from pulson440_skeleton import PulsON440
import config


def main(args):

    # Create PulsON440 object
    radar = PulsON440()
    #hand radar object of to configurator
    config.RADAR_OBJ = radar
    #configure
    config.configure(args)

    """
    #connect to radar
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.bind((UDP_IP_RX, UDP_PORT))
    """


if __name__ == "__main__":
    """
    Standard Python alias for command line execution.
    """
    main(sys.argv[1:])
