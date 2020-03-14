
function [] = get_peak_intensity(peaks,total_image)
    % get coordinates of the peaks, fit intensity profile to Gaussian form and
    % record intensity series into file.
    % Need to have files with peak positions

    % peaks (string) - index of the peak group, e.g. '110'
    % total_image (cell of matrixes) - series of diffraction images 

coordinate_matrix = dlmread(strcat('c',peaks,'.txt'));
peaks_intensity = peak_profile_fit(coordinate_matrix, total_image);
dlmwrite(strcat(peaks, "_intensity.txt"),peaks_intensity);

end


function [ sorted_intensity] = peak_profile_fit(coord_matrix, image)
% Fit 1D integrated intensity profiles to Gaussian curve
% and sorts by the value of delay

gauss = fittype(...
    'Am/w*exp(-2*(x-x0)*(x-x0)/w/w)+Bg+kBg*x','coefficients',...
    {'Am','x0','Bg','kBg','w'},'independent',{'x'});

%set the integration window size
% chech in ImageJ that this is an appropriate window size
incrX=120;
incrY=40;

total_intensity = dlmread('intensity_total.txt')/1e8;

x = coord_matrix(:,1);
y = coord_matrix(:,2);

num_of_points = length(x);
point = cell(num_of_points,1);

% preallocating vectors of amplitudes
steps = length(image);
amplitude = zeros(4,steps);
intensity = zeros(steps,1);
space = (1:1:incrX);

for n=1:steps
     
    for j =1:num_of_points
        % selecting equivalent points
        corner_x = x(j) - round(incrX/2);
        corner_y = y(j) - round(incrY/2);
        point{j} = IntensityWindow(corner_x,corner_y,incrX,incrY,image{n});
        
        % evaluating initial fitting parameters
        profile = point{j}.integrateY();
        Bg(j) = profile(1);
        Am(j) = max(profile);
        xc(j) = round(incrX/2);    
    end

    
    figure(2)
    
    for j=1:num_of_points
        [obj,gof,opt] = fit(double(space'),double(point{j}.integrateY()),gauss,'StartPoint', [Am(j),xc(j),Bg(j),0,3]);
        amplitude(j,n)=obj.Am;
        plot(double(space),double(point{j}.integrateY()));
        hold on
        plot(obj)
    end
        hold off
        
        intensity(n) = sum(amplitude(:,n))/total_intensity(n);
         
end
    sorted_intensity = sort_intensity(intensity);
    figure(3)
    plot(sorted_intensity)
end

function sorted_intensity = sort_intensity(value)
 
% sort intensity aray according to the delay array (in case the delay stage
% moves in random directions)

steps = length(value);
delay = dlmread('delay.txt');

sorted_intensity = value;
for n=1:steps
    for m=2:steps
        if (delay(m-1)>delay(m))
            delay_aux=delay(m);
            delay(m)=delay(m-1);
            delay(m-1)=delay_aux;
            sorted_intensity_aux=sorted_intensity(m);
            sorted_intensity(m)=sorted_intensity(m-1);
            sorted_intensity(m-1)=sorted_intensity_aux;
        end
    end
end

end