# -*- coding: utf-8 -*-
"""
Tests for peak_info.py library
"""
import pytest
import peak_info as pinf
import numpy as np

def test_get_profile():
    
    np.random.seed(1)
    image = np.random.randint(10, size=(50, 50))
    x = 20
    y = 20    
    incr_x = 10
    incr_y = 15   
    corner_x = x - incr_x//2
    corner_y = y - incr_y//2
    image_part = image[corner_y:corner_y+incr_y, corner_x:corner_x+incr_x]
    
    profile_y = np.sum(image_part, 0)
    profile_x = np.sum(image_part, 1)
    
    assert all(profile_y == pinf.get_profile(image, x, y, incr_x, incr_y, direction = 'Y'))
    assert all(profile_x == pinf.get_profile(image, x, y, incr_x, incr_y, direction = 'X'))
    

def test_initiate_parameters():
    
    profile = np.array([5]*10)    
    background = 5
    amplitude = 50
    center =  0
    width = 10
    background_slope = 0
    
    assert  (amplitude, center,
             width, background,
             background_slope) == pinf.initiate_parameters(profile), 'Parameters initiated incorrectly'
    
def gauss(x, amplitude, center, width, background, background_slope):
    
    return (amplitude/width * np.exp(-0.5*((x-center)**2)/(width**2))
            + background + background_slope * x)

def test_fit_profile():
   
    np.random.seed(1)
    noise = np.random.random(100)    
    x = np.arange(100)
    y = gauss(x, 100, 50, 10, 0, 0.02) + noise
    
    fit_parameters, r_squared = pinf.fit_profile(y, [100, 50, 10, 0, 0.02], False)
    
    assert r_squared > 0.95, 'Impoper fit function'
    
def test_sort_normalize():
    
    delays = { 1: 10, 2: 1, 3: 5} 
    total_electrons = { 1: 1, 2: 2, 3: 3} 
    intensities = { 1: 10, 2: 4, 3: 6}
    
    assert [1,1,5] == pinf.sort_normalize(intensities, total_electrons, delays, 1)

def test_remove_outliers():
    
    np.random.seed(1)
    series = np.random.randint(5, size =20)
    initial_series = series
    series[4] = 50
    series[10] = -10
    delays = np.arange(len(series))
    
    assert all(initial_series == pinf.remove_outliers(series, delays))          
