#import the required functions
import pickle
import numpy as np
import argparse
import sys
import pylab
import math

import matplotlib.pyplot as plt

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
#Loads pulses file
    f = open(args.file, 'rb')
    data = pickle.load(f)
    f.close()
    #print(data)
#Plot data
    Platform = data[0]
    Pulses = data[1]
    Ranges = data[2]
    AbsPulses = np.absolute(Pulses)
    RealPulses = np.real(Pulses)

    for i in AbsPulses:
        pylab.scatter(Ranges,i)

    plt.xlabel('Range')
    plt.ylabel('Intensity')
    plt.title('Intensity vs Range for 100 Positionss')
    #pylab.show()

    integrated_mags = Pulses[0]
    r = 0
    #while r < len(Ranges[0])-1:
    while r < 10:
        bshift = bin_shift(Ranges[0][r],Ranges[0][r+1])
        integrated_mags = coherently_integrate(integrated_mags,Pulses[r+1],bshift)
        r += 1
        print(integrated_mags)
    
#Mathematical functions
def bin_shift(range1,range2):
    return int(math.floor((range2-range1)/0.03))

def coherently_integrate(mag1,mag2,bshift):
    nmag = []
    for i in range(len(mag1)-bshift):
        m1 = 0
        m2 = 0
        if i < len(mag1)-bshift:
            m1 = mag1[i+bshift]
        if i < len(mag2)-bshift:
            m2 = mag2[i]
        nmag.append( math.sqrt((np.real(m1)+np.real(m2))**2+(np.imag(m1)+np.imag(m2))**2) )

    #print(nmag)
    return nmag

#Mathematical functions
    """
    Steps & proposed solutions
        1: Locate the reference point
    """
    xCenter = Math.round(np.amax(Platform[0])-((np.amax(Platform[0])-np.amin(Platform[0]))/2))
    yCenter = Math.round(np.amax(Platform[1])-((np.amax(Platform[1])-np.amin(Platform[1]))/2))
    zCenter = Math.round(np.amax(Platform[2])-((np.amax(Platform[2])-np.amin(Platform[2]))/2))
    """
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
