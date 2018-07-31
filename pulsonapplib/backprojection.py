import pickle
import numpy as np
import argparse
import sys
import pylab
import math
import matplotlib.pyplot as plt
from scipy import signal
from pulsonapplib.constants import SPEED_OF_LIGHT

# Gets overwritten later
IMAGE_RESOLUTION = (1000, 1000)  # Max pixel size
IMAGE_SIZE = (5.0, 5.0)
PIXEL_SIZE = (IMAGE_SIZE[0] / IMAGE_RESOLUTION[0], IMAGE_SIZE[1] / IMAGE_RESOLUTION[1])


# Gives each pixel a location based on the center being (0,0)
def get_pixel_in_space(x, y):
    loc = (-IMAGE_SIZE[0] / 2 + PIXEL_SIZE[0] * x, -IMAGE_SIZE[1] / 2 + PIXEL_SIZE[1] * y)
    return loc


# Finds the distance from the pixel to the platform
def get_pixel_range(x, y, plat_x):
    loc = get_pixel_in_space(x, y)
    range_p = math.sqrt((loc[0] - plat_x) ** 2 + (loc[1] + 15) ** 2 + 5 ** 2)
    return range_p


# Adds the distance calculated above to an array
def generate_range_vector(x, y, platform):
    res = []
    for p in platform:
        res.append(get_pixel_range(x, y, p))
    return res


# Gets the intensity of a pixel for one pulse
def get_intensity_in_space(pulse_range, pulse_intensities):
    r_bin = 0
    r_bin = int(pulse_range / (0.0184615))
    return pulse_intensities[r_bin]


# Adds the intensity of each pulse to the pixel
def integrate_pixel_intensity(ranges, pulses, x, y):  #, bul
    pixel_intensity = 0
    for i in range(len(ranges)):
        pixel_intensity += get_intensity_in_space(ranges[i], pulses[i])

    return pixel_intensity


# Parses arguments
def parse_args(args):
    parser = argparse.ArgumentParser(description='PulsON440 SAR Image former')
    parser.add_argument('-f', '--file', dest='file', help='PulsON 440 data file')
    parser.add_argument('-s', '--size', type=int, default=5.0, help='Size of the image')
    parser.add_argument('-p', '--pixels', type=int, default=250, help='Square root of pixels to be generated')
    parser.add_argument('-m', '--mode', dest='mode', type=str, default='normal',
                        help='Mode in which to run the program')
    parser.add_argument('-q', '--freq', type=int, default=4060000000, help='Center operating frequency of radar')
    return parser.parse_args(args)


# Fourier shift approach
def fourierShift(file, size, pixels, mode, freq, num):
    range_time = np.transpose(range_bins / SPEED_OF_LIGHT)
    drange_time = range_time[1] - range_time[0]

    row = np.zeros(pixels, dtype=np.complex)
    integrated_pulses = 0 + 0j
    for n in range(0, len(platform_positions)):
        pix_array = get_pixel_in_space(np.arange(0, IMAGE_RESOLUTION[0]), num)
        range_array = np.sqrt((pix_array[0] - platform_positions[n]) ** 2 + (pix_array[1] - 15) ** 2 + 25)

        ang_freq = 2 * np.pi * np.arange(-len(range_bins[0]) / 2, len(range_bins[0]) / 2) / (
                    len(range_bins[0]) * drange_time)
        time_distance = 2 * range_array / SPEED_OF_LIGHT

        pulsesofint = np.transpose(np.atleast_2d(pulses[n])) * np.exp(
            -1j * 2 * np.pi * freq * (range_time - time_distance))
        shiftvec = np.exp(1j * np.outer(ang_freq, time_distance))

        preShiftPulse = np.fft.fftshift(np.fft.fft(pulsesofint, axis=0), axes=0)
        shiftedPulse = preShiftPulse * shiftvec
        integrated_pulses += np.fft.ifft(np.fft.ifftshift(shiftedPulse, 0), axis=0)
        # print(len(preShiftPulse[0]))
        # print(len(shiftvec[0]))
    row = integrated_pulses[0]
    return row


colormap_name = 'viridis'

fluffy = plt.Figure(figsize=(10, 6), dpi=100)

# Main function, run to start file
def main(file, size, pixels, mode):
    # Finishes parsing arguments
    # args = parse_args(args)
    # Overwrites these variables to match console input values
    global IMAGE_RESOLUTION
    IMAGE_RESOLUTION = (pixels, pixels)
    global IMAGE_SIZE
    IMAGE_SIZE = (float(size), float(size))
    global PIXEL_SIZE
    PIXEL_SIZE = (IMAGE_SIZE[0] / IMAGE_RESOLUTION[0], IMAGE_SIZE[1] / IMAGE_RESOLUTION[1])
    global freq
    freq = 4060000000   # Frequency is hard-coded as of Nile's GUI version

    # Loads the .pkl file & saves data cleanly
    f = open(file, 'rb')
    data = pickle.load(f)
    f.close

    # Sorts the data loaded from the .pkl file
    global platform_positions
    platform_positions = np.swapaxes(data[0], 0, 1).tolist()[0]
    global pulses
    pulses = data[1]
    global range_bins
    range_bins = data[2]

    # Determines mode to use
    if mode is True:
        sar_image = np.zeros(IMAGE_RESOLUTION)
        perDone = 0
        for i in range(0, len(sar_image)):
            sar_image[i] = np.abs(fourierShift(file, size, pixels, mode, freq, i))
            if i == len(sar_image) - 1:
                print("Done")
            elif math.floor(100 * i / IMAGE_RESOLUTION[0]) > perDone:
                perDone = math.floor(100 * i / IMAGE_RESOLUTION[0])
                print(str(perDone) + "%")
    # Defines the matrix that will be used the generate the image and fills it in with the intensities
    else:
        sar_image = np.zeros(IMAGE_RESOLUTION)
        perDone = 0
        for i in range(len(sar_image)):
            for j in range(len(sar_image[i])):
                sar_image[len(sar_image) - i - 1][len(sar_image[i]) - j - 1] = integrate_pixel_intensity(
                    generate_range_vector(j, i, platform_positions), pulses, i, j)  #, bul
            if i == len(sar_image) - 1:
                print("Done")
            elif math.floor(100 * i / IMAGE_RESOLUTION[0]) > perDone:
                perDone = math.floor(100 * i / IMAGE_RESOLUTION[0])
                print(str(perDone) + "%")

    a = fluffy.add_subplot(111)
    a.clear()
    a.imshow(signal.convolve2d(np.abs(sar_image), [[0.11, 0.11, 0.11], [0.11, 0.11, 0.11], [0.11, 0.11, 0.11]]),
             cmap=plt.get_cmap(colormap_name))
    #a.show()

"""
if __name__ == '__main__':
    main(sys.argv[1:])
"""
