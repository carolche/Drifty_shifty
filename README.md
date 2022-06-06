# Drifty_shifty

This script was created to help process images especially those taken using microscopy over an extended period of time. This script encompasses 3 different processes:
1)  focus stacking,
2)  XY drift correction, and
3)  cropping of aligned images.

In the first process, images taken at different focal points (slices or z-planes) are merged into a single in-focus image. And because objects may move slightly over time while the images are taken, XY drift correction needs to be applied in order to align all of the images. This latter process creates a black border or padding around the images, thus, the last process is to crop the image to remove the black border as well as some parts of the image that are not visible in all of the images.
