# -*- coding: utf-8 -*-
"""
RTK_Log.py
Script for logging the RTK GPS data using a Raspberry Pi

Created on Tue Apr 10 15:22:00 2018

Updated on Tue Apr 10 2018
    Added basic functionality

@author: Michael Riedl
"""

# -----------------------------------------------------------------------------
# SETUP
# -----------------------------------------------------------------------------

# Import the required modules
import serial
import sys

# -----------------------------------------------------------------------------
# SET PARAMETERS
# -----------------------------------------------------------------------------

# Make sure there are not too many inputs
if len(sys.argv) > 2:
    print("Requires only one (1) input parameter!\n")
    print("Usage: python RTK_Log.py [filename]\n")
    print("\t[filename]: Name of the file to save the RTK GPS data.")
    exit()
    
# Check for valid input arguments and set the save file
if len(sys.argv) == 1:
    save_file_name = "untitled.rtk"
else:
    if sys.argv[1] == "--help":
        print("Usage: python RTK_Log.py [filename]\n")
        print("\t[filename]: Name of the file to save the RTK GPS data.")
        exit()   
    save_file_name = sys.argv[1]
    if save_file_name[0] == "-":
        print(save_file_name, "is an invalid file name!")
        exit()
        
# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
    
# Open the control file
control_file = open("control_rtk", "w")
control_file.write("0")
control_file.close()
control_file = open("control_rtk", "r")

# Open the save file
save_file = open(save_file_name, 'wb')

# Setup the serial port for reading the data
ser = serial.Serial("/dev/ttyACM0")
print("Logging the data...")

# Start loggin the data
while True:
    
    # Try to read a packet if available
    data = ser.read(1500)
    save_file.write(data)
    
    # Check the status of the control file and quit if signaled
    exit_flag = control_file.read()
    if exit_flag != "0":
        break
    control_file.seek(0)
    
# Close the files
print("Closing files and ending program!")
control_file.close()
save_file.close()