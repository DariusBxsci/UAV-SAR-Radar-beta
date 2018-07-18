#import the required functions
import pickle
import numpy as np
import argparse
import sys
import pylab

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
    f = open(args.file, 'rb')
    data = pickle.load(f)
    f.close()

#plot data

    Platform = data[0]
    Pulses = data[1]
    Ranges = data[2]
    AbsPulses = np.absolute(Pulses)
    RealPulses = np.real(Pulses)

    print(Ranges)

    #for r in AbsPulses:
        #print(np.max(r))

    for i in AbsPulses:
        pylab.scatter(Ranges,i)

    pylab.show()

if __name__ == "__main__":
    main(sys.argv[1:])
