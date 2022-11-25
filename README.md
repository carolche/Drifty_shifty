This script was created to help process images especially those taken using microscopy over an extended period of time. This script encompasses 3 different processes:
1)  focus stacking,
2)  XY drift correction, and
3)  cropping of aligned images.

In the first process, images taken at different focal points (slices or z-planes) are merged into a single in-focus image. And because objects may move slightly over time while the images are taken, XY drift correction needs to be applied in order to align all of the images. This latter process creates a black border or padding around the images, thus, the last process is to crop the image to remove the black border as well as some parts of the image that are not visible in all of the images.

The main file, FocusStacker_Dedrifter_main_file.py, incorporates all the main functions and includes the driver program which expects the input and output directories, as well as the desired output format.
Alternatively, the GUI can be launched from the terminal: python FocusStacker_Dedrifter_GUI.py.  The GUI will pop up and expects the input and output directories as well as the desired output format. The GUI allows you to run the program three consecutive times by filling out the required inputs on three different tabs; the next program will run once the previous program finishes.
Finally, the helper files, FocusStacker_final_all.py, crop_aligned_img_final.py, and Drifty_Shifty_final.py are required.
