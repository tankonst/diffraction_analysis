# -*- coding: utf-8 -*-
"""
Creates simulated series of diffrction patterns
"""

## record a rotated image for reference
#    np.savetxt("image.txt", total_images[1], delimiter=" ")
    
import numpy as np
from PIL import Image





def generate_peak(amplitude, size, sigma):
    x, y = np.meshgrid(np.linspace(-1,1,size), np.linspace(-1,1,size))
    d = np.sqrt(x**2+y**2)
    g = amplitude * np.exp(-( d**2 / ( 2.0 * sigma**2 ) ) )
    return g


np.random.seed(1)
delays = np.random.choice(500, 100, replace=False)
start = np.min(delays)

for t in range(50):
    # noise only
    pattern = 200*np.random.rand(1024,1024)
    x = [380, 700, 380, 700]
    y = [350, 650, 650, 350]
    size = 60
    for j in range(4):
        amplitude = 10000 * np.exp( (start-delays[t]) / 1000) + 10 #* (1 + np.random.random())
        g = generate_peak(amplitude, size, 0.2)
        pattern[y[j] - size//2:y[j] + size//2, x[j] - size//2:x[j] + size//2] += g
   
    size = 900
#    g = generate_peak(200 * (1+np.random.random()), size,0.5)
    g = generate_peak(200 , size,0.5)
    pattern[512 - size//2:512 + size//2, 512 - size//2:512 + size//2] += g 
    pattern8 = (((pattern - pattern.min()) / (pattern.max() - pattern.min())) * 255.9).astype(np.uint8)
    file_name = r'test_images\images-ANDOR1\ANDOR1_delayLow-' + str(t) + '-' + str(delays[t]) + '_20170331.tif'
    im = Image.fromarray(pattern8)
    im.save(file_name)
