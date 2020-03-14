classdef IntensityWindow
    % class for operating with intensities inside a rectangular window
    
    properties
        x % left top corner of the window
        y
        width
        hight
        intensity 
    end
    
    methods
        function obj = IntensityWindow(x,y,width,hight,matrix)
            obj.x = x;
            obj.y = y;
            obj.width = width;
            obj.hight = hight;
            obj.intensity = matrix(y:y+hight-1,x:x+width-1);
        end
        
        function integrated2D = integrate2D(window)
            % calculate total intensity within the window
            integrated2D = sum(sum(window.intensity));
        end
        
        function integratedX = integrateX(window)
            % calculate vertical profile within the window
            integratedX = zeros(window.hight,1);
            for j = 1:window.hight
                integratedX(j) = sum(window.intensity(j, :));
            end
        end
        
        function integratedY = integrateY(window)
            % calculate horizontal profile within the window
            integratedY = zeros(window.width,1);
            for j = 1:window.width
                integratedY(j) = sum(window.intensity(:, j));
            end
        end
        
    end
    
end