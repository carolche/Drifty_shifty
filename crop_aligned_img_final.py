# Title: crop_aligned_images
# AUTHOR: Caroline Berthebaud Cheung
# DATE: 2022/06/03 (YY/MM/DD)
#
# [] = main_crop(input_dir, output_dir, output_format)
#
#      This script is used to crop dedrifted, thus aligned, images of an object taken over a certain period of time.
#      Because over time, the object will move slightly (or sometimes a lot) from its original place, we first dedrifted
#      the images and aligned them by padding the moved distance with a black border. In order to keep only the parts of
#      the object that is exactly the same in each image, I created this script to crop out the black border as well as
#      the parts of the object that are not in every frame.
#
#      This script takes 3 required input: "input_dir" which is the directory where all the images are contained;
#      "output_dir" which is the directory where the cropped images will be saved; and the "output_format" which should
#      either be png or tif(f).
#
# -------------------------------------------------------------------------------------------------------------------


import numpy as np
import cv2
import os
from timeit import default_timer as timer


def remove_black_border(images):
    y_nonzero, x_nonzero = list(zip(*[np.nonzero(i) for i in images]))

    min_y = np.max([np.min(y) for y in y_nonzero])
    max_y = np.min([np.max(y) for y in y_nonzero])
    min_x = np.max([np.min(x) for x in x_nonzero])
    max_x = np.min([np.max(x) for x in x_nonzero])

    return min_y, min_x, max_y, max_x



def crop_aligned_images(input_dir, output_dir, output_format):
    start = timer()
    print('start cropping')

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
    images = [cv2.imread(f) for f in fileNames]
    images = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) for i in images if i.shape[2]==3]
    names = [f.rsplit('.')[0] for f in fileNames]

    min_y, min_x, max_y, max_x = remove_black_border(images)

    for i in range(len(images)):
        image = images[i][min_y:max_y, min_x:max_x]
        cv2.imwrite(os.path.join(output_dir, f"{names[i]}_crop.{output_format}"), image)

    end = timer()
    print(f'elapsed time {end-start}')
    print('cropping successful')

    return None





if __name__ == '__main__':
    input_dir = "/Volumes/Caro2/scene2_8bit2_FS_dedrifted"
    output_dir = "/Volumes/Caro2/scene2_8bit2_FS_dedrifted_cropped"
    output_format = 'png'

    crop_aligned_images(input_dir, output_dir, output_format)