# -*- coding: utf-8 -*-
"""
@author: Tatiana Konstantinova
"""
import IntensityWindow as iw
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from collections import defaultdict



def get_profile(image, x,y, incrX = 120, incrY = 40, direction = 'Y'):
    """
    extract profile of the Bragg peak by integrating along one of the coordinates
    """
    corner_x = x - incrX//2
    corner_y = y - incrY//2
    point  = iw.IntensityWindow(corner_y,corner_x,incrY,incrX,image)
    if direction == 'Y':
        return point.integrateY()
    elif direction == 'X':
        return point.integrateX()
    else:
        print('direction of integration is incorrect')
        return []

def initiate_parameters(profile):
    """
    estimates starting points for peak fit
    """
    Bg = profile[0]
    Am = max(profile)
    xc = len(profile)//2    
    return  Am, xc, Bg

def gauss(x, Am, x0, w, Bg, kBg):
    return Am/w*np.exp(-0.5*((x-x0)**2)/(w**2))+ Bg+kBg*x

def fit_profile(profile):
    """ 
    fits profile with Gaussian function,
    returns fit parameters : (Am, x0, w, Bg, kBg)
    plots the result of the fit
    """
    # estimate initial parameters
    Am_0, xc_0, Bg_0 = initiate_parameters(profile)
    w_0 = 3
    kBg_0 = 0
    initial_parameters = np.array([Am_0,xc_0, w_0, Bg_0, kBg_0])
    
    x = list(range(len(profile)))
    
    try:    
        fitted_parameters, pcov = curve_fit(gauss, x, profile, initial_parameters)
    except Exception as e:
        print(e)
        fitted_parameters = initial_parameters
        
    # Plot results of the fitting
    x_fit = np.linspace(min(x), max(x), 100)
    y_plot = gauss(x_fit, *fitted_parameters)
    
    plt.figure(num =2)
    plt.plot(x, profile, 'D') 
    plt.plot(x_fit, y_plot)
    plt.show()
    return fitted_parameters
    
def get_peak_intensity(peaks, total_images):
    """
    Get series of varage peak intensity for the family of equivalent peaks
    peaks -- string, name of the peak family
    total_images -- dictionary of images
    """
    intensities = defaultdict(float)
    xs = []
    ys = []
    # get lists of coordinates
    with open('c'+peaks+'.txt', 'r') as file:
        for coordinates in file:            
            xs.append(int(coordinates.split(' ')[0]))
            ys.append(int(coordinates.split(' ')[1]))
            
    for delay in total_images.keys():        
        
        for j in range(len(xs)):
            profile = get_profile(total_images[delay], xs[j],ys[j])
            fit_parameters = fit_profile(profile)
            intensities[delay] += fit_parameters[0]
    return intensities
            
def sort_normalize(intensities, total_electrons, delays, n_unpumped = 5, peaks = '100'):
    """
    1. Nomalize intensities by total electron counts at each time point
    2. Sort intensities according to the time delay
    3. Nomalize the series by the average value before laser arrival
    """
    assert all([x>0 for x in total_electrons.values()])
    assert len(set(intensities.keys()).difference(set(total_electrons.keys()))) == 0
    

    udj_intensities_delays = [[delays[d], intensities[d]/total_electrons[d]] for d in delays.keys()]
    udj_intensities_delays.sort(key = lambda x: x[0])
    
    udj_intensities = [x[1] for x in udj_intensities_delays]
    delays_sorted = [x[0] for x in udj_intensities_delays]
    before_pump = np.mean(udj_intensities[:n_unpumped])
    norm_intensities = [x/before_pump for x in udj_intensities]
    
    plt.figure(num = 3)
    plt.plot(delays_sorted,norm_intensities)
    np.savetxt(peaks+"intensity.txt", norm_intensities, delimiter=" ")
    
    return norm_intensities
    
    
    
           
            
    
    

    
    
    