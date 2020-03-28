# -*- coding: utf-8 -*-
"""
Methods for measuring intensities of individual Bragg peaks:
    * fitting peak profile
    * sorting and normalizing the values
    * romoving obvious outliers in time series
"""
import modules.IntensityWindow as iw
from scipy.optimize import curve_fit
import numpy as np
from collections import defaultdict
import modules.visualize as viz
import modules.files_kit as fk

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
    amplitude = sorted(profile)[-1]
    center =  np.where(profile == amplitude)[0][0]
    amplitude *= 10
    width = 10
    background_slope = 0
    
    return  amplitude, center, width, background, background_slope

def gauss(x, amplitude, center, width, background, background_slope):
    
    return (amplitude/width * np.exp(-0.5*((x-center)**2)/(width**2))
            + background + background_slope*x)

def fit_profile(profile, initial_parameters, visualize = True):
    """ 
    Fits profile with Gaussian function,
    returns:
        fit parameters (amplitude, center, width, background, background_slope),
        r_squared    
    plots the result of the fit.
    """
    
    x = list(range(len(profile)))
    
    try:    
        fit_parameters, pcov = curve_fit(gauss, x, profile, initial_parameters)
        resid = gauss(np.array(x),*fit_parameters) - np.array(profile)
        ss_res = np.sum(resid**2)
        ss_tot = np.sum((profile-np.mean(profile))**2)
        r_squared = 1 - (ss_res / ss_tot)        
    except Exception as e:
        print(e)
       
    # Plot results to check that fitting is adequate   
    if visualize:
        viz.plot_fit(profile, gauss, fit_parameters, 1)

    return fit_parameters, r_squared
    
def get_peak_intensity(peaks, total_images, incr_x, incr_y):
    """
    Get series of average peak intensity for the family of equivalent peaks.
    peaks -- string, name of the peak family
    total_images -- dictionary of images
    incr_x, incr_y -- size of integration window
    """
    
    intensities = defaultdict(float)
    
    xs, ys = fk.read_coordinates(peaks)    
        
    for j in range(len(xs)):
       first_profile = get_profile(total_images[1], xs[j],ys[j], incr_x, incr_y)
       initial_parameters = np.array(initiate_parameters(first_profile))   
       for delay in total_images.keys():    
            profile = get_profile(total_images[delay],
                                  xs[j],ys[j],
                                  incr_x, incr_y)
            fit_parameters , r_squared = fit_profile(profile, initial_parameters)
            intensities[delay] += fit_parameters[0]
            # if the fit is good, pass the results of the fit as initial parameters for the next time point
            if r_squared > 0.90:
                initial_parameters = fit_parameters
            
    return intensities
            
def sort_normalize(intensities, total_electrons, delays, n_unpumped):
    """
    1. Normalize intensities by total electron counts at each time point
    2. Sort intensities according to the time delay
    3. Normalize the series by the average value before laser arrival
    
    n_unpumped -- number of time points before laser arrival
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
    
def remove_outliers(series, delays):
    """
    Removes outliers in the series that commonly appear due to cosmic rays.
    Series must be sorted to avoid deleting legitimate points.
    """   
    
    alpha = 2*np.std(series)/np.mean(series)
    for j in range(1,len(series)-1):
        if series[j] > (1+alpha)*series[j-1] and series[j] > (1+alpha)*series[j+1]:
            series[j] = 0.5*(series[j-1] + series[j+1])
            print('Outlier at {}'.format(delays[j]))
        elif series[j] < (1-alpha)*series[j-1] and series[j] < (1-alpha)*series[j+1]:
            series[j] = 0.5*(series[j-1] + series[j+1])
            print('Outlier at {}'.format(delays[j]))
    
    return series
    
    
           
            
    
    

    
    
    