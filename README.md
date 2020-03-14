# diffraction_analysis
 A demo of code for diffraction file analysis.
 The demo is only limited to fitting peaks' profiles to Gaussian forms for extracting peaks' intensity.

Files description:

get_coordinates.m identifies coordinates of the peak in a rotated diffraction pattern from mouse clicks. This need to be executed before the first run of analyze_script. Unless the beam moved, the extracted coordinates can be used for multiple experimental sets.

analyze_script.m is the main file to run the analysis. This script calls get_list_of_files.m, get_electron_count.m, get_images.m and get_peak_intensity.m .

IntensityWindow.m is the class for area around a diffraction peak. Methods include the 
