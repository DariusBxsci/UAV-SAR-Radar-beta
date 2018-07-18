#import the required functions
import pickle
import numpy as np
import argparse
import sys
import pylab
import math

import matplotlib.pyplot as plt

"""
KNOWN BUGS:
    -Certain files are 'unrecognized arguments'
"""

   

#Handles the arguments given in the console
def parse_args(args):
    parser = argparse.ArgumentParser(description='PulsON440 SAR Image former')
<<<<<<< HEAD
    parser.add_argument('-f', '--file', action='store', dest='file', help='PulsON 440 data file')
    parser.add_argument('-l --legacy', action='store_true', dest='legacy', help='Load legacy format of file')
=======
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')
    parser.add_argument('-l', '--legacy', action='store_true', dest='legacy', help='Load legacy format of file')
>>>>>>> fb1e582d55d454dc03d3a1cc4baa1d2837bedd27
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
<<<<<<< HEAD
    #print(data)

#plot data

    Platform = data[0]
    Pulses = data[1]
    Ranges = data[2]
    AbsPulses = np.absolute(Pulses)
    RealPulses = np.real(Pulses)

    for i in AbsPulses:
        pylab.scatter(Ranges,i)

    pylab.show()

    print(len(Platform))
    print(len(Pulses[0]))
    print(len(Ranges))

    integrated_mags = Pulses[0][0]
    r = 0
    while r < len(Ranges[0])-1:
        bshift = bin_shift(Ranges[0][r],Ranges[0][r+1])
        integrated_mags = coherently_integrate(integrated_mags,Pulses[0][r+1],bshift)
        r += 1

    console.log(integrated_mags)

#Mathematical functions
def bin_shift(range1,range2):
    return math.ceil((range2-range1)/0.03)

def coherently_integrate(mag1,mag2,bshift):
    if (bshift > 0):
        for i in range(bshift):
            np.insert(mag2,0,0)
            print(mag1)
            np.insert(mag1,mag1.shape[0],0)
    else:
        for i in range(bshift):
            np.insert(mag1,0,0)
            np.insert(mag2,mag2.shape[0],0)

    nmag = []
    for i in range(len(mag1)):
        nmag.append(mag1[i] + mag2[i])

    print(nmag)
    return nmag

=======
    pos = data[0]
    pulse = data[1]
    bins = data[2]
#Mathematical functions
    """
    Steps & proposed solutions
        1: Locate the reference point
    """
    xCenter = Math.round(np.amax(pos[0])-((np.amax(pos[0])-np.amin(pos[0]))/2))
    yCenter = Math.round(np.amax(pos[1])-((np.amax(pos[1])-np.amin(pos[1]))/2))
    zCenter = Math.round(np.amax(pos[2])-((np.amax(pos[2])-np.amin(pos[2]))/2))
    """
        2: Determine the image size/location/resolution (Square image)
        3: Compensate for time & position
            for n:
                time?[n] = 2(R[reference]-R[n])/SPEED_OF_LIGHT
        4: Find the range to each pixel from pulse location
        5: Fill in the image pixel by pixel using the average signal at that range
    """
>>>>>>> fb1e582d55d454dc03d3a1cc4baa1d2837bedd27
#Plots the processed data

#Starts the file's main function on loading
if __name__ == "__main__":
    main(sys.argv[1:])
