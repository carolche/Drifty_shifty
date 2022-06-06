# Title: master_main
# AUTHOR: Caroline Berthebaud Cheung
# DATE: 2022/05/23 (YY/MM/DD)
#
# [] =  master_main(input_dir, output_dir_fs, output_dir_ds, output_dir, output_format, fs=True, image_range_fs=True,
#       ds=True, image_range_ds=True, shift_data=True, pad=True, overwrite=True, parallel=True)
#
#     This script is used as a pipeline to run focusstacking, drifty_shifty, and crop_aligned_images sequentially in
#     order to merge slices of an image taken at different focal points into one focused image, to dedrift and align the
#     images, and then to crop and retain only the parts of the images that are visible in every single frame. This
#     script reads images from path='input_dir', focus stacks the images, and saves them into an output directory
#     (output_dir_fs). It then dedrifts these images and saves them into another output directory (output_dir_ds). Since
#     the dedrifting process will create a black border around the images, we need to remove the black padding using the
#     crop_aligned_images function, which takes the images in the 'output_dir_ds' directory as input, removes the black
#     border as well as parts of the images that are not in every single frame, and then saves the cropped images in the
#     final output directory (output_dir). All of the edited images will be saved as the given output format
#     (output_format ie. png or tif(f)).
#
#     To be clear, the input and output directories for the three different processes (focusstacking, drifty_shifty,
#     crop_aligned_images) are as follows:
#     1. focusstacking input directory = input_dir
#     2. focusstacking output directory = output_dir_fs
#     3. drifty_shifty input directory = output_dir_fs
#     4. drifty_shifty output directory = output_dir_ds
#     5. crop_aligned_images input directory = output_dir_ds
#     6. crop_aligned_images output directory = output_dir
#
#     This pipeline takes 5 required inputs (input_dir, output_dir_fs, output_dir_ds, output_dir, output_format) and
#     8 optional parameters (image_range_fs, fs, ds, image_range_ds, shift_data, pad, overwrite, parallel) which are all
#     True by default. If you don't want to convert all of your images in your folder, then input as image_range (a) in
#     Pycharm: a tuple of integers, bracketed and separated by a comma, or (b) by command line: 2 integers separated by
#     a space, to denote the start and the end of the images to be converted. If you want to just perform focusstacking,
#     then input ds=False, and if you wish to perform only drifty_shifty, then input fs=False.
#
#     By default, "shift_data" is set as True which means that the function calc_shift will be called and a new set of
#     shift arrays will be calculated. However, if there is already a set of calculated shift arrays (saved as
#     "shift_arrays.npz" file), then please put this file into "output_dir_fs" and input the file name as the
#     "shift_data" argument.
#
#     If you want to just calculate the shift array and not dedrift the images, then set pad=False.
#
#     By default, variable input "overwrite" is set to True, but can be changed to False. This will save subsequent
#     files with the same base name with the addition of sequential numbers at the end.
#
#     User can also define whether to run the functions in parallel (via joblib) or not, denoted here as
#     "parallel", which by default is True but can be set to False.
#
#     Finally, the dedrifted,aligned images will be cropped to remove the black padding created by the dedrifting
#     process and to retain only the parts of the images that are visible in every single frame (via the
#     crop_aligned_images function).
#
# -------------------------------------------------------------------------------------------------------------------

from focus_stack_final import focusstacking
from drifty_shifty_final import drifty_shifty
from crop_aligned_img_final import crop_aligned_images


def master_main(input_dir, output_dir_fs, output_dir_ds, output_dir, output_format, fs=True, image_range_fs=True,
                ds=True, image_range_ds=True, shift_data=True, pad=True, overwrite=True, parallel=True):


    if fs == True:
        focusstacking(input_dir, output_dir_fs, output_format, parallel=True, image_range_fs=True,
                      overwrite=True)
    if ds == True:
        drifty_shifty(output_dir_fs, output_dir_ds, output_format, image_range_ds=True, shift_data=True,
                      pad=True, overwrite=True, parallel=True)
        crop_aligned_images(output_dir_ds, output_dir, output_format)



if __name__ == '__main__':
    input_dir = "/Volumes/Caro2/finalstack_orig"
    output_dir_fs = "/Volumes/Caro2/finalstack_orig"
    output_dir_ds = "/Volumes/Caro2/finalstack_dedrift"
    output_dir = "/Volumes/Caro2/finalstack_crop"
    output_format = 'png'
    foo = 'shift_arrays.npz'

    master_main(input_dir, output_dir_fs, output_dir_ds, output_dir, output_format, fs=False)