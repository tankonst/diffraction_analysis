# -*- coding: utf-8 -*-
"""
Main script for extracting intensities of a single or multiple Bragg peaks.
Before running the script make sure that
coordinates of the points are in 'coordinates***.txt' files
and the correct scan parameters are listed in the file 'scan_info.txt'
To run the script, the address of the folder with DF is needed.
The script returns the table with normalized intensity time series.
"""
import scan_info as scinf
import peak_info as pinf
import visualize as viz
import files_kit as fk
import glob
import pandas as pd


# get parameters of the scan
try:
    [angle, 
    n_unpumped,
    incr_x,
    incr_y,
    x_center,
    y_center,
    dx_center,
    dy_center,
    camera_v,
    camera_h] = fk.read_scan_parameters('experiment_info.txt')


    peaks_to_analyze = fk.get_list_of_peaks()
    
    # get a list of DF files
    path = input('Enter the file location: ')
    image_files_names = glob.glob(path+r'\images-ANDOR1\*.tif')
    
    # get general information about the scan
    total_electron_count, center_int_d, camera_b_d = scinf.get_electrons_counts(image_files_names,
                                                                                x_center, y_center, dx_center, dy_center,
                                                                                camera_v, camera_h) 
    delays = scinf.get_delays(image_files_names)
    delays_sorted = sorted(delays.values())
    scan = pd.DataFrame(index = delays_sorted)
    
    # get rotated images
    total_images = scinf.get_images(image_files_names, angle)
    
    # obtain the information about individual peaks
    for peaks in peaks_to_analyze:
        print('Analyzing peaks: {}'.format(peaks))
        row_intensities = pinf.get_peak_intensity(peaks, total_images, incr_x,incr_y)
        normalized_intensities = pinf.sort_normalize(row_intensities,
                                                     total_electron_count,
                                                     delays, n_unpumped, peaks)
        normalized_intensities = pinf.remove_outliers(normalized_intensities)
        
        # record into resulting table
        scan.loc[:, peaks] = normalized_intensities
        
        # plot the intensity series
        viz.plot_series(delays_sorted, normalized_intensities, peaks, 'peak intensity', 2)
     
    # record intensities table    
    scan.to_csv(path+'\intensities.csv')
    
    # plot the total intensity
    viz.plot_series(list(total_electron_count.keys()),
                    list(total_electron_count.values()),
                    'e-counts', 'total intensity', 3)
except Exception as e:
    print(e)

print('Done!')