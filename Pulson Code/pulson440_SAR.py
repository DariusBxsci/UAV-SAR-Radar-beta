#import the required functions
import pickle
import numpy as np
import argparse
import sys

"""
KNOWN BUGS:
    -parse_args() isn't working as meant to, evidenced by print(args) outputting "none"
"""    

#Handles the arguments given in the console
def parse_args(args):
    parser = argparse.ArgumentParser(description='PulsON440 SAR Image former')
    parser.add_argument('-l --legacy', action='store_true', dest='legacy', help='Load legacy format of file')
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')

#Main function, creates the SAR image
def main(args):
#Gives arguments
    args = parse_args(args)
    print(sys.argv[1:])
    print(parser)
#Loads file - Replaced 'unpickle()'
    f = open(args.file, 'rb')
    data = pickle.load(args.file)
    f.close()
#Mathematical functions
    
#Plots the processed data

#Starts the file's purpose on loading
if __name__ == "__main__":
    main(sys.argv[1:])
