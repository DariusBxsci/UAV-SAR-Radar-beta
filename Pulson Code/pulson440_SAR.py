#import the required functions
import pickle
import numpy as np
import argparse
import sys



#Loads the file ---WIP--- SEE:'fileName'
def unpickle(fileName):
    pickle.load(fileName ,fix_imports=True, encoding="ASCII", errors="strict")

#Main function, creates the SAR image
def main():
    print(sys.argv[1:])
    
    #Loads file
""" unpickle(arg) """
    
    #Mathematical functions
    
    #Plots the processed data

#Starts the file's purpose on loading
if __name__ == "__main__":
    main()  #Used for testing file
    #main(sys.argv[1:])  <-Use in final version