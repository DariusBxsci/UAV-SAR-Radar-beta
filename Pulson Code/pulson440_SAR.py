#import the required functions
import pickle
import numpy as np
import argparse
import sys



#Loads the file ---WIP--- SEE:'fileName'
def unpickle(fileName, legacy=False):
    pickle.load(fileName ,fix_imports=True, encoding="ASCII", errors="strict")

#Handles the arguments given in the console
def parse_args(args):
    parser = argparse.ArgumentParser(description='PulsON440 SAR Image former')
    parser.add_argument('-l --legacy', action='store_true', dest='legacy',
                        help='Load legacy format of file')
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')

#Main function, creates the SAR image
def main(args):
    #Gives arguments
    #args = parse_args(args) ---WIP--- parse_args() is still broken
    #Loads file
    unpickle(arg.file, arg.legacy)#---WIP--- unpickle() is unknown
    
    #Mathematical functions
    
    #Plots the processed data

#Starts the file's purpose on loading
if __name__ == "__main__":
    #main()  #Used for testing file
    main(sys.argv[1:])  #<-Use in final version
