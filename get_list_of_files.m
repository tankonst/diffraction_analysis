function [list_of_files] = get_list_of_files(path)

% gets list of files in the foulder

files_info = dir(strcat(path,'\*.tif'));
list_of_files = strings(length(files_info),1);
for i = 1:length(files_info)
    list_of_files(i)= files_info(i).name;    
end
end