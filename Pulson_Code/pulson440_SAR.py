# -*- coding: utf-8 -*-

import pickle
import numpy as np
import argparse
import sys
import pylab
import math
import matplotlib.pyplot as plt

#Parses arguments
def parse_args(args):
    parser = argparse.ArgumentParser(description='PulsON440 SAR Image former')
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')
    parser.add_argument('-l', '--legacy', action='store_true', dest='legacy', help='Load legacy format of file')
    return parser.parse_args(args)

def main(args):
    #Finishes parsing arguments
    args = parse_args(args)
    #Loads the .pkl file & saves data cleanly
    f = open(args.file, 'rb')
    data = pickle.load(f)
    f.close
    pos = data[0]
    pulses = data[1]
    range = data[2][0]

if __name__ == '__main__':
    main(sys.argv[1:])