# -*- coding: utf-8 -*-
"""
Methods for obtaining general characteristic of the scan (not related to a certain Bragg peak).
"""   
from collections import defaultdict
import matplotlib.pyplot as plt
import modules.IntensityWindow as iw
from skimage.transform import rotate
import numpy as np

    

def camera(image, camera_v, camera_h):
    """
    Calculates camera background (function of temperature) 
    at the corner of the image, where no electrons arrived.
    The size of the area needs to be estimated with ImageJ.
    
    camera_v, camers_h -- vertical and horizontal dimensions of the windows for intensity calculations
    """    
    
    assert camera_v > 0 and camera_h > 0
    
    im_size = len(image)
    top_left = iw.IntensityWindow(0, 0, camera_v, camera_h, image)
    bottom_left = iw.IntensityWindow(im_size-camera_v, 0, camera_v, camera_h, image)
    top_right = iw.IntensityWindow(0,im_size-camera_h, camera_v, camera_h, image)
    bottom_right = iw.IntensityWindow(im_size-camera_v, im_size-camera_h, camera_v, camera_h, image)

    return (top_left.integrate2D() 
            + bottom_left.integrate2D()
            + top_right.integrate2D() 
            + bottom_right.integrate2D())/4/camera_h/camera_v


def center(image, x_center, y_center, dx_center, dy_center):
    """
    Extracts the intensity of the central beam. 
    Use imageJ to determine the integration windows parameters.
    
    x_center, y_center -- coordinates of left top corner
    dx_center, dy_center -- dimensions of the integration window
    """    
    
    assert 0 < x_center < len(image) and 0 < y_center < len(image)
    assert dx_center > 0, dy_center > 0
    
    center_window = iw.IntensityWindow(y_center, x_center, dy_center, dx_center, image)

    return center_window.integrate2D()

def read_image_delay(file_name):
    """
    Returns delay of the single image
    """
    return int(file_name.split('ANDOR1')[2].split('-')[1])

def get_electrons_counts(image_files_names,
                         x_center, y_center, dx_center, dy_center,
                         camera_v, camera_h, shuffled = False, save_text = True):
    """
    Calculates total intensity due to incoming electrons to use for
    normalization of other intensities (adjust for the long-term drift).
    Central intensity is subtracted to reduce the impact of the motion of
    the beam around the detector (this influence is usually
    insignificant).
    Returns text files with the intensity series
    
    image_files_names -- list of pathes to image files
    x_center, y_center, dx_center, dy_center -- parameters of center beam
    camera_v, camera_h -- dimensions of corners for calculating camera background
    """
    
    assert len(image_files_names) > 0
    
    center_int = []
    camera_b = []
    total_int = []
    
    # there can me multiple files with the same delay
    # defaultdict is used to sum the intensities at the same delay
    center_int_d = defaultdict(int)
    camera_b_d = defaultdict(int)
    total_int_d = defaultdict(int)
    
    for i in range(len(image_files_names)):
        file_name = image_files_names[i]
        image_delay = read_image_delay(file_name)
                
        # calculate all important intensities
        image = plt.imread(file_name).astype(float)
        
        # camera  background (function of temperature)
        cam_b = camera(image, camera_v, camera_h)
        camera_b_d[image_delay] += cam_b
        
        # center intensity
        center_i = center(image - cam_b, x_center, y_center, dx_center, dy_center)
        center_int_d[image_delay] += center_i
        
        #total intensity
        total_int_d[image_delay] += sum(sum(image - cam_b)) - center_i
        
    if not shuffled:    
        for delay in sorted(total_int_d):
            total_int.append(total_int_d[delay])
            camera_b.append(camera_b_d[delay])
            center_int.append(center_int_d[delay])
    else:
        for delay in total_int_d:
            total_int.append(total_int_d[delay])
            camera_b.append(camera_b_d[delay])
            center_int.append(center_int_d[delay])
     
    # records intensity series in the files (ordered by time of recording,
    # which may not match the order of actual delay values) 
    if save_text:
        np.savetxt('intensity_total.txt', total_int)
        np.savetxt('camera.txt', camera_b)
        np.savetxt('central_intensity.txt', center_int)
    
    return total_int_d, center_int_d, camera_b_d

def get_images(image_files_names, angle):
    """ 
    Gets series of rotated diffraction patterns.
    """
    
    total_images = {}   
    for file_name in image_files_names:
        image_delay = read_image_delay(file_name)
        image = rotate(plt.imread(file_name), angle)
        if image_delay in total_images:
            total_images[image_delay] += image
        else:
            total_images[image_delay] = image
    
#    # record a rotated image for reference
#    np.savetxt("image.txt", total_images[1], delimiter=" ")
    
    return total_images


    
def get_delays(image_files_names):
    """
    Reads time delays from the file names.
    """
    
    delays= {}    
    for file_name in image_files_names:
        image_delay = read_image_delay(file_name)
        delays[image_delay] = float(file_name.split('ANDOR1')[2].split('-')[2].split('_')[0])
      
    return delays

def delays_to_ps(delays, n_unpumped):
    """
    Converts delay values from mm of motion stage to ps.
    """
    time_zero = sorted(delays)[n_unpumped]
    delays_ps = [(d-time_zero)*6.667 for d in delays]
        
    return delays_ps
   
    