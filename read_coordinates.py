# -*- coding: utf-8 -*-
"""
Reads coordinates of the Bragg peaks from mouse clicks
tiff_file -- image file
angle -- angle of rotation
n -- number of points in the same family
bragg_index -- index of the Bragg peaks
@author: Tatiana Konstantinova
"""

import matplotlib.pyplot as plt
from skimage.transform import rotate

tiff_file = input('Enter your file: ')
bragg_index = input('Enter bragg index: ')
n = int(input('Enter number of peaks: '))
angle = float(input('Enter  angle: '))
 
I = plt.imread(tiff_file)
I = rotate(I, angle)
plt.imshow(I)
points = plt.ginput(n)    
with open('coordinate'+str(bragg_index)+'.txt', 'w') as file:
    for point in points:
        file.write(str(int(point[0]))+' '+str(int(point[1]))+'\n')
