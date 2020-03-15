# -*- coding: utf-8 -*-
"""
@author: Tatiana Konstantinova
"""
class IntensityWindow():
    
    def __init__(self,y,x,height,width,matrix):
        self.x = x
        self.y = y
        self.width = width
        self.hight = height
        self.intensity = matrix[y:y+height+1, x:x+width+1]
    
    def integrate2D(self):
        return sum(sum(self.intensity))
    
    def integrateY(self):
        return sum(self.intensity)
    
    def integrateX(self):
        return sum(self.intensity.T)
    

        
    
    