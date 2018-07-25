import numpy as np 
import cv2
#1. Turn given image into something that can be used in blob detection (?)
Image = cv2.imread('Fourier Image_Cropped.png',0) #Brings in scan, 0 is grayscale, 1 is color
Image = cv2.GaussianBlur(Image,(5,5),0)
Image = cv2.bitwise_not(Image) #Inverse color. COMMENT OUT WHEN SIGNAL IS ALREADY BLACK
Image = cv2.erode(Image, None, iterations=1)   #SOMETIMES have to mess with the iterations here for more or less noise wiping
Image = cv2.dilate(Image, None, iterations=2)
'''FIND WAY TO ALSO IMPUT THE ABOVE'''

#thresh = cv2.threshold(Image, 200, 255, cv2.THRESH_BINARY)

#Image = cv2.minMaxLoc(Image)
#1.5. Function to set params (not urgent, can be merged with next step for now.)
#2. Function to find blobs within parameters that will find desired target.
def blob_finder(sarimage):
    params = cv2.SimpleBlobDetector_Params()
    # Change thresholds
    #params.minThreshold = 150
    params.maxThreshold =  150  #Could be brought down to ignore clutter from like metal and stuff? Also to deal with rogue giant circles.
    
    
    # Filter by Area.
    params.filterByArea = False
    params.minArea = 20
    params.maxArea = 150
     
    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.785
     
    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.87
     
    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = .1

    # Color Filtering seems to be broken, stop messin with it I guess
    #filterByColor = 1 
    #blobColor = 255
    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create(params)
    blobs = detector.detect(sarimage)
    blob_diameter = blobs[0].size 
    #print (blob_diameter)
    #print (blobs)
    marked_image = cv2.drawKeypoints(sarimage, blobs, np.array([]), [0,0,255], cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) #Spits out image with blobs circled (last argument) in red (second to last argument)
    cv2.imwrite('marked_image.jpg', marked_image)
    blobs_coordinates = (tuple(blobs[0].pt))
    blob_x = blobs_coordinates[0]
    blob_y = blobs_coordinates[1]
     
    return (Image, blob_x, blob_y, blob_diameter)
blob_finder(Image)

 
'''sarimage[479][639] = 2
    for i in range(len(sarimage)):
        for j in range(len(sarimage[i])):
            sarimage[i][j] *= 2'''

    
