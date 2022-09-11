# Title: FocusStacker
# AUTHOR: Caroline Berthebaud Cheung
# DATE: 2022/05/23 (YY/MM/DD)
#
# [] = FocusStacker(input_dir, output_dir, output_format, parallel=True)
#
#     Based on focus-stacking (laplacian pyramid fusion method) by Zongnan Bao and Han Chen,  for their final project
#     of CS445 in Fall2020. This script achieves the functionality of focus stacking (stack photos with different depth
#     of fields) using the Laplacian Pyramid Fusion method as described in Wang and Chang's article
#     (Wencheng Wang and Faliang Chang.  A Multi-focus Image Fusion Method Based on Laplacian Pyramid.
#     J. Comput. 2011, V.6: 2559-2566).
#
#     This script takes 3 required inputs and 2 optional input. The 'input_dir' is the directory which holds all of
#     the images that need to be focus stacked. The 'output_dir' is the directory into which the focus stacked images
#     will be saved. The 'output_format' can be either png or tif(f), although png images look a bit better because
#     the images saved as tif(f)s tend to have differing contrasts. Lastly, the default 'parallel' parameter is True
#     which will make the function run in parallel via joblib, and if parallel is False, the script will run serially.
#     If you don't want to convert all of your images in your folder, then input a tuple of integers as image_range.
#     Input 2 integers (bracketed and separated by a comma) to denote the start and the end of the images to be
#     converted.

#
# -------------------------------------------------------------------------------------------------------------------
# DETAILED EXPLANATION.
# I.  Laplacian pyramid fusion
#     Takes two parameters, N = depth of Laplacian pyramid (default is 5), and kernel_size = integer represents
#     the side length of the Gaussian kernel (default is 5).
#     1. Generate an array of Laplacian pyramids (default N = 5)
#     2. Regional fusion using these Laplacian pyramids. Fuse level based on Laplacian pyramid (N=5), D=deviation,
#        E=entropy (both of which depend on kernel_size [default 5]).
#     3. Reconstruct final Laplacian pyramid back to original image by getting the top level of the Gaussian pyramid
#        and combining with each level of the Laplacian pyramid
# II. Recreating image and saving file.
#     1. Transform the fused image as an RGB array.
#     2. Save into output directory as grayscale.
#
# ***********************************************************************************************
#
#
# EXAMPLE USAGE
#
# 1. FocusStacker(input_dir, output_dir, output_format='png')
# -->This is the standard usage. It will read and process all images in the "input_dir", and save the focus stacked
# images in the "output_dir" directory as the "output_format" (png in this case). The images that are saved as png have
# better quality than those saved as tif(f) due to contrast issues in the latter. If the directory already has images,
# the script will continue from where it left off until all the images are processed, and if the "output_dir" is full
# of images already, the script will automatically overwrite the previous images. Further, the program will by default
# run in parallel.
#
# 2. FocusStacker(input_dir, output_dir, output_format='png', image_range=(5,200)
# -->In this example, only images 5-200 in the "input_dir" will be processed and then saved images in the "output_dir"
# directory as the "output_format" (png in this case).

# ***********************************************************************************************

# Here are all the relevant imports:
import numpy as np
import cv2
from joblib import Parallel, delayed
from timeit import default_timer as timer
import itertools
import os
import sys
import glob
# from helper_final import get_laplacian_pyramid, entropy, deviation, region_energy

intro = \
"""
Focus Stacking

This project is the final project of CS445 Fall2020,
Team: Zongnan Bao(zb3) and Han Chen(hanc3)\n\n
"""

simple = \
"""
stack photos with different depth of fields
"""


# Laplacian Pyramid
def get_laplacian_pyramid(img, N):
    """
    returns N-level Laplacian Pyramid of input image as a list
    @input: image
    @output: - Laplacian Pyramid: list of N images containing laplacian pyramids from level 0 to level N
             - Gaussian Pyramid: list of N images containing gaussian pyramids from level 0 to level N
    """
    # current level image
    curr_img = img

    lap_pyramids = []
    gaussian_pyramids = [curr_img, ]

    # for N level
    for i in range(N):
        down = cv2.pyrDown(curr_img)
        gaussian_pyramids.append(down)
        up = cv2.pyrUp(down, dstsize=(curr_img.shape[1], curr_img.shape[0]))
        lap = curr_img - up.astype('int16')  # NOTE: BE SURE to use int16 instead of cv2.subtract,
        #       which cv2 will clip value to 0-255, here we want
        #       arbitratry integeter value.
        lap_pyramids.append(lap)
        curr_img = down
        # top level laplacian be a gaussian downsampled
        if i == N - 1:
            lap_pyramids.append(curr_img)

    return lap_pyramids


def get_probabilities(gray_image):
    levels, counts = np.unique(gray_image.astype(np.uint8), return_counts=True)
    probabilities = np.zeros((256,), dtype=np.float64)
    probabilities[levels] = counts.astype(np.float64) / counts.sum()
    return probabilities


def _area_entropy(area, probabilities):
    levels = area.flatten()
    return -1. * (levels * np.log(probabilities[levels])).sum()


def entropy(image, kernel_size):
    probabilities = get_probabilities(image)
    pad_amount = int((kernel_size - 1) / 2)
    padded_image = cv2.copyMakeBorder(image, pad_amount, pad_amount, pad_amount, pad_amount, cv2.BORDER_REFLECT101)
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
    padded_image = cv2.copyMakeBorder(image, pad_amount, pad_amount, pad_amount, pad_amount, cv2.BORDER_REFLECT101)
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


#focus-stacking (laplacian pyramid fusion method)
def lap_focus_stacking(images, N=5, kernel_size=5):
    """
    achieves the functionality of focus stacking using Laplacian Pyramid Fusion described 
        in Wang and Chang's 2011 paper (regional fusion)
    @input: images - array of images
            N      - Depth of Laplacian Pyramid, default is 5
            kernel_size - integer represents the side length of Gaussian kernel, default is 5
    @output: single image that stacked the depth of fields of all images
    """

    # 1- Generate array of Laplacian pyramids
    list_lap_pyramids = np.array([get_laplacian_pyramid(img, N)[:-1] for img in images], dtype=object)

    LP_f = []


    # 2 - Regional fusion using these Laplacian pyramids
    # fuse level = N laplacian pyramid, D=deviation, E=entropy
    D_N = np.array([deviation(lap, kernel_size) for lap in list_lap_pyramids[:, -1]])
    E_N = np.array([entropy(lap, kernel_size) for lap in list_lap_pyramids[:, -1]])

    # 2.1 - init level N fusion canvas
    LP_N = np.zeros(list_lap_pyramids[0, -1].shape)
    for m in range(LP_N.shape[0]):
        for n in range(LP_N.shape[1]):
            D_max_idx = np.argmax(D_N[:, m, n])
            E_max_idx = np.argmax(E_N[:, m, n])
            D_min_idx = np.argmin(D_N[:, m, n])
            E_min_idx = np.argmin(E_N[:, m, n])
            # if the image maximizes BOTH the deviation and entropy, use the pixel from that image
            if D_max_idx == E_max_idx:
                LP_N[m, n] = list_lap_pyramids[D_max_idx, -1][m, n]
            # if the image minimizes BOTH the deviation and entropy, use the pixel from that image
            elif D_min_idx == E_min_idx: 
                LP_N[m, n] = list_lap_pyramids[D_min_idx, -1][m, n]
            # else average across all images
            else:
                for k in range(list_lap_pyramids.shape[0]):
                    LP_N[m, n] += list_lap_pyramids[k, -1][m, n]
                LP_N[m, n] /= list_lap_pyramids.shape[0]

    LP_f.append(LP_N)

    # 2.2 - Fusion other levels of Laplacian pyramid (N-1 to 0)
    for l in reversed(range(0, N-1)):
        # level l final laplacian canvas
        LP_l = np.zeros(list_lap_pyramids[0, l].shape)

        # region energy map for level l
        RE_l = np.array([region_energy(lap) for lap in list_lap_pyramids[:, l]], dtype=object)

        for m in range(LP_l.shape[0]):
            for n in range(LP_l.shape[1]):
                RE_max_idx = np.argmax(RE_l[:, m, n])
                LP_l[m, n] = list_lap_pyramids[RE_max_idx, l][m, n]

        LP_f.append(LP_l)

    LP_f = np.array(LP_f, dtype=object)
    LP_f = np.flip(LP_f)


    # 3 - time to reconstruct final laplacian pyramid(LP_f) back to original image!
    # get the top-level of the gaussian pyramid
    for img in images:
        base = get_laplacian_pyramid(img, N)[-1]
    fused_img = cv2.pyrUp(base, dstsize=(LP_f[-1].shape[1], LP_f[-1].shape[0])).astype(np.float64)

    for i in reversed(range(N)):
        # combine with laplacian pyramid at the level
        fused_img += LP_f[i]
        if i != 0:
            fused_img = cv2.pyrUp(fused_img, dstsize=(LP_f[i-1].shape[1], LP_f[i-1].shape[0]))

    return fused_img


# Recreates the stacked image and saves it into output_dir
def merged_focus(group, output_dir_fs, output_format, overwrite=True):

    # 1 - load images (in GRAY)
    image = [cv2.imread(g) for g in group]
    if image[0].shape[2] == 3:
        images = np.array([cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in image])
    else:
        images = np.array([img for img in image])

    # defines the base name in order to name the files correctly
    z = group[0].rfind('z')
    names = [g[:z] for g in group][0]

    # check the filenames are valid
    if any([image is None for image in images]):
        raise RuntimeError("Cannot load one or more input files.")

    # 2 - focus stacking by first creating fused image as RGB image
    RGB_images = np.array([img for img in images])
    canvas = np.array([lap_focus_stacking(RGB_images[:, :, :])])
    canvas = np.moveaxis(canvas, 0, -1)

    # 3 - write to file (grayscale)
    if overwrite == False:
        a = glob.glob(os.path.join(output_dir_fs, f"{names}_merged.{output_format}"))
        b = len(a)
        if output_format.lower() == 'png':
            if b == 0:
                cv2.imwrite(os.path.join(output_dir_fs, f'{names}_merged.{output_format}'), canvas)
            elif b == 1:
                cv2.imwrite(os.path.join(output_dir_fs, f'{names}_merged1.{output_format}'), canvas)
            else:
                cv2.imwrite(os.path.join(output_dir_fs, f'{names}_merged{b}.{output_format}'), canvas)
        else:
            canvas2 = cv2.normalize(src=canvas, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            if b == 0:
                cv2.imwrite(os.path.join(output_dir_fs, f'{names}_merged.{output_format}'), canvas2)
            elif b == 1:
                cv2.imwrite(os.path.join(output_dir_fs, f'{names}_merged1.{output_format}'), canvas2)
            else:
                cv2.imwrite(os.path.join(output_dir_fs, f'{names}_merged{b}.{output_format}'), canvas2)
    else:
        if output_format.lower() == 'png':
            cv2.imwrite(os.path.join(output_dir_fs, f'{names}_merged.{output_format}'), canvas)
        else:
            canvas2 = cv2.normalize(src=canvas, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            cv2.imwrite(os.path.join(output_dir_fs, f'{names}_merged.{output_format}'), canvas2)

    return None


# This is the main function that calls all other functions.
def FocusStacker(input_dir, output_dir_fs, output_format, parallel=True, image_range_fs=True, overwrite=True):

    start = timer()
    print('start merging')

    # current working dir
    cwd = os.curdir

    # change working dir to image directory
    os.chdir(input_dir)

    # These are all the accepted types of extensions
    expected_ext = ['png', 'tif', 'tiff']

    # sorting and grouping images according to the base name and the number of slices (z)
    image_files = sorted(os.listdir(input_dir))
    file_names = [img for img in image_files if img.split(".")[-1].lower() in expected_ext]

    # If you don't want to convert all of your images in your folder, then input a tuple of integers as image_range.
    # Input 2 integers (bracketed and separated by a comma) to denote the start and the end of the images to be
    # converted. If you do not input exactly 2 integers, an error will be raised. If image_range is True,
    # all the files in the folder will be passed into the function.
    if image_range_fs != True:
        if len(image_range_fs)!=2:
            sys.exit("image_range doesn't exist. Please input a tuple of two values.")
        else:
            file_names = file_names[image_range_fs[0]:image_range_fs[1]]

    z = file_names[0].rfind('z')
    groups = [list(g) for _, g in itertools.groupby(sorted(file_names), lambda x: x[0:z])]

    # determines how many slices (z - images with different focus) in each group
    for group in groups:
        num_of_zplane_images = len(group)

    # input sanity checks
    num_files = len(file_names)
    assert num_files > 1, "Provide at least 2 images."

    # determines the number of files already in output directory
    output_files = os.listdir(output_dir_fs)
    if len(output_files) != (0 or len(file_names)/num_of_zplane_images):
        output_files2 = [output_file.split('_merged')[0] for output_file in output_files]
        file_names2 = [f for f in file_names if f[0:z] not in output_files2]
        groups = [list(g) for _, g in itertools.groupby(sorted(file_names2), lambda x: x[0:z])]


    # If you want to run the main focus stacking function, merged_focus, serially which would be slower
    if parallel == False:
        [merged_focus(group, output_dir_fs, output_format, overwrite) for group in groups]
    else:
        # run the main focus stacking function, merged_focus, in parallel with joblib
        Parallel(n_jobs=-1)(delayed(merged_focus)(group, output_dir_fs, output_format, overwrite) for group in groups)

    # change working dir back to original working directory
    os.chdir(cwd)
    end = timer()
    print(f'elasped time {end-start}, Focus Stacking successful')
    return None


if __name__ == "__main__":

    input_dir = "/Volumes/Caro2/scene2_8bit3"
    output_dir_fs = "/Volumes/Caro2/scene2_8bit3_fs"
    output_format = 'png'

    # call the function
    FocusStacker(input_dir, output_dir_fs, output_format, parallel=True, image_range_fs=True, overwrite=True)
