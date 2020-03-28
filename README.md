# diffraction_analysis
A demo of code for analysis of time series of diffraction patterns (DP).
The demo is only limited to fitting peaks' profiles to Gaussian forms for extracting peaks' intensity, sorting according to the position of the delay stage, normalizing and removing outliers (due to cosmic rays).

 ## Files Scheme
![File Scheme](https://github.com/tankonst/diffraction_analysis/blob/master/scheme.JPG?raw=true)

## Files Descriptions
* **read_coordinates.py** – reads coordinates of peaks from a mouse click. Need to be done for each group of peaks before running the analysis (only once per experiment unless sample change/beam shift). The script generates files **coordinate_.txt** 
* **experiment_info.txt** – files with parameters of the analysis (numper of time points before excitation with the laser, rotation angle, sizes of integration windows, etc.)
* **modules/vizualize.py** – vizualization methonds
* **modules/files_kit.py** – methods for extracting data from external .txt files
* **modules/IntensityWindow.py** – class for integrating intensity within a window
* **modules/scan_info.py** – methods to operate with image series and to extract global (not peak-specific) information for each scan: time delay values, total intensity, camera background, etc
* **modules/peak_info.py** – methods to extract intensities of individual peaks, as well as sort and normalize them and remove outliers
* **analyze_script.py** (MAIN SCRIPT) – extract intensities for each peak groups and record them into .csv file. Requires the files path, experiment_info.txt, coordinate*.txt for at least one peak.
* **tests/test_scan_info.py** and **teststest_peak_info.py** – tests for the corresponding libraries (to be used with PyTest)
* **test** folder also contains simulated series of images (intensity drop ~ exp(-0.5))

