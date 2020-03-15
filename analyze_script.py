# -*- coding: utf-8 -*-
"""
@author: Tatiana Konstantinova
"""
import ScanInfo as scinf
import PeakInfo as pinf
import glob
import pandas as pd

# parameters of the scan
angle = 0 # angle of DF rotation, important for DF with satellites
n_unpumped = 8 # number of frames before arrival of the laser
peaks_to_analyze = ['200']

# get a list of diffraction patterns
path = r'C:\Users\YourPath'
image_files_names = glob.glob(path+r'\images-ANDOR1\*.tif')

# get general information about the scan
total_electron_count, center_int_d, camera_b_d = scinf.get_electrons_counts(image_files_names) 
delays = scinf.get_delays(image_files_names)
scan = pd.DataFrame(index = sorted(delays.values()))

# get rotated images
total_images = scinf.get_images(image_files_names, angle)


# now obtain the information about individual peaks
for peaks in peaks_to_analyze:
    print('Analyzing peaks: {}'.format(peaks))
    row_intensities = pinf.get_peak_intensity(peaks, total_images)
    normalized_intensities = pinf.sort_normalize(row_intensities,
                                                 total_electron_count,
                                                 delays, n_unpumped, peaks)
    scan.loc[:, peaks] = normalized_intensities
    

# record intensities table    
scan.to_csv(path+'\intensities.csv')

print('Done!')