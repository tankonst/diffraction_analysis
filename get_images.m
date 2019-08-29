function total_image = get_images(angle, path, image_files_names, steps )

    %getting array of total images
    total_image=cell(steps,1);
    delay=zeros(1,steps);
   
    % creating an empty array of the right size to accomodate rotated
    % images
    file_path=char(strcat(path,image_files_names(1)));
    
    for i=1:steps    
        total_image{i}=zeros(size(imrotate(double(imread(file_path)),angle,'bilinear')));
    end
    
   %%%filling array with rotated images  
   previous_delay = 0;
   
   
for i = 1:length(image_files_names)
    fileName =image_files_names(i);
    %getting image_delay    
    file_name = image_files_names(i);
    split_name = strsplit(file_name, ["-", "_"]);
    image_delay=str2double(split_name(3));
    delay(i)= str2double(split_name(4));    
    
    if image_delay > previous_delay
        file_path=char(strcat(path,fileName));
        total_image{image_delay}=total_image{image_delay}+imrotate(double(imread(file_path)),angle,'bilinear');
    else
        previous_delay = previous_delay + 1;
    end   
end

 % record delay into text files
 dlmwrite('delay.txt',delay,'\t');
 
 %record a rotated image
 dlmwrite('image',total_image{1},'\t');
 
end
