# -*- coding: utf-8 -*-
"""
Tests for scan_info.py library
"""

import pytest
import scan_info as sinf
import numpy as np

def test_camera():
    
    np.random.seed(1)
    image = np.random.randint(10, size = (50,50))    
    h = 5
    v = 6
    test_cam = ( np.sum(image[:v,:h])
                + np.sum(image[50-v:50,:h])
                + np.sum(image[50-v:50,50-h:50])
                + np.sum(image[:v,50-h:50]))/4/h/v
                
    assert test_cam == sinf.camera(image, v, h), 'camera background is incorrect'
    
def test_center():
    np.random.seed(1)
    image = np.random.randint(10, size = (50,50))
    y_center, x_center, dy_center, dx_center = 20, 25, 10, 15    
    center_window = np.sum(image[y_center:y_center+dy_center, x_center:x_center+dx_center])
    
    assert center_window == sinf.center(image, x_center, y_center,
                                        dx_center, dy_center), 'center intensity is incorrect'