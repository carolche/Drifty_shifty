# Title: FocusStacker_Dedrifter
# AUTHOR: Caroline Berthebaud Cheung
# DATE: 2022/05/23 (YY/MM/DD)
#
# [] =  FocusStacker_Dedrifter(input_dir, output_dir_fs, output_dir_ds, output_dir, output_format, fs=True, image_range_
#       fs=True, ds=True, image_range_ds=True, shift_data=True, pad=True, overwrite=True, parallel=True, crop=True)
#
#     This script is used as a pipeline to run FocusStacker, Drifty_Shifty, and crop_aligned_images sequentially in
#     order to merge slices of an image taken at different focal points into one focused image, to dedrift and align the
#     images, and then to crop and retain only the parts of the images that are visible in every single frame. This
#     script reads images from path='input_dir', focus stacks the images, and saves them into an output directory
#     (output_dir_fs). It then dedrifts these images and saves them into another output directory (output_dir_ds). Since
#     the dedrifting process will create a black border around the images, it may be removed using the
#     crop_aligned_images function, which takes the images in the 'output_dir_ds' directory as input, removes the black
#     border as well as parts of the images that are not in every single frame, and then saves the cropped images in the
#     final output directory (output_dir). All of the edited images will be saved as the given output format
#     (output_format ie. png or tif(f)).
#
#     To be clear, the input and output directories for the three different processes (FocusStacker, Drifty_Shifty,
#     crop_aligned_images) are as follows:
#     1. FocusStacker input directory = input_dir
#     2. FocusStacker output directory = output_dir_fs
#     3. Drifty_Shifty input directory = output_dir_fs
#     4. Drifty_Shifty output directory = output_dir_ds
#     5. crop_aligned_images input directory = output_dir_ds
#     6. crop_aligned_images output directory = output_dir
#
#     This pipeline takes 5 required inputs (input_dir, output_dir_fs, output_dir_ds, output_dir, output_format) and
#     9 optional parameters (image_range_fs, fs, ds, image_range_ds, shift_data, pad, overwrite, parallel, crop) which
#     are all True by default. If you don't want to convert all of your images in your folder, then input a tuple of
#     integers, bracketed and separated by a comma, as the image_range to denote the start and the end of the images to
#     be converted. If you want to just perform FocusStacker, then input ds=False, and if you wish to perform only
#     Drifty_Shifty, then input fs=False.
#
#     By default, "shift_data" is set as True which means that the function calc_shift will be called and a
#     shift array will be calculated. However, if there is already a calculated shift array (saved as
#     "shift_arrays.npz" file), then please move this file into "output_dir_fs" and input the file name as the
#     "shift_data" argument.
#
#     If you want to just calculate the shift array and not dedrift the images, then set pad=False.
#
#     By default, the variable input "overwrite" is set to True, but can be changed to False. This will save subsequent
#     files with the same base name with the addition of sequential numbers at the end.
#
#     User can also define whether to run the functions in parallel (via joblib) or not, denoted here as
#     "parallel", which by default is True but can be set to False.
#
#     Finally, by default, the dedrifted/aligned images will be cropped to remove the black padding created by the
#     dedrifting process and to retain only the parts of the images that are visible in every single frame (via the
#     crop_aligned_images function). But if crop is set to False, this function will not be called.
#
# -------------------------------------------------------------------------------------------------------------------

from FocusStacker_final import FocusStacker
from Drifty_Shifty_final import Drifty_Shifty
from crop_aligned_img_final import crop_aligned_images


def FocusStacker_Dedrifter(input_dir, output_dir_fs, output_dir_ds, output_dir, output_format, fs=True,
                           image_range_fs=True, ds=True, image_range_ds=True, shift_data=True, pad=True, overwrite=True,
                           parallel=True, crop=True):


    if fs == True:
        FocusStacker(input_dir, output_dir_fs, output_format, parallel=True, image_range_fs=True,
                     overwrite=True)
    if ds == True:
        Drifty_Shifty(output_dir_fs, output_dir_ds, output_format, image_range_ds=True, shift_data=True,
                      pad=True, overwrite=True, parallel=True)
    if crop == True:
        crop_aligned_images(output_dir_ds, output_dir, output_format)



if __name__ == '__main__':
    input_dir = ""
    output_dir_fs = ""
    output_dir_ds = ""
    output_dir = ""
    output_format = ""

    FocusStacker_Dedrifter(input_dir, output_dir_fs, output_dir_ds, output_dir, output_format)