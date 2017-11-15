import os, sys
import numpy as np
from scipy import ndimage as ndi
from scipy.misc import imsave
import matplotlib.pyplot as plt
from skimage.filters import sobel, threshold_local
from skimage.morphology import watershed
from skimage import io
import cv2



def open_image(name):
    img=cv2.imread(name,0)
    #cv2.imshow('primera',img)
    #cv2.waitKey(0)

    return img

def adaptive_threshold(image):

    # Create threshold image
    # Offset is not desirable for these images
    block_size = 41
    threshold_img = threshold_local(image, block_size)

    # Binarize the image with the threshold image
    binary_adaptive = image < threshold_img

    # Convert the mask (which has dtype bool) to dtype int
    # This is required for the code in `segmentize` (below) to work
    binary_adaptive = binary_adaptive.astype(int)

    # Return the binarized image
    return binary_adaptive

def segmentize(image):
    # make segmentation using edge-detection and watershed
    edges = sobel(image)
    markers = np.zeros_like(image)
    foreground, background = 1, 2
    markers[image == 0] = background
    markers[image == 1] = foreground

    ws = watershed(edges, markers)
    plt.imshow(ws, interpolation='none')
    plt.show()
    return ndi.label(ws == foreground)


def find_segment(segments, index):
    segment = np.where(segments == index)
    shape = segments.shape

    minx, maxx = max(segment[0].min() - 1, 0), min(segment[0].max() + 1, shape[0])
    miny, maxy = max(segment[1].min() - 1, 0), min(segment[1].max() + 1, shape[1])

    im = segments[minx:maxx, miny:maxy] == index

    return (np.sum(im), np.invert(im))


def run():
    print('Processing:', 1)

    image = open_image('descarga.jpg')
    processed = adaptive_threshold(image)
    segments = segmentize(processed)
    print('Segments detected:', segments[1])

    seg = []
    for s in range(1, segments[1]):
        seg.append(find_segment(segments[0], s))
        #plt.imshow(segments[0], interpolation='none')
        #plt.show()

    seg.sort(key=lambda s: -s[0])

    # Get the directory name (if a full path is given)
    folder = r'celulas'

    # Get the file name
    filenm = 'image'

    # If it doesn't already exist, create a new dir "segments"
    # to save the PNGs
    segments_folder = folder
    os.path.isdir(folder) or os.mkdir(folder)

    # Save the segments to the "segments" directory
    for i in range(len(seg)):
        imsave(os.path.join(segments_folder, filenm + '_' + str(i) + '.png'), seg[i][1]) # Create an MxNx4 array (RGBA)
        seg_rgba = np.zeros((seg[i][1].shape[0],seg[i][1].shape[1],4),dtype=np.bool)

        # Fill R, G and B with copies of the image
        for c in range(3):
            seg_rgba[:,:,c] = seg[i][1]

        # For A (alpha), use the invert of the image (so background is 0=transparent)
        seg_rgba[:,:,3] = ~seg[i][1]

        # Save image
        imsave(os.path.join(segments_folder, filenm[:-4] + '_' + str(i) + '.png'), seg_rgba)





run()
