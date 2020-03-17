# -*- coding: utf-8 -*-
"""
Methods for measuring intensities of individual Bragg peaks:
    * fitting peak profile
    * sorting and normalizing the values
    * romoving obvious outliers in time series
"""
import IntensityWindow as iw
from scipy.optimize import curve_fit
import numpy as np
from collections import defaultdict
import visualize as viz
import files_kit as fk

def get_profile(image, x, y, incr_x, incr_y, direction = 'Y'):
    """
    Extracts profile of the Bragg peak by integrating along one of the coordinates.
    x, y -- center of the Bragg peak
    incr_x, incr_y -- dimensions of the window around the Bragg peak
    direction ('X', 'Y') -- direction of integration
    """
    
    corner_x = x - incr_x//2
    corner_y = y - incr_y//2
    point  = iw.IntensityWindow(corner_y, corner_x, incr_y, incr_x, image)
    if direction == 'Y':
        return point.integrateY()
    elif direction == 'X':
        return point.integrateX()
    else:
        print('direction of integration is incorrect')
        return []

def initiate_parameters(profile):
    """
    Estimates starting points for peak fit.
    """
    
    background = profile[0]
    amplitude = max(profile)
    center = len(profile)//2  
    
    return  amplitude, center, background

def gauss(x, amplitude, center, width, background, background_slope):
    
    return (amplitude/width * np.exp(-0.5*((x-center)**2)/(width**2))
            + background + background_slope*x)

def fit_profile(profile):
    """ 
    Fits profile with Gaussian function,
    returns fit parameters : (amplitude, center, width, background, background_slope),
    plots the result of the fit.
    """
    
    # estimate initial parameters
    amplitude_0, center_0, background_0 = initiate_parameters(profile)
    width_0 = 10
    background_slope_0 = 0
    initial_parameters = np.array([amplitude_0, center_0, width_0, background_0, background_slope_0])
    
    x = list(range(len(profile)))
    
    try:    
        fitted_parameters, pcov = curve_fit(gauss, x, profile, initial_parameters)
    except Exception as e:
        print(e)
        fitted_parameters = initial_parameters
        
    # Plot results to check that fitting is adequate   
    viz.plot_fit(profile, gauss, fitted_parameters, 1)

    return fitted_parameters
    
def get_peak_intensity(peaks, total_images, incr_x, incr_y):
    """
    Get series of average peak intensity for the family of equivalent peaks.
    peaks -- string, name of the peak family
    total_images -- dictionary of images
    """
    
    intensities = defaultdict(float)
    
    xs, ys = fk.read_coordinates(peaks)
            
    for delay in total_images.keys():    
         for j in range(len(xs)):
            profile = get_profile(total_images[delay],
                                  xs[j],ys[j],
                                  incr_x, incr_y)
            fit_parameters = fit_profile(profile)
            intensities[delay] += fit_parameters[0]
            
    return intensities
            
def sort_normalize(intensities, total_electrons, delays, n_unpumped, peaks):
    """
    1. Normalize intensities by total electron counts at each time point
    2. Sort intensities according to the time delay
    3. Normalize the series by the average value before laser arrival
    """
   
    assert all([x>0 for x in total_electrons.values()])
    assert len(set(intensities.keys()).difference(set(total_electrons.keys()))) == 0
    
    # sort
    udj_intensities_delays = [[delays[d], intensities[d]/total_electrons[d]] for d in delays.keys()]
    udj_intensities_delays.sort(key = lambda x: x[0])
    
    # normalize
    udj_intensities = [x[1] for x in udj_intensities_delays]
    before_pump = np.mean(udj_intensities[:n_unpumped])
    norm_intensities = [x/before_pump for x in udj_intensities]
    
    return norm_intensities
    
def remove_outliers(series):
    """
    Removes outliers in the series that commonly appear due to cosmic rays.
    """   
    
    alpha = 2*np.std(series)/np.mean(series)
    for j in range(1,len(series)-1):
        if series[j] > (1+alpha)*series[j-1] and series[j] > (1+alpha)*series[j+1]:
            series[j] = 0.5*(series[j-1] + series[j+1])
        elif series[j] < (1-alpha)*series[j-1] and series[j] < (1-alpha)*series[j+1]:
            series[j] = 0.5*(series[j-1] + series[j+1])
    
    return series
    
    
           
            
    
    

    
    
    