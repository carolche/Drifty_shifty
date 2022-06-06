# Title: master_main
# AUTHOR: Caroline Berthebaud Cheung
# DATE: 2022/05/23 (YY/MM/DD)
#
# [] =  master_main(input_dir, output_dir_fs, output_dir_ds, output_dir, output_format, image_range_fs=True, fs=True,
#       ds=True, image_range_ds=True, shift_data=True, pad=True, overwrite=True, parallel=True)
#
#     This script is used as a pipeline to run focusstacking and drifty_shifty sequentially in order to merge slices of
#     an image taken at different focal points into one focused image and then to dedrift the images. This script reads
#     images from path='input_dir', focus stacks the images, and saves them into an output directory (output_dir_fs). It
#     then dedrifts these images and saves them into another output directory (output_dir_ds). Since the dedrifting
#     process will create a black border around the images, we need to remove the black padding using the
#     main_remove_black_border function, which takes the images in the 'output_dir_ds' directory as input, removes the
#     black border, and then saves the cropped images in the final output directory (output_dir). All of the edited
#     images will be saved as the given output format (output_format ie. png or tif(f)).
#
#     To be clear, the input and output directories for the three different processes (focusstacking, drifty_shifty,
#     remove_black_border) are as follows:
#     1. focusstacking input directory = input_dir
#     2. focusstacking output directory = output_dir_fs
#     3. drifty_shifty input directory = output_dir_fs
#     4. drifty_shifty output directory = output_dir_ds
#     5. remove_black_border input directory = output_dir_ds
#     6. remove_black_border output directory = output_dir
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
# -------------------------------------------------------------------------------------------------------------------

from focus_stack_final import focusstacking
from drifty_shifty_final import drifty_shifty
from remove_black_border import main_remove_black_border
from argparse import ArgumentParser


def master_main(input_dir, output_dir_fs, output_dir_ds, output_dir, output_format, image_range_fs=True,
                fs=True, ds=True, image_range_ds=True, shift_data=True, pad=True, overwrite=True, parallel=True):

    parser = ArgumentParser(prog="Tool to focus stack and dedrift a list of images.")

    parser.add_argument(
        "-i",
        "--input_dir",
        help="directory of images to focus stack",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-o", "--output_dir_fs",
        help="directory to save output image of focusstacking and input directory of drifty_shifty",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-o", "--output_dir_ds",
        help="directory to save output image of drifty_shifty and input directory of remove_black_border",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-o_d", "--output_dir", help="directory to save output image of remove_black_border", required=True, type=str,
    )
    parser.add_argument(
        "-o_f", "--output_format", help="output format", required=True, type=str,
    )
    parser.add_argument(
        "-i_r_fs", "--image_range_fs", help="image range of focusstacking", default=True, required=False, nargs='+',
        type=int,
    )
    parser.add_argument(
        "-fs",
        "--fs",
        help="will run focusstacking if True",
        default=True,
        required=False,
        type=str,
    )
    parser.add_argument(
        "-ds",
        "--ds",
        help="will run drifty_shifty if True",
        default=True,
        required=False,
        type=str,
    )
    parser.add_argument(
        "-i_r_ds", "--image_range_ds", help="image range of drifty_shifty", default=True, required=False, nargs='+',
        type=int,
    )
    parser.add_argument(
        "-s",
        "--shift_data",
        help="will calculate shift array if True",
        default=True,
        required=False,
        type=str,
    )
    parser.add_argument(
        "-p",
        "--pad",
        help="will pad and dedrift image if True",
        default=True,
        required=False,
        type=str,
    )
    parser.add_argument(
        "-ov",
        "--overwrite",
        help="will overwrite files if True",
        default=True,
        required=False,
        type=str,
    )
    parser.add_argument(
        "-par",
        "--parallel",
        help="will run functions in parallel if True",
        default=True,
        required=False,
        type=str,
    )

    args = parser.parse_args()

    if fs == True:
        focusstacking(args.input_dir, args.output_dir_fs, args.output_format, args.parallel, args.image_range_fs,
                      args.overwrite)
    if ds == True:
        drifty_shifty(args.output_dir_fs, args.output_dir_ds, args.output_format, args.image_range_ds, args.shift_data,
                      args.pad, args.overwrite, args.parallel)
        main_remove_black_border(args.output_dir_ds, args.output_dir, args.output_format)

#
# if __name__ == '__main__':
#     input_dir = "/Volumes/Caro2/scene2_8bit2"
#     output_dir_fs = "/Volumes/Caro2/scene2_8bit2_FS"
#     output_dir_ds
#     output_dir = "/Volumes/Caro2/scene2_8bit2_FS_dedrifted"
#     output_format = 'png'
#     foo = 'shift_arrays.npz'
#
#     master_main(input_dir, output_dir_fs, output_dir_ds, output_dir, output_format)