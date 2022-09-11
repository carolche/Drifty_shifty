import PySimpleGUI as sg
from FocusStacker_final_all import FocusStacker
from Drifty_Shifty_final_GUI import Drifty_Shifty
from crop_aligned_img_final import crop_aligned_images
import ast


def error_win():
    layout = [[sg.Text('Please make sure you entered all the relevant inputs!!', size=(45, 1),
                       justification='center', font=("Helvetica", 15))], [sg.Button('OK')]]
    window = sg.Window('ERROR! ', layout, element_justification='center')
    while True:
        event, values = window.read()
        if event == 'OK' or event == sg.WINDOW_CLOSED:
            break
    window.close()


def error_win2():
    layout = [[sg.Text('If you do not want to run Crop, please input False for Crop!', size=(45, 1),
                       justification='center', font=("Helvetica", 15))], [sg.Button('OK')]]
    window = sg.Window('ERROR! ', layout, element_justification='center')
    while True:
        event, values = window.read()
        if event == 'OK' or event == sg.WINDOW_CLOSED:
            break
    window.close()


def end_win():
    layout = [[sg.Text('Program successfully completed. Press OK to end.', size=(55, 2), justification='center',
                       font=("Helvetica", 15))], [sg.Button('OK')]]
    window = sg.Window('End Program', layout, size=(500, 100), element_justification='center')
    while True:
        event, values = window.read()
        if event == 'OK' or event == sg.WINDOW_CLOSED:
            break
    window.close()


def main_functions(text, fs, ds, crop, inp, out_fs, out_ds, out, form, par, im_r_fs, over, im_r_ds, shift, pad):

    layout5 = [[sg.Text(text, size=(35, 1), justification='center', font=("Helvetica", 25)),
                sg.ProgressBar(max_value=10, key='progress')]]

    window5 = sg.Window('Progress Meter', layout5, size=(500, 100), finalize=True, element_justification='center')
    window5['progress'].update()

    input_value = [values[inp] == '', values[out_fs] == '', values[out_ds] == '', values[out] == '', values[form] == '']

    if values[fs] == 'True' and values[ds] == 'True' and values[crop] == 'True':
        if values[inp] == '' and values[out_fs] == '' and values[out_ds] == '' and values[out] == '' and values[form] == '':
            window5.close()
            # end_win()
        elif any(input_value) == True:
            window5.close()
            error_win()
        else:
            FocusStacker(values[inp], values[out_fs], values[form], parallel=eval(values[par]),
                         image_range_fs=eval(values[im_r_fs]), overwrite=eval(values[over]))
            Drifty_Shifty(values[out_fs], values[out_ds], values[form],
                          image_range_ds=eval(values[im_r_ds]), shift_data=values[shift],
                          pad=eval(values[pad]), overwrite=eval(values[over]),
                          parallel=eval(values[par]))
            crop_aligned_images(values[out_ds], values[out], values[form])
            window5.close()
    elif values[fs] == 'False' and values[ds] == 'True' and values[crop] == 'True':
        if values[out_fs] == '' or values[out_ds] == '' or values[out] == '' or values[form] == '':
            window5.close()
            error_win()
        else:
            Drifty_Shifty(values[out_fs], values[out_ds], values[form],
                          image_range_ds=eval(values[im_r_ds]), shift_data=values[shift],
                          pad=eval(values[pad]), overwrite=eval(values[over]),
                          parallel=eval(values[par]))
            crop_aligned_images(values[out_ds], values[out], values[form])
            window5.close()
    elif values[fs] == 'False' and values[ds] == 'True' and values[crop] == 'False':
        if values[out_fs] == '' or values[out_ds] == '' or values[form] == '':
            window5.close()
            error_win()
        else:
            Drifty_Shifty(values[out_fs], values[out_ds], values[form],
                          image_range_ds=eval(values[im_r_ds]), shift_data=values[shift],
                          pad=eval(values[pad]), overwrite=eval(values[over]),
                          parallel=eval(values[par]))
            window5.close()
    elif values[fs] == 'True' and values[ds] == 'True' and values[crop] == 'False':
        if values[inp] == '' or values[out_fs] == '' or values[out_ds] == '' or values[form] == '':
            window5.close()
            error_win()
        else:
            FocusStacker(values[inp], values[out_fs], values[form], parallel=eval(values[par]),
                         image_range_fs=eval(values[im_r_fs]), overwrite=eval(values[over]))
            Drifty_Shifty(values[out_fs], values[out_ds], values[form],
                          image_range_ds=eval(values[im_r_ds]), shift_data=values[shift],
                          pad=eval(values[pad]), overwrite=eval(values[over]),
                          parallel=eval(values[par]))
            window5.close()
    elif values[fs] == 'True' and values[ds] == 'False' and values[crop] == 'True':
        if values[inp] == '' or values[out_fs] == '' or values[form] == '':
            window5.close()
            error_win()
        elif values[out_ds] == '' or values[out] == '':
            window5.close()
            error_win2()
        else:
            FocusStacker(values[inp], values[out_fs], values[form], parallel=eval(values[par]),
                         image_range_fs=eval(values[im_r_fs]), overwrite=eval(values[over]))
            window5.close()
    elif values[fs] == 'True' and values[ds] == 'False' and values[crop] == 'False':
        if values[inp] == '' or values[out_fs] == '' or values[form] == '':
            window5.close()
            error_win()
        else:
            FocusStacker(values[inp], values[out_fs], values[form], parallel=eval(values[par]),
                         image_range_fs=eval(values[im_r_fs]), overwrite=eval(values[over]))
            window5.close()
    elif values[fs] == 'False' and values[ds] == 'False' and values[crop] == 'True':
        if values[out_ds] == '' or values[out] == '' or values[form] == '':
            window5.close()
            error_win()
        else:
            crop_aligned_images(values[out_ds], values[out], values[form])
            window5.close()



sg.theme('Light Blue 2')

layout1 = [[sg.Text('Welcome to FocusStacker_Dedrifter', size=(70, 1), justification='center', font=("Helvetica", 25),
                    relief=sg.RELIEF_RIDGE)],
          [sg.Text(' ' * 100, size=(5, 1), font=("Helvetica", 1))],
          [sg.Multiline(default_text='This script is used as a pipeline to run FocusStacker, Drifty_Shifty, and crop_aligned_images sequentially in'
                                     'order to merge slices of an image taken at different focal points into one focused image, to dedrift and align the'
                                     'images, and then to crop and retain only the parts of the images that are visible in every single frame. However,'
                                     'there is an option of running just the specified process. All of the edited images will be saved in the given output format'
                                     '(output_format ie. png or tif/f)'
                                     '\n'
                                     '\nThis program has 8 required inputs as follows. You must enter True or False in the first 3 inputs to determine which program to run. Directories can be empty if not running the process:'
                                     '\n1. FocusStacker: True or False --> False if running FocusStacker is not desired. In this case, leave <Input directory for FocusStacker> empty.'
                                     '\n2. Drifty_Shifty: True or False --> False if running Drifty_Shifty is not desired; leave <Output directory for FocusStacker/Input directory '
                                     'for Drifty_Shifty> and <Output directory for Cropping> empty.'
                                     '\n3. Crop: True or False --> False if cropping the images after dedrifting is not desired. In this case, leave <Output directory for Cropping> empty.'
                                     '\n4. Input directory for FocusStacker'
                                     '\n5. Output directory for FocusStacker/Input directory for Drifty_Shifty'
                                     '\n6. Output directory for Drifty_Shifty/Input directory for Cropping'
                                     '\n7. Output directory for Cropping'
                                     '\n8. Output format (png or tif/f)'
                                     '\n'
                                     '\nThis program also takes 6 optional parameters which are all True by default:'
                                     '\n1. Image range for FocusStacker: True or tuple --> True to run all images. Enter a tuple to designate the start and end of the image range desired.'
                                     '\n2. Image range for Drifty_Shifty: True or tuple --> True to run all images. Enter a tuple to designate the start and end of the image range desired.'
                                     '\n3. Shift data: True or filename --> True if you wish to create a new shift array. Or else enter filename of a previously created shift array that ends with <.npz>.'
                                     '\n4. Pad data: True or False --> False if padding and dedrifting the images are not desired.'
                                     '\n5. Overwrite: True or False --> False if overwriting the saved images is not desired.'
                                     '\n6. Parallel: True or False --> False if running the script in parallel is not desired.'
                                     '\n'
                                     '\nBy default, "shift_data" is set as True which means that the function calc_shift will be called and a '
                                    'shift array will be calculated. However, if there is already a calculated shift array (saved as '
                                    'shift_arrays.npz file), then please move this file into the output directory for FocusStacker and input the filename as the '
                                    'Shift Data argument.'
                                    '\nIf you want to just calculate the shift array and not dedrift the images, then set Pad=False.'
                                    '\nBy default, the variable input "overwrite" is set to True, but can be changed to False. This will save subsequent '
                                    'files with the same base name with the addition of sequential numbers at the end.'
                                    '\nUser can also define whether to run the functions in parallel (via joblib) or not, denoted here as '
                                    'parallel, which by default is True but can be set to False.'
                                    '\nFinally, by default, the dedrifted/aligned images will be cropped to remove the black padding created by the '
                                    'dedrifting process and to retain only the parts of the images that are visible in every single frame (via the '
                                    'crop_aligned_images function). But if crop is set to False, this function will not be called.'
                                    '\nYou may run the program up to three times, which will run sequentially, using different images and different '
                                    'parameters. Just input the information into the different tabs and press Run. The tab "Run #1" will run first, '
                                    'followed by "Run #2" and "Run #3". If you leave any of the tabs empty, they will not be run.',
                        no_scrollbar=True, size=(210, 32), justification='left', font=("Helvetica", 10), border_width=1)],
          [sg.Text(' ' * 100, size=(5, 1), font=("Helvetica", 1))],
          [sg.Text('Please enter the required inputs:', size=(86, 1), justification='left', font=("Helvetica", 17),
                   relief=sg.RELIEF_RIDGE)],
           [sg.Text('If you do not want to run FocusStacker, enter False for FocusStacker',
                    size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
           [sg.Text('FocusStacker: True or False', size=(50, 1), font=("Helvetica", 12)),
            sg.Input('True', key='fs', size=(70, 1), font=("Helvetica", 12))],
            [sg.Text('If you do not want to run Drifty_Shifty, enter False for Drifty_Shifty', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Drifty_Shifty: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key='ds', size=(70, 1), font=("Helvetica", 12))],
            [sg.Text('If you do not want to crop your images and remove the black border, enter False for Crop',
                     size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
            [sg.Text('Crop: True or False', size=(50, 1), font=("Helvetica", 12)),
             sg.Input('True', key='crop', size=(70, 1), font=("Helvetica", 12))],
            [sg.Text('Input/Output Directories. Can be empty if not running process.',
                    size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
            [sg.Text('Input directory for FocusStacker', size=(50, 1), font=("Helvetica", 12)),
             sg.Input(key='inp', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output directory for FocusStacker/Input directory for Drifty_Shifty', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key='out_fs', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output directory for Drifty_Shifty/Input directory for Cropping', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key='out_ds', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output directory for Cropping', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key='out', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output format (png or tif/f)', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key='form', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('*'  * 230, size=(210, 1))],
          [sg.Text('These are the optional parameters:', size=(86, 1), justification='left', font=("Helvetica", 17),
                   relief=sg.RELIEF_RIDGE)],
          [sg.Text('If you do not want to process all your images, enter the range of images as a tuple for Image Range',
                   size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Image range for FocusStacker: True or tuple', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key='im_r_fs', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to process all your images, enter the range of images as a tuple for Image Range',
                   size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Image range for Drifty_Shifty: True or tuple', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key='im_r_ds', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to create new shift data and already have a shift array in an .npz file, enter '
                   'the filename', size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Shift data: True or filename', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key='shift', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to run Pad to dedrift the images, enter False for Pad', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Pad data: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key='pad', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to overwrite your saved files, enter False for Overwrite', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Overwrite: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key='over', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to run the script in parallel, enter False for Parallel', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Parallel: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key='par', size=(70, 1), font=("Helvetica", 12))],
          [sg.Submit('Run', size=(5, 1), font=("Helvetica", 15)), sg.Cancel('Quit'), sg.Button('Reset')]]

layout2 = [[sg.Text('Welcome to FocusStacker_Dedrifter', size=(70, 1), justification='center', font=("Helvetica", 25),
                    relief=sg.RELIEF_RIDGE)],
          [sg.Text(' ' * 100, size=(5, 1), font=("Helvetica", 1))],
          [sg.Multiline(default_text='This script is used as a pipeline to run FocusStacker, Drifty_Shifty, and crop_aligned_images sequentially in'
                                     'order to merge slices of an image taken at different focal points into one focused image, to dedrift and align the'
                                     'images, and then to crop and retain only the parts of the images that are visible in every single frame. However,'
                                     'there is an option of running just the specified process. All of the edited images will be saved in the given output format'
                                     '(output_format ie. png or tif/f)'
                                     '\n'
                                     '\nThis program has 8 required inputs as follows. You must enter True or False in the first 3 inputs to determine which program to run. Directories can be empty if not running the process:'
                                     '\n1. FocusStacker: True or False --> False if running FocusStacker is not desired. In this case, leave <Input directory for FocusStacker> empty.'
                                     '\n2. Drifty_Shifty: True or False --> False if running Drifty_Shifty is not desired; leave <Output directory for FocusStacker/Input directory '
                                     'for Drifty_Shifty> and <Output directory for Cropping> empty.'
                                     '\n3. Crop: True or False --> False if cropping the images after dedrifting is not desired. In this case, leave <Output directory for Cropping> empty.'
                                     '\n4. Input directory for FocusStacker'
                                     '\n5. Output directory for FocusStacker/Input directory for Drifty_Shifty'
                                     '\n6. Output directory for Drifty_Shifty/Input directory for Cropping'
                                     '\n7. Output directory for Cropping'
                                     '\n8. Output format (png or tif/f)'
                                     '\n'
                                     '\nThis program also takes 6 optional parameters which are all True by default:'
                                     '\n1. Image range for FocusStacker: True or tuple --> True to run all images. Enter a tuple to designate the start and end of the image range desired.'
                                     '\n2. Image range for Drifty_Shifty: True or tuple --> True to run all images. Enter a tuple to designate the start and end of the image range desired.'
                                     '\n3. Shift data: True or filename --> True if you wish to create a new shift array. Or else enter filename of a previously created shift array that ends with <.npz>.'
                                     '\n4. Pad data: True or False --> False if padding and dedrifting the images are not desired.'
                                     '\n5. Overwrite: True or False --> False if overwriting the saved images is not desired.'
                                     '\n6. Parallel: True or False --> False if running the script in parallel is not desired.'
                                     '\n'
                                     '\nBy default, "shift_data" is set as True which means that the function calc_shift will be called and a '
                                    'shift array will be calculated. However, if there is already a calculated shift array (saved as '
                                    'shift_arrays.npz file), then please move this file into the output directory for FocusStacker and input the filename as the '
                                    'Shift Data argument.'
                                    '\nIf you want to just calculate the shift array and not dedrift the images, then set Pad=False.'
                                    '\nBy default, the variable input "overwrite" is set to True, but can be changed to False. This will save subsequent '
                                    'files with the same base name with the addition of sequential numbers at the end.'
                                    '\nUser can also define whether to run the functions in parallel (via joblib) or not, denoted here as '
                                    'parallel, which by default is True but can be set to False.'
                                    '\nFinally, by default, the dedrifted/aligned images will be cropped to remove the black padding created by the '
                                    'dedrifting process and to retain only the parts of the images that are visible in every single frame (via the '
                                    'crop_aligned_images function). But if crop is set to False, this function will not be called.'
                                    '\nYou may run the program up to three times, which will run sequentially, using different images and different '
                                    'parameters. Just input the information into the different tabs and press Run. The tab "Run #1" will run first, '
                                    'followed by "Run #2" and "Run #3". If you leave any of the tabs empty, they will not be run.',
                        no_scrollbar=True, size=(210, 32), justification='left', font=("Helvetica", 10), border_width=1)],
          [sg.Text(' ' * 100, size=(5, 1), font=("Helvetica", 1))],
          [sg.Text('Please enter the required inputs:', size=(86, 1), justification='left', font=("Helvetica", 17),
                   relief=sg.RELIEF_RIDGE)],
           [sg.Text('If you do not want to run FocusStacker, enter False for FocusStacker',
                    size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
           [sg.Text('FocusStacker: True or False', size=(50, 1), font=("Helvetica", 12)),
            sg.Input('True', key=' fs', size=(70, 1), font=("Helvetica", 12))],
            [sg.Text('If you do not want to run Drifty_Shifty, enter False for Drifty_Shifty', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Drifty_Shifty: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' ds', size=(70, 1), font=("Helvetica", 12))],
            [sg.Text('If you do not want to crop your images and remove the black border, enter False for Crop',
                     size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
            [sg.Text('Crop: True or False', size=(50, 1), font=("Helvetica", 12)),
             sg.Input('True', key=' crop', size=(70, 1), font=("Helvetica", 12))],
           [sg.Text('Input/Output Directories. Can be empty if not running process.',
                    size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
            [sg.Text('Input directory for FocusStacker', size=(50, 1), font=("Helvetica", 12)),
             sg.Input(key=' inp', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output directory for FocusStacker/Input directory for Drifty_Shifty', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key=' out_fs', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output directory for Drifty_Shifty/Input directory for Cropping', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key=' out_ds', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output directory for Cropping', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key=' out', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output format (png or tif/f)', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key=' form', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('*'  * 230, size=(210, 1))],
          [sg.Text('These are the optional parameters:', size=(86, 1), justification='left', font=("Helvetica", 17),
                   relief=sg.RELIEF_RIDGE)],
          [sg.Text('If you do not want to process all your images, enter the range of images as a tuple for Image Range',
                   size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Image range for FocusStacker: True or tuple', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' im_r_fs', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to process all your images, enter the range of images as a tuple for Image Range',
                   size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Image range for Drifty_Shifty: True or tuple', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' im_r_ds', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to create new shift data and already have a shift array in an .npz file, enter '
                   'the filename', size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Shift data: True or filename', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' shift', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to run Pad to dedrift the images, enter False for Pad', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Pad data: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' pad', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to overwrite your saved files, enter False for Overwrite', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Overwrite: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' over', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to run the script in parallel, enter False for Parallel', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Parallel: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' par', size=(70, 1), font=("Helvetica", 12))]]

layout3 = [[sg.Text('Welcome to FocusStacker_Dedrifter', size=(70, 1), justification='center', font=("Helvetica", 25),
                    relief=sg.RELIEF_RIDGE)],
          [sg.Text(' ' * 100, size=(5, 1), font=("Helvetica", 1))],
          [sg.Multiline(default_text='This script is used as a pipeline to run FocusStacker, Drifty_Shifty, and crop_aligned_images sequentially in'
                                     'order to merge slices of an image taken at different focal points into one focused image, to dedrift and align the'
                                     'images, and then to crop and retain only the parts of the images that are visible in every single frame. However,'
                                     'there is an option of running just the specified process. All of the edited images will be saved in the given output format'
                                     '(output_format ie. png or tif/f)'
                                     '\n'
                                     '\nThis program has 8 required inputs as follows. You must enter True or False in the first 3 inputs to determine which program to run. Directories can be empty if not running the process:'
                                     '\n1. FocusStacker: True or False --> False if running FocusStacker is not desired. In this case, leave <Input directory for FocusStacker> empty.'
                                     '\n2. Drifty_Shifty: True or False --> False if running Drifty_Shifty is not desired; leave <Output directory for FocusStacker/Input directory '
                                     'for Drifty_Shifty> and <Output directory for Cropping> empty.'
                                     '\n3. Crop: True or False --> False if cropping the images after dedrifting is not desired. In this case, leave <Output directory for Cropping> empty.'
                                     '\n4. Input directory for FocusStacker'
                                     '\n5. Output directory for FocusStacker/Input directory for Drifty_Shifty'
                                     '\n6. Output directory for Drifty_Shifty/Input directory for Cropping'
                                     '\n7. Output directory for Cropping'
                                     '\n8. Output format (png or tif/f)'
                                     '\n'
                                     '\nThis program also takes 6 optional parameters which are all True by default:'
                                     '\n1. Image range for FocusStacker: True or tuple --> True to run all images. Enter a tuple to designate the start and end of the image range desired.'
                                     '\n2. Image range for Drifty_Shifty: True or tuple --> True to run all images. Enter a tuple to designate the start and end of the image range desired.'
                                     '\n3. Shift data: True or filename --> True if you wish to create a new shift array. Or else enter filename of a previously created shift array that ends with <.npz>.'
                                     '\n4. Pad data: True or False --> False if padding and dedrifting the images are not desired.'
                                     '\n5. Overwrite: True or False --> False if overwriting the saved images is not desired.'
                                     '\n6. Parallel: True or False --> False if running the script in parallel is not desired.'
                                     '\n'
                                     '\nBy default, "shift_data" is set as True which means that the function calc_shift will be called and a '
                                    'shift array will be calculated. However, if there is already a calculated shift array (saved as '
                                    'shift_arrays.npz file), then please move this file into the output directory for FocusStacker and input the filename as the '
                                    'Shift Data argument.'
                                    '\nIf you want to just calculate the shift array and not dedrift the images, then set Pad=False.'
                                    '\nBy default, the variable input "overwrite" is set to True, but can be changed to False. This will save subsequent '
                                    'files with the same base name with the addition of sequential numbers at the end.'
                                    '\nUser can also define whether to run the functions in parallel (via joblib) or not, denoted here as '
                                    'parallel, which by default is True but can be set to False.'
                                    '\nFinally, by default, the dedrifted/aligned images will be cropped to remove the black padding created by the '
                                    'dedrifting process and to retain only the parts of the images that are visible in every single frame (via the '
                                    'crop_aligned_images function). But if crop is set to False, this function will not be called.'
                                    '\nYou may run the program up to three times, which will run sequentially, using different images and different '
                                    'parameters. Just input the information into the different tabs and press Run. The tab "Run #1" will run first, '
                                    'followed by "Run #2" and "Run #3". If you leave any of the tabs empty, they will not be run.',
                        no_scrollbar=True, size=(210, 32), justification='left', font=("Helvetica", 10), border_width=1)],
          [sg.Text(' ' * 100, size=(5, 1), font=("Helvetica", 1))],
          [sg.Text('Please enter the required inputs:', size=(86, 1), justification='left', font=("Helvetica", 17),
                   relief=sg.RELIEF_RIDGE)],
           [sg.Text('If you do not want to run FocusStacker, enter False for FocusStacker',
                    size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
           [sg.Text('FocusStacker: True or False', size=(50, 1), font=("Helvetica", 12)),
            sg.Input('True', key=' fs ', size=(70, 1), font=("Helvetica", 12))],
            [sg.Text('If you do not want to run Drifty_Shifty, enter False for Drifty_Shifty', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Drifty_Shifty: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' ds ', size=(70, 1), font=("Helvetica", 12))],
            [sg.Text('If you do not want to crop your images and remove the black border, enter False for Crop',
                     size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
            [sg.Text('Crop: True or False', size=(50, 1), font=("Helvetica", 12)),
             sg.Input('True', key=' crop ', size=(70, 1), font=("Helvetica", 12))],
           [sg.Text('Input/Output Directories. Can be empty if not running process.',
                    size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
            [sg.Text('Input directory for FocusStacker', size=(50, 1), font=("Helvetica", 12)),
             sg.Input(key=' inp ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output directory for FocusStacker/Input directory for Drifty_Shifty', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key=' out_fs ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output directory for Drifty_Shifty/Input directory for Cropping', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key=' out_ds ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output directory for Cropping', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key=' out ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('Output format (png or tif/f)', size=(50, 1), font=("Helvetica", 12)),
           sg.Input(key=' form ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('*'  * 230, size=(210, 1))],
          [sg.Text('These are the optional parameters:', size=(86, 1), justification='left', font=("Helvetica", 17),
                   relief=sg.RELIEF_RIDGE)],
          [sg.Text('If you do not want to process all your images, enter the range of images as a tuple for Image Range',
                   size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Image range for FocusStacker: True or tuple', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' im_r_fs ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to process all your images, enter the range of images as a tuple for Image Range',
                   size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Image range for Drifty_Shifty: True or tuple', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' im_r_ds ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to create new shift data and already have a shift array in an .npz file, enter '
                   'the filename', size=(122, 1), justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Shift data: True or filename', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' shift ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to run Pad to dedrift the images, enter False for Pad', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Pad data: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' pad ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to overwrite your saved files, enter False for Overwrite', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Overwrite: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' over ', size=(70, 1), font=("Helvetica", 12))],
          [sg.Text('If you do not want to run the script in parallel, enter False for Parallel', size=(122, 1),
                   justification='left', font=("Helvetica", 12), relief=sg.RELIEF_GROOVE)],
          [sg.Text('Parallel: True or False', size=(50, 1), font=("Helvetica", 12)),
           sg.Input('True', key=' par ', size=(70, 1), font=("Helvetica", 12))]]


tabgrp = [[sg.TabGroup([[sg.Tab('Run #1', layout1), sg.Tab('Run #2', layout2), sg.Tab('Run #3', layout3)]],
                       tab_location='centertop', title_color='Red', tab_background_color='Purple',
                       selected_title_color='Black', selected_background_color='Gray'), sg.Button('Close')]]

window = sg.Window('FocusStacker_Dedrifter', tabgrp, size=(1000, 1150))

while True:
    event, values = window.read()
    if event == 'Quit' or event == sg.WINDOW_CLOSED:
        break
    elif event == 'Reset':
        window['inp']('')
        window['out_fs']('')
        window['out_ds']('')
        window['out']('')
        window['form']('')
        window['fs']('True')
        window['im_r_fs']('True')
        window['ds']('True')
        window['im_r_ds']('True')
        window['shift']('True')
        window['pad']('True')
        window['over']('True')
        window['par']('True')
        window['crop']('True')
    elif event == 'Run':
        main_functions('Program #1 is running.....', 'fs', 'ds', 'crop', 'inp', 'out_fs', 'out_ds', 'out', 'form',
                       'par', 'im_r_fs', 'over', 'im_r_ds', 'shift', 'pad')
        main_functions('Program #2 is running.....', ' fs', ' ds', ' crop', ' inp', ' out_fs', ' out_ds', ' out',
                       ' form', ' par', ' im_r_fs', ' over', ' im_r_ds', ' shift', ' pad')
        main_functions('Program #3 is running.....', ' fs ', ' ds ', ' crop ', ' inp ', ' out_fs ', ' out_ds ', ' out ',
                       ' form ', ' par ', ' im_r_fs ', ' over ', ' im_r_ds ', ' shift ', ' pad ')
        end_win()
        break

window.close()