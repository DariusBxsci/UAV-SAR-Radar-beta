#import the required functions
import pickle
import numpy as np
import argparse
import sys

"""
KNOWN BUGS:
    -Certain files are 'unrecognized arguments'
"""    

   

#Handles the arguments given in the console
def parse_args(args):
    parser = argparse.ArgumentParser(description='PulsON440 SAR Image former')
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')
    parser.add_argument('-l', '--legacy', action='store_true', dest='legacy', help='Load legacy format of file')
    return parser.parse_args(args)
#Main function, creates the SAR image
def main(args):
#Gives arguments
    args = parse_args(sys.argv[1:])
    print(sys.argv[1:])
    print(args.file)
#Loads pulses file
    f = open(args.file, 'rb')
    data = pickle.load(f)
    f.close()
    pos = data[0]
    pulse = data[1]
    bins = data[2]
#Mathematical functions
    """
    Steps & proposed solutions
        1: Locate the reference point
    rangeBins = 'number of horizontal cells' - 1
    
    x-axis = pos[0] 'row 1'
    y-axis = pos[1] 'row 2'
    z-axis = pos[2] 'row 3'
    
    xMax = max(x-axis)
    xMin = min(x-axis)
    yMax = max(y-axis)
    yMin = min(y-axis)
    zMax = max(z-axis)
    zMin = min(z-axis)
            
    xCenter = Math.round(xMax-((xMax-xMin)/2))
    yCenter = Math.round(yMax-((yMax-yMin)/2))
    zCenter = Math.round(zMax-((zMax-zMin)/2))
        2: Determine the image size/location/resolution (Square image)
        3: Compensate for time & position
            for n:
                time?[n] = 2(R[reference]-R[n])/SPEED_OF_LIGHT
        4: Find the range to each pixel from pulse location
        5: Fill in the image pixel by pixel using the average signal at that range
    """
#Plots the processed data

#Starts the file's main function on loading
if __name__ == "__main__":
    main(sys.argv[1:])
