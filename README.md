# diffraction_analysis
 A demo of code for diffraction file analysis.
 The demo is only limited to fitting peaks' profiles to Gaussian forms for extracting peaks' intensity.

Files description:

read_coordinates.py -- reads coordinates of peaks from a mouse click. Need to be done for each peak before running the analysis (only once per experiment unless sample change/beam shift)

analyze_script.py -- extract intensities for each families of peaks (average among equivalent peaks)

ScanInfo.py -- library to operate with image series and to extract global (not peak-specific) information for each scan: time delay values, total intensity, camera background, etc.

PeakInfo.py -- library to operate with individual peaks

IntensityWindow -- class for integrating intensity 
