function [x , y] = get_coordinates(folder, n, angle, fname)

    % Reads the coordinates of 'n' points in image(first image in 'folder') from coursor and records them
    % into file 'fname'

%reading the image
cd(folder)
fnames = dir('*.tif');
image_name = fnames(1).name; 
image = imrotate(im2double(imread(image_name)),angle,'bilinear');
imagesc(image);

%getting coordinates
[x,y] = ginput(n);


%recording coordinates into a file
cd('C:\Users\Tatiana\Documents\MATLAB\Codes\tif\FeSe')
dlmwrite(fname, [uint32(x) , uint32(y)], '\t')

end

%% example of the call
%   get_coordinates('./user_folder/images',4,'c200.txt')