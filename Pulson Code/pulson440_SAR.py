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
    parser.add_argument('-f', '--file', action='store', dest='file', help='PulsON 440 data file')
    parser.add_argument('-l --legacy', action='store_true', dest='legacy', help='Load legacy format of file')
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


    integrated_mags = Pulses[0]
    r = 0
    #while r < len(Ranges[0])-1:
    while r < 10:
        bshift = bin_shift(Ranges[0][r],Ranges[0][r+1])
        integrated_mags = coherently_integrate(integrated_mags,Pulses[r+1],bshift)
        r += 1

    #console.log(integrated_mags)

    Platform = data[0]
    Pulses = integrated_mags
    Ranges = data[2]
    
    print(len(integrated_mags))
    print(len(Ranges))
    
    for i in AbsPulses:
        pylab.scatter(Ranges,i)

    pylab.show()

    
#Mathematical functions
def bin_shift(range1,range2):
    return int(math.floor((range2-range1)/0.03))

def coherently_integrate(mag1,mag2,bshift):
    print(len(mag1))
    print(len(mag2))
    print('\n')
    
    print("SHIFT: " + str(bshift))
    nmag = []
    for i in range(len(mag1)-bshift):
        m1 = 0
        m2 = 0
        if i < len(mag1)-bshift:
            m1 = mag1[i+bshift]
        if i < len(mag2)-bshift:
            m2 = mag2[i]
        #print (np.real(m1))
        #print (np.real(m2))
        #print(i)
        #nmag.append((np.real(m1)+np.real(m2),np.imag(m1)+np.imag(m2)))
        nmag.append( math.sqrt((np.real(m1)+np.real(m2))**2+(np.imag(m1)+np.imag(m2))**2) )

    #print(nmag)
    return nmag

#Plots the processed data

#Starts the file's main function on loading
if __name__ == "__main__":
    main(sys.argv[1:])
