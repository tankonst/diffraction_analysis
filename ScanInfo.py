# -*- coding: utf-8 -*-
"""
@author: Tatiana Konstantinova
"""   
from collections import defaultdict
import matplotlib.pyplot as plt
import IntensityWindow as iw
from skimage.transform import rotate
import numpy as np
    

def camera(image, v =100, h =100):
    """
    Calculates camera background (function of temperature) 
    at the corner of the image, where no electrons arrived
    The size of the area needs to be estimated with ImageJ
    
    v, h -- vertical and horizontal dimensions of the windows for intensity calculations
    """    
    assert v > 0 and h > 0
    
    im_size = len(image)
    top_left = iw.IntensityWindow(0,0,v,h,image)
    bottom_left = iw.IntensityWindow(im_size-v,0,v,h,image)
    top_right = iw.IntensityWindow(0,im_size-h,v,h,image)
    bottom_right = iw.IntensityWindow(im_size-v,im_size-h,v,h,image)

    return (top_left.integrate2D() + bottom_left.integrate2D() + top_right.integrate2D() + bottom_right.integrate2D())/4/h/v


def center(image, x_center = 504, y_center = 462, dx_center = 97, dy_center = 97):
    """
    calculating central intensity defining the positon of the
    center beam integration window (use ImageJ)
    
    x_center, y_center -- coordinates of left top corner
    dx_center, dy_center -- dimensions of the intergration window
    """    
    assert 0 < x_center < len(image) and 0 < y_center < len(image)
    assert dx_center > 0, dy_center > 0
    
    center_window = iw.IntensityWindow(y_center,x_center, dy_center, dx_center,image)

    return center_window.integrate2D()

def get_electrons_counts(image_files_names):
    """
    Calculates total intensity due to incoming electrons to use for
    normalization of other intensities (adjust for the long-term drift).
    Central intensity is subtracted to reduce the impact of the motion of
    the beam arond the detector (this influence is usually
    insignificant).
    Returns text files with the intensity series
    
    image_files_names -- list of pathes to image files
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
        image_delay = int(file_name.split('-')[4].split('_')[0])
        print(image_delay)
        
        # calculate all important intensities
        image = plt.imread(file_name).astype(float)
        
        # camera  background (function of temperature)
        cam_b = camera(image)
        camera_b_d[image_delay] += cam_b
        
        # center intensity
        center_i = center(image - cam_b)
        center_int_d[image_delay] += center_i
        
        #total intensity
        total_int_d[image_delay] += sum(sum(image - cam_b)) - center_i
        
    for delay in sorted(total_int_d):
        total_int.append(total_int_d[delay])
        camera_b.append(camera_b_d[delay])
        center_int.append(center_int_d[delay])
     
    # records intensity series in the files    
    with open('intensity_total.txt', 'w') as file:
        for intensity in total_int:
            file.write(str(intensity)+'\n')
    
    with open('camera.txt', 'w') as file:
        for intensity in camera_b:
            file.write(str(intensity)+'\n')
            
    with open('central_intensity.txt', 'w') as file:
        for intensity in center_int:
            file.write(str(intensity)+'\n')
    plt.plot(total_int)
    
    return total_int_d, center_int_d, camera_b_d

def get_images(image_files_names, angle):
    """ 
    gets series of rotated diffraction patterns
    """
    total_images = {}   
    for file_name in image_files_names:
        image_delay = int(file_name.split('-')[4].split('_')[0])
        image = rotate(plt.imread(file_name), angle)
        if image_delay in total_images:
            total_images[image_delay] += image
        else:
            total_images[image_delay] = image
    
    # record a rotated image for reference
    np.savetxt("image.txt", total_images[1], delimiter=" ")
    return total_images


def get_delays(image_files_names):
    """
    reads time delays from the file names
    """
    delays= {}    
    for file_name in image_files_names:
        image_delay = int(file_name.split('-')[4].split('_')[0])
        delays[image_delay] = float(file_name.split('-')[5].split('_')[0])
    return delays

   
    