# -*- coding: utf-8 -*-
"""
Methods for visualizing the results of the analysis.
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_fit(profile, func, arguments, n=1):
    """
    Plots the result of fitting data (profile) with function (func).
    n -- figure id
    """
    
    x = list(range(len(profile)))
    
    # Plot results of the fitting to check that fitting is adequate 
    x_fit = np.linspace(min(x), max(x), 100)
    y_plot = func(x_fit, *arguments)
    
    plt.figure(num = n)
    plt.plot(x, profile, 'D') 
    plt.plot(x_fit, y_plot)
    plt.show()
    
def plot_series(delays, values, label, feature, n=1):
    """
    Plots a time series of feature.
    """
    data =  [[d, v] for d,v in zip(delays,values)]
    data.sort(key = lambda x: x[0])
    delays = [x[0] for x in data]
    values = [x[1] for x in data]
    
    plt.figure(num = n)
    plt.plot(delays, values, label = label)
    plt.legend()
    plt.title(feature)