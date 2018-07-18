import pickle
import numpy as np
import argparse
import sys
import pylab
import math
import matplotlib.pyplot as plt

IMAGE_RESOLUTION = (150,150)
IMAGE_SIZE = (3.0,3.0)
PIXEL_SIZE = (IMAGE_SIZE[0]/IMAGE_RESOLUTION[0],IMAGE_SIZE[1]/IMAGE_RESOLUTION[1])
RANGE_AXIS = None

def get_pixel_in_space(x,y):
    return (-IMAGE_SIZE[0]/2+PIXEL_SIZE[0]*x,-IMAGE_SIZE[1]/2+PIXEL_SIZE[1]*y)

def get_pixel_range(x,y,plat_x):
    loc = get_pixel_in_space(x,y)
    #print("PIXEL LOC " + str(loc))
    range_p = math.sqrt( (loc[0] - plat_x)**2 + (loc[1] + 15)**2 + 5**2 )
    return range_p

def generate_range_vector(x,y,platform):
    res = []
    for p in platform:
        res.append(get_pixel_range(x,y,p))
    return res

def get_intensity_in_space(pulse_range,pulse_intensities):
    r_bin = 0
    """
    while RANGE_AXIS[r_bin] < pulse_range:
        r_bin += 1
    """
    r_bin = int(round( pulse_range / 0.0369 ))
    #print("Falling in bin " + str(r_bin))
    return pulse_intensities[r_bin]

def integrate_pixel_intensity(ranges,pulses):
    pixel_intensity = 0
    for i in range(len(ranges)):
        if (i == 0):
            print(pulses[i])
        pixel_intensity += get_intensity_in_space(ranges[i],pulses[i])
    return pixel_intensity

#Parses arguments
def parse_args(args):
    parser = argparse.ArgumentParser(description='PulsON440 SAR Image former')
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')
    return parser.parse_args(args)

def main(args):
    #Finishes parsing arguments
    args = parse_args(args)
    #Loads the .pkl file & saves data cleanly
    f = open(args.file, 'rb')
    data = pickle.load(f)
    f.close
    
    platform_positions = data[0]
    platform_positions = np.swapaxes(platform_positions,0,1).tolist()[0]
    
    pulses = data[1]
    range_bins = data[2][0]
    print(range_bins)
    
    global RANGE_AXIS
    RANGE_AXIS = range_bins
    
    #print(platform_positions)
    
    sar_image = np.zeros(IMAGE_RESOLUTION)
    for i in range(len(sar_image)):
        for j in range(len(sar_image[i])):
            sar_image[i][j] = np.absolute(integrate_pixel_intensity( generate_range_vector(i,j,platform_positions) , pulses ))
            
    plt.imshow(sar_image)
    plt.show()

if __name__ == '__main__':
    main(sys.argv[1:])