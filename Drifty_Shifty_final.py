# Title: DRIFTY_SHIFTY
# AUTHOR: Caroline Berthebaud Cheung
# DATE: 2022/04/01 (YY/MM/DD)
#
# [] = Drifty_Shifty(input_dir, output_dir, output_format, image_range = True,
#                   shift_data = True, pad = True, overwrite = True, parallel=True)
#
#     Based on drifty_shifty.ma by Dr. Andrew Utada, which was in turn based on
#     drifty_shifty_deluxe (a script)). This script computes the shift from a
#     sequence of images (path: input_dir), pads the images and saves them to an output directory
#     (output_dir) with a given output extension (output_format ie. png, tif, and tiff).
#
#     Optionally, a range of images in the original directory can be given as a variable
#     input, "image_range", which requires a tuple of values as input.
#
#     By default, "shift_data" is set as True which means that the function calc_shift will be called
#     and a new set of shift arrays will be calculated. However, if there is already a set of calculated
#     shift arrays (saved as an "npz" file), then please put this file into the input directory that holds the images
#     and input the file name as the "shift_data" argument.
#
#     By default, variable input "overwrite" is set to True, but can be changed to False. This will save subsequent
#     files with the same base name with the addition of sequential numbers at the end.
#
#     User can also define whether to run the functions in parallel (via joblib) or not, denoted here as
#     "parallel", which by default is True but can be set to False.

#
# -------------------------------------------------------------------------------------------------------------------
# DETAILED EXPLANATION.
# I. Fourier transformation to power spectrum to determine drift.
#     1. x domain shift f(x-a) transforms to F(w)exp(-iaw)
#     2. Find a, given f(x) and f(x-a)
#     3. F(w)*conj(F(w)exp(-iaw)) gives |F(w)|^2*exp(iaw) (keeping shift but discarding phase info in image)
#     4. ifft of |F(w)| is maximum at zero because all components are in phase there.
#     5. ifft of the whole thing is shifted by a, so identify the location of the maximum.
# II. Padding and shift values are generated and saved as arrays in "npz" format.
# III.Shift data is opened and loaded, and then each image in the input directory is opened,
#     padded (to shift the image), and saved in the output directory in the output format.
#
#
# The current script was translated from the matlab code written by Andrew Utada, University of
# Tsukuba/TARA Center, which was in turn modified from the base code written by:
# Josh Sugar and Dave Robinson, Sandia National Labs Copyright 2014 Sandia Corporation.
# Under the terms of Contract DE-AC04-94AL85000, there is a non-exclusive license for use of this work by
# or on behalf of the U.S. Government. Export of this program may require a
# license from the United States Government. Please cite the Microscopy
# Today article _blank_ if you use this script.
#
# ***********************************************************************************************
#
#
# EXAMPLE USAGE
#
# 1. Drifty_Shifty(input_dir, output_dir, output_format='png')
# -->This is the standard usage. It will read and process all images in the "input_dir",
# calculate the drift array which is saved in the "input_dir", and then pad/dedrift the images which are saved in the
# "output_dir" directory as the "output_format" (png in this case). If the directory already has images,
# the script will continue from where it left off until all the images are processed, and if the "output_dir" is full
# of images already, the script will automatically overwrite the previous images. Further, the program will be run in
# parallel.
#
# 2. Drifty_Shifty(input_dir, output_dir, output_format='tif', image_range=(0,100))
# -->Same as before but this time, only chooses the first 101 images to process, and outputs tif files.
#
#
# 3. Drifty_Shifty(input_dir, output_dir, output_format='tif', image_range=(300,1000), shift_data='shift_arrays.npz',
#  overwrite=False)
# -->Same as before but this time, only processes images 300-1000, and doesn't calculate the shift array because
# a previously calculated array will be used. Also, if there were images in the 'output_dir' already, the images will
# not be overwritten.
#
#
# 4. Drifty_Shifty(input_dir, output_dir, output_format='tif', pad=False, parallel=False)
# -->This time, the script will only produce the shift array and will not perform the padding/dedrifting of the images.
# Further, the code will run serially and not in parallel so will be slower.

# ***********************************************************************************************

# Here are all the relevant imports:
import numpy as np
import cv2
import os
import glob
import sys
from timeit import default_timer as timer
import scipy.fft as fft
from joblib import Parallel, delayed
from iteration_utilities import deepflatten



# This function takes 3 required inputs and 5 optional inputs (all set to True). If you don't want to process all
# images in your folder, then just input a tuple of 2 integers, bracketed and separated by a comma, as the argument
# for "image_range" to denote the start and the end of the image range.
# By default, shift_data is True, so it will run the calc_shift functions and save the shift array as an .npz file into
# the "input_dir". However, if you already have a shift array saved somewhere (usually an .npz file), then put it into
# the "input_dir" and input the file name as argument for shift_data when calling the function. This script will by
# default run in parallel via joblib multiprocessing function.


# Step 1: Calculate shift x,y pairs for each frame. If 'shift_data=True' and 'pad=False', the code will just produce
# the shift array and will not process the images further to dedrift.
def get_ref(images):

    # Get and process reference frame (first one in the sequence)
    frameref = cv2.imread(images[0])
    if frameref.shape[2] == 3:
        frameref = cv2.cvtColor(frameref, cv2.COLOR_BGR2GRAY)
    fft_ref = fft.fft2(frameref)

    vidHeight = frameref.shape[1]
    vidWidth = frameref.shape[0]  # The blank variable here gets rid of extra padding - we didn't do this in python!!
    centery = (vidHeight / 2) + 1
    centerx = (vidWidth / 2) + 1

    return fft_ref, vidHeight, vidWidth, centery, centerx


# this function performs fourier transformation for each image and returns the maximum x and y indices
def calc_shift(images, fft_ref):

    img = cv2.imread(images)
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Calculate fourier transformation of each image
    fft_frame = fft.fft2(img)

    # vector multiplication of the fourier-transformed image reference with the
    # complex conjugate array of each fourier-transformed image
    prod = fft_ref * np.conjugate(fft_frame)

    # get inverse fourier transformation of the product
    # need to get the "real" numbers and not the imaginary numbers
    cc = (fft.ifft2(prod)).real

    # 'fftshift' moves corners to center, 'max()' gives largest element in the whole array, and
    # 'where' returns indices of that point
    maxYX = np.where(fft.fftshift(cc) == np.max(cc))

    return maxYX


# this function then takes the maximum x and y indices to calculate the x-y shift array
def calc_shift2(images, maxYX, vidHeight, vidWidth, centery, centerx):

    nFrames = len(images)

    shifty = np.zeros((nFrames,))
    shiftx = np.zeros((nFrames,))

    maxYX2 = list(deepflatten(maxYX))
    maxY = maxYX2[::2]
    maxX = maxYX2[1::2]

    i=0
    for i in range(nFrames):

        shifty[i] = maxY[i] - centery
        shiftx[i] = maxX[i] - centerx

        # Previous version didn't subtract center point here
        if i > 0:  # Checks to see if there is an ambiguity problem with FFT because of the periodic boundary in FFT
            if np.abs(shifty[i] - shifty[i - 1]) > vidHeight / 2:
                shifty[i] = shifty[i] - np.sign(shifty[i] - shifty[i - 1]) * vidHeight

            if np.abs(shiftx[i] - shiftx[i - 1]) > vidWidth / 2:
                shiftx[i] = shiftx[i] - np.sign(shiftx[i] - shiftx[i - 1]) * vidWidth

        i=i+1

    return shifty, shiftx


# Step 2: Pads and defrifts images

# This function is the core function and actually pads, centers, and dedrifts the images according to the calculated
# shift data. It will take the shift array saved as an .npz file in the 'input_dir' and dedrift the images accordingly.
def pad_images(images, shift_arrays, output_dir, output_format, overwrite=True):

    # this will load the shift_data from the calc_shift function
    with np.load(shift_arrays) as data:
        shiftx = data['x']
        shifty = data['y']

    # number of images
    nFrames = len(images)

    # Get Height & Width of reference image (first one in the sequence)
    frameref = cv2.imread(images[0])
    if frameref.shape[2] == 3:
        frameref = cv2.cvtColor(frameref, cv2.COLOR_BGR2GRAY)
    frameref = frameref.astype(dtype='uint8')
    vidHeight, vidWidth = frameref.shape[0:2]

    # Pad the images. Use first image as "center"
    newsizey = round(2 * np.max(np.abs(shifty)) + vidHeight)
    newsizex = round(2 * np.max(np.abs(shiftx)) + vidWidth)

    # Assume max positive shift = max negative shift; centers reference frame
        # This was the original code but for some reason works for some but not all sets of images
        # midindexy = (newsizey - vidHeight) / 2 + 1
        # midindexx = (newsizex - vidWidth) / 2 + 1
    midindexy = (newsizey - vidHeight) / 2
    midindexx = (newsizex - vidWidth) / 2

    # Determine how many images are in the output directory in case run was stopped while in progress
    files_in_outputdir = glob.glob(os.path.join(output_dir, f"*_dedrifted*.{output_format}"))
    num_files_in_outputdir = len(files_in_outputdir)

    # If the 'output_dir' does not contain any images or contains the entire set of dedrifted images, it will start
    # processing the images from the beginning.
    # If the 'output_dir' contains some of the dedrifted images but not all from the 'input_dir', it will continue
    # processing the images where it left off.
    if num_files_in_outputdir == (0 or nFrames):
        range_of_images = range(nFrames)
    else:
        range_of_images = range(num_files_in_outputdir, nFrames)

    # The following code takes the image and shifts it according to the shift array in a frame padded with a black
    # border if overwrite is False. Newly dedrifted images will be saved with an extra number at the end if the same
    # file already exists in the 'output_dir'
    for i in range_of_images:
        frame_shift = np.zeros((newsizey, newsizex), dtype='uint8')

        img = cv2.imread(images[i])
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # For every image, want to shift the frame according to shifty/shiftx and center and pad it.
        # starty/x and endy/x are the coordinates inside the frame_shift frame in which to place the image (img)
        starty = (midindexy + shifty[i]).astype(int)
        endy   = (midindexy + shifty[i] + (vidHeight)).astype(int)
        startx = (midindexx + shiftx[i]).astype(int)
        endx   = (midindexx + shiftx[i] + (vidWidth)).astype(int)
        frame_shift[starty:endy, startx:endx] = img

        # This file is the corrected image and is subsequently saved
        dedrifted = np.round_(frame_shift)

        # This code saves the dedrfited images into the output directory. If overwrite is False, then newly saved
        # images will not overwrite files with the same name already in the output directory.
        if overwrite == False:
            a = glob.glob(os.path.join(output_dir, f"{images[i].rsplit('.')[0]}_dedrifted*.{output_format}"))
            b = len(a)
            if b == 0:
                cv2.imwrite(os.path.join(output_dir, f"{images[i].rsplit('.')[0]}_dedrifted.{output_format}"), dedrifted)
            elif b == 1:
                cv2.imwrite(os.path.join(output_dir, f"{images[i].rsplit('.')[0]}_dedrifted1.{output_format}"),
                            dedrifted)
            else:
                cv2.imwrite(os.path.join(output_dir, f"{images[i].rsplit('.')[0]}_dedrifted{b}.{output_format}"),
                            dedrifted)
        else:
            cv2.imwrite(os.path.join(output_dir, f"{images[i].rsplit('.')[0]}_dedrifted.{output_format}"), dedrifted)

    # This code will print out how many images are done to determine progress
        if i % 50 == 0:
            print(f'{i} frames out of {nFrames} are done')

        i=i+1

    return None



# Step 3: Call all of the functions using the main function
def Drifty_Shifty(input_dir, output_dir, output_format,
                  image_range_ds=True, shift_data="True", pad=True, overwrite=True, parallel=True):

    start = timer()
    print(f'start shifting')

    # define current working dir as cwd
    cwd = os.curdir

    # Change the working directory to the input directory
    os.chdir(input_dir)

    # Get all the individual files in the input directory
    files = sorted(os.listdir(input_dir))

    # These are all the accepted types of extensions
    expected_ext = ['png', 'tif', 'tiff']

    # Determine input format type
    fileNames = [img for img in files if (img.split(".")[-1].lower() in expected_ext and img[0].isalnum())]

    # in case someone accidentally inputs another type of format (ie. jpg), the output format will be tif
    if output_format not in expected_ext:
        output_format = 'tif'


    # If you don't want to convert all of your images in your folder, then input a tuple of integers as image_range.
    # Input 2 integers (bracketed and separated by a comma) to denote the start and the end of the images to be
    # converted. If you do not input exactly 2 integers, an error will be raised. If image_range is True,
    # all the files in the folder will be passed into the function.
    if image_range_ds != True:
        if len(image_range_ds)!=2:
            sys.exit("image_range doesn't exist. Please input a tuple of two values.")
        else:
            fileNames = fileNames[image_range_ds[0]:image_range_ds[1]]

    # this code calls the functions to calculate the shift array and save it as an .npz file in the 'input_dir'.
    # If shift_data is not True and is instead a path to an .npz file that contains the shift data, then the code
    # will bypass this part and go directly to pad images.
    if shift_data == "True":
        fft_ref, vidHeight, vidWidth, centery, centerx = get_ref(fileNames)
        if parallel == False:
            # Serial processing
            maxYX = [calc_shift(fileNames[i], fft_ref) for i in range(len(fileNames))]
            shift_arrays = calc_shift2(fileNames, maxYX, vidHeight, vidWidth, centery, centerx)
        else:
            # Joblib multiprocessing
            maxYX = Parallel(n_jobs=-1, prefer="threads")(delayed(calc_shift)(fileNames[i], fft_ref)
                                                          for i in range(len(fileNames)))
            shift_arrays = calc_shift2(fileNames, maxYX, vidHeight, vidWidth, centery, centerx)


        # if overwrite is False, then any previously saved shift arrays will not be overwritten and new arrays will
        # instead have an extra number at the end.
        if overwrite == False:
            a = glob.glob('shift_arrays*.npz')
            b = len(a)
            if b == 0:
                np.savez('shift_arrays.npz', x=shift_arrays[1], y=shift_arrays[0])
                shift_arrays = 'shift_arrays.npz'
            elif b == 1:
                np.savez(f'shift_arrays1.npz', x=shift_arrays[1], y=shift_arrays[0])
                shift_arrays = 'shift_arrays1.npz'
            else:
                np.savez(f'shift_arrays{b}.npz', x=shift_arrays[1], y=shift_arrays[0])
                shift_arrays = f'shift_arrays{b}.npz'
        else:
            np.savez('shift_arrays.npz', x=shift_arrays[1], y=shift_arrays[0])
            shift_arrays = 'shift_arrays.npz'
    # but if already have a shift array for this particular set of images saved somewhere, then put that file into the
    # input_dir and input path as argument for shift_arrays
    else:
        print('importing shift arrays')
        shift_arrays = shift_data
    end = timer()
    print(f'elapsed time: {end - start}')

    # use this function to actually shift the images in the frame with a black padding
    if pad == True:
        start = timer()
        print(f'start padding')

        pad_images(fileNames, shift_arrays, output_dir, output_format, overwrite)

        end = timer()
        print(f'elapsed time: {end - start}')


    # change the working directory back to the original one
    os.chdir(cwd)

    print('dedrifting successful')
    return None




if __name__ == '__main__':
    input_dir = ""
    output_dir = ""
    output_format = ""
    shift_data =""

    Drifty_Shifty(input_dir, output_dir, output_format, shift_data="True")
