# -*- coding: utf-8 -*-
"""
Methods for extracting data from files.

"""

import glob


def get_list_of_peaks():
    """
    Reads the indexes of Bragg peaks that need to be analyzed from the text
    files with coordinates in the folder
    """
    
    peaks_list = []
    coordinate_files = glob.glob('coordinate*.txt')
    for file in coordinate_files:
        new_peak = file.split('coordinate')[1].split('.')[0]
        peaks_list.append(new_peak)
        
    return peaks_list

def read_coordinates(peaks):
    """
    Read x and y coordinates of Bragg peaks from the text files.
    """
    xs = []
    ys = []
    # get lists of coordinates
    with open('coordinate'+peaks+'.txt', 'r') as file:
        for coordinates in file:            
            xs.append(int(coordinates.split(' ')[0]))
            ys.append(int(coordinates.split(' ')[1]))
            
    return xs, ys

def read_scan_parameters(filename):
    """
    Reads list of values of parameters from a self-explanatory file.
    """
    
    parameters = []
    with open(filename, 'r') as file:
       info = file.read()
    info = info.split('\n')
    for line in info:
        parameters.append(int(line.split(' = ')[1]))
        
    return parameters
    
    
    