import pickle
import numpy as np
import argparse
import sys
import pylab
import math
import matplotlib.pyplot as plt

IMAGE_RESOLUTION = (150,150)
IMAGE_SIZE = (8.0,8.0)
PIXEL_SIZE = (IMAGE_SIZE[0]/IMAGE_RESOLUTION[0],IMAGE_SIZE[1]/IMAGE_RESOLUTION[1])
RANGE_AXIS = None

# Gives each pixel a location based on the center being (0,0)
def get_pixel_in_space(x,y):
    loc = (-IMAGE_SIZE[0]/2+PIXEL_SIZE[0]*x,-IMAGE_SIZE[1]/2+PIXEL_SIZE[1]*y)
    return loc
# Finds the distance from the pixel to the platform 
def get_pixel_range(x,y,plat_x):
    loc = get_pixel_in_space(x,y)
    range_p = math.sqrt( (loc[0] - plat_x)**2 + (loc[1] + 15)**2 + 5**2 )
    return range_p
# Adds the distance calculated above to an array
def generate_range_vector(x,y,platform):
    res = []
    for p in platform:
        res.append(get_pixel_range(x,y,p))
    return res
# Gets the intensity of a pixel for one pulse
def get_intensity_in_space(pulse_range,pulse_intensities):
    r_bin = 0
    r_bin = int(pulse_range / (0.0184615))
    return pulse_intensities[r_bin]
# Adds the intensity of each pulse to the pixel
def integrate_pixel_intensity(ranges,pulses):
    pixel_intensity = 0
    for i in range(len(ranges)):
        pixel_intensity += get_intensity_in_space(ranges[i],pulses[i])
    return pixel_intensity
# Parses arguments
def parse_args(args):
    parser = argparse.ArgumentParser(description='PulsON440 SAR Image former')
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')
    return parser.parse_args(args)
# Main function, run to start file
def main(args):
    #Finishes parsing arguments
    args = parse_args(args)
    #Loads the .pkl file & saves data cleanly
    f = open(args.file, 'rb')
    data = pickle.load(f)
    f.close
    # Sorts the data loaded from the .pkl file
    platform_positions = np.swapaxes(data[0],0,1).tolist()[0]
    pulses = data[1]
    range_bins = data[2][0]
    
    global RANGE_AXIS
    RANGE_AXIS = range_bins
    # Defines the matrix that will be used the generate the image and fills it in with the intensities
    sar_image = np.zeros(IMAGE_RESOLUTION)
    for i in range(len(sar_image)):
        for j in range(len(sar_image[i])):
            sar_image[-i][j] = np.absolute(integrate_pixel_intensity( generate_range_vector(j,i,platform_positions) , pulses ))
    # Shows the plot of the above matrix
    plt.imshow(sar_image)
    plt.show()

if __name__ == '__main__':
    main(sys.argv[1:])
