# -*- coding: utf-8 -*-
"""
Constants module
"""

# Universal constants
SPEED_OF_LIGHT = 299792458 # m/s

# Communication protocol constants
MAX_PACKET_SIZE = 1500 # (bytes)
CONTINUOUS_SCAN = 65535 # Scan count setting to enable continuous scans
STOP_SCAN = 0 # Scan count setting to stop scans

# Radar constants
DT_MIN = 1 / (512 * 1.024) # Time sample resolution/bin size of the radar (ns)
T_BIN = 32 * DT_MIN # Rake receiver time sample/bin size (ns)
DN_BIN = 96 # Radar scan time segment/quanta size (ps)
SEG_NUM_BINS = 350.0 # Number of bins in a scan segment