# -*- coding: utf-8 -*-
"""
@author: Tatiana Konstantinova
"""

import matplotlib.pyplot as plt
from skimage.transform import rotate

def get_coordinates(tiff_file,angle = 0, n = 4, bragg_index = '100'):
    
    """"
    reads coordinates of the Bragg peaks from mouse clicks
    tiff_file -- image file
    angle -- angle of rotation
    n -- number of points in the same family
    bragg_index -- index of the Bragg peaks
    """
 
    I = plt.imread(tiff_file)
    I = rotate(I, angle)
    plt.imshow(I)
    points = plt.ginput(n)
    with open('c'+str(bragg_index)+'.txt', 'w') as file:
        for point in points:
            file.write(str(int(point[0]))+' '+str(int(point[1]))+'\n')
    
#
            
tiff_file = r'C:\Users\YourPath'
get_coordinates(tiff_file, bragg_index = '200')