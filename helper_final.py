import numpy as np
import cv2

# These are all helper functions used by focus_stack_final.py

# Laplacian Pyramid
def get_laplacian_pyramid(img,N):
    """
    returns N-level Laplacian Pyramid of input image as a list
    @input: image
    @output: - Laplacian Pyramid: list of N images containing laplacian pyramids from level 0 to level N
             - Gaussian Pyramid: list of N images containing gaussian pyramids from level 0 to level N
    """
    # current level image
    curr_img = img

    lap_pyramids = []
    gaussian_pyramids = [curr_img,]

    # for N level
    for i in range(N):
        down = cv2.pyrDown(curr_img)
        gaussian_pyramids.append(down)
        up = cv2.pyrUp(down, dstsize=(curr_img.shape[1], curr_img.shape[0]))
        lap = curr_img - up.astype('int16') # NOTE: BE SURE to use int16 instead of cv2.subtract,
                                            #       which cv2 will clip value to 0-255, here we want 
                                            #       arbitratry integeter value.
        lap_pyramids.append(lap)
        curr_img = down
        # top level laplacian be a gaussian downsampled
        if i == N-1:
            lap_pyramids.append(curr_img)

    return lap_pyramids
    
def get_probabilities(gray_image):
    levels, counts = np.unique(gray_image.astype(np.uint8), return_counts = True)
    probabilities = np.zeros((256,), dtype=np.float64)
    probabilities[levels] = counts.astype(np.float64) / counts.sum()
    return probabilities


def _area_entropy(area, probabilities):
    levels = area.flatten()
    return -1. * (levels * np.log(probabilities[levels])).sum()


def entropy(image, kernel_size):
    probabilities = get_probabilities(image)
    pad_amount = int((kernel_size - 1) / 2)
    padded_image = cv2.copyMakeBorder(image,pad_amount,pad_amount,pad_amount,pad_amount,cv2.BORDER_REFLECT101)
    entropies = np.zeros(image.shape[:2], dtype=np.float64)
    offset = np.arange(-pad_amount, pad_amount + 1)
    for row in range(entropies.shape[0]):
        for column in range(entropies.shape[1]):
            area = padded_image[row + pad_amount + offset[:, np.newaxis], column + pad_amount + offset]
            entropies[row, column] = _area_entropy(area, probabilities)

    return entropies


def _area_deviation(area):
    average = np.average(area).astype(np.float64)
    return np.square(area - average).sum() / area.size


# calculates the D: Deviation for every pixel locations
# Source: https://github.com/sjawhar/focus-stacking/blob/master/focus_stack/pyramid.py - Line 108-122
def deviation(image, kernel_size):
    pad_amount = int((kernel_size - 1) / 2)
    padded_image = cv2.copyMakeBorder(image,pad_amount,pad_amount,pad_amount,pad_amount,cv2.BORDER_REFLECT101)
    deviations = np.zeros(image.shape[:2], dtype=np.float64)
    offset = np.arange(-pad_amount, pad_amount + 1)
    for row in range(deviations.shape[0]):
        for column in range(deviations.shape[1]):
            area = padded_image[row + pad_amount + offset[:, np.newaxis], column + pad_amount + offset]
            deviations[row, column] = _area_deviation(area)

    return deviations


def generating_kernel(a):
    kernel = np.array([0.25 - a / 2.0, 0.25, a, 0.25, 0.25 - a / 2.0])
    return np.outer(kernel, kernel)

def convolve(image, kernel=generating_kernel(0.4)):
    return cv2.filter2D(src=image.astype(np.float64), ddepth=-1, kernel=np.flip(kernel))


# calculated RE: regional energy for every pixel locations
# Source: https://github.com/sjawhar/focus-stacking/blob/master/focus_stack/pyramid.py - Line 167-169
def region_energy(laplacian):
    return convolve(np.square(laplacian))