clear all
close all
%% Experimental parameters
angle = -52; % angle to rotate the diffraction pattern
n_unpumped = 10; %number of steps at negative delay, i.e before arrival of the laser

% enter all the peaks of interest (coordinates of peoak need to be obtained
% in advance using get_coordinates.m file
peaks_to_analyze = ["200","400"]; 

%% get information about the files

% select the working folder
folder = 'C:\Users\Tatiana\Documents\BNL\SLAC\March 2017\Tatiana\31032017';
[path] = uigetdir(folder);
path = strcat(path, '\');

%get names of image files
image_files_names = get_list_of_files(path);

%% get total intensity for normalization

total_intensity = get_electron_count(path, image_files_names);
steps = length(total_intensity); % delay steps

%% get the array of images for further analysis

total_image = get_images(angle, path, image_files_names, steps);

% get the list of dealays
old_delays=dlmread('delay.txt');
delay = dlmread('delay.txt');

%% Extract peak intensities and write them into respective files

for j =1:length(peaks_to_analyze)
    
    peak = peaks_to_analyze(j);
    disp(peak)
    get_peak_intensity(peak,total_image);    
end




