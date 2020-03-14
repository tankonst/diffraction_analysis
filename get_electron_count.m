function [total_intensity] = get_electron_count(path, image_files_names)

    %Calculates total intensity due to incoming electrons to use for
    %normalization of other intensities (adjust for the long-term drift).
    %Central intensity is subtracted to reduce the impact of the motion of
    %the beam arond the detector (this influence is usually
    %insignificant)

center_int=zeros(150,1);
camB=zeros(150,1);
total_intensity= zeros(150,1);

previous_delay=0; %setting initial delay to zero

for i = 1:length(image_files_names)
    
    %getting image_delay    
    file_name = image_files_names(i);
    split_name = strsplit(file_name, '-');
    image_delay=str2double(split_name(2));
    
    if image_delay > previous_delay
        filePath = char(strcat(path,file_name));
        total_image = double(imread(filePath));
        
        %calulating camera background (function of the camera temperature)   
        camera_background = camera(total_image);
             
        %new image with subtracted camera background 
        total_image = total_image-camera_background;
        
        
        center_intensity = center(total_image);
        
        % calculate all important intensities
        total_intensity(image_delay) = total_intensity(image_delay) + sum(sum(total_image));
        center_int(image_delay) = center_int(image_delay) + center_intensity;
        camB(image_delay) = camB(image_delay) + camera_background;
               
    else
        previous_delay = previous_delay + 1;
        
    end
    
         
end

total_intensity = total_intensity(total_intensity~=0);
camB = camB(camB ~=0);
center_int = center_int(center_int~=0);

% plot total intensity
figure(1)
plot(total_intensity)

% write all intensities into text files 
dlmwrite('intensity_total.txt',total_intensity,'\t');
dlmwrite('camera.txt',camB,'\t');
dlmwrite('central_intensity.txt',center_int,'\t');
%dlmwrite('image',imrotate(im2double(total_image),ang,'bilinear'),'\t');
end

function [camera_background] = camera(image)

% calulating camera background (funtion of the camera's temperature)  

 im_dim=size(image);
 v = 100;
 h = 100;
 
 % selecting areas to measure the camera background (use ImageJ to define
 % the proper areas)
 
 top_left = IntensityWindow(1,1,h,v,image);
 bottom_left = IntensityWindow(1,im_dim(1)-v,h,v,image);
 top_right = IntensityWindow(im_dim(2)-h,1,h,v,image);
 bottom_right = IntensityWindow(im_dim(2)-h,im_dim(1)-v,h,v,image);
 
 camera_background = (top_left.integrate2D() + bottom_left.integrate2D() + top_right.integrate2D() + bottom_right.integrate2D())/4/h/v;
 

end

function [center_intensity] = center(image)

% calculating central intensity
% defining the positon of the center beam integration window (use ImageJ)
x_center=504;
y_center=462;
dx_center=97; 
dy_center=97;

center_window = IntensityWindow(x_center, y_center, dx_center, dy_center,image);

center_intensity = center_window.integrate2D();   

end
