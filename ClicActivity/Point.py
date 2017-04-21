''' 
    This file is part of Sugar-Clic
    
    Sugar-Clic is copyrigth 2009 by Maria Jose Casany Guerrero and Marc Alier Forment
    of the Universitat Politecnica de Catalunya http://www.upc.edu
    Contact info: Marc Alier Forment granludo @ gmail.com or marc.alier
    @ upc.edu
    
    Sugar-Clic is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Sugar-Clic is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with Sugar-Clic. If not, see <http://www.gnu.org/licenses/>.
    


    @package sugarclic
    @copyrigth 2009 Marc Alier, Maria Jose Casany marc.alier@upc.edu
    @copyrigth 2009 Universitat Politecnica de Catalunya http://www.upc.edu
    
    @autor Marc Alier
    @autor Jordi Piguillem
    
    @license http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
'''
from math import sqrt
import unittest

class Point(object):
    """Point class with public x and y attributes """
 
    def __init__(self, v):
        
        self.x = v[0]
        self.y = v[1]
 
    def dist(self, point):
        """return the Euclidian distance between self and p"""
        dx = self.x - point.x
        dy = self.y - point.y
        return sqrt(dx*dx + dy*dy)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self, x):
        self.x = x
    def getPoint(self):
        return (self.x,self.y) 
    def setY(self,y):
        self.y = y
        
    def setLocation(self, punt):
        self.x = punt.x
        self.y = punt.y
        
    def reset(self):
        self.x = 0
        self.y = 0

    def __add__(self, point):
        """return a new point found by adding self and point. This method is called by e.g. point+q for points p and q"""
        return Point(self.x + point.x, self.y + point.y)
 
    def __repr__(self):
        """return a string representation of this point. This method is called by the repr() function, andalso the str() function. It should produce a string that, when evaluated, returns a point with the same data."""
        return 'Point(%d,%d)' % (self.x, self.y)
    
    def equals (self, point):
        return self.x == point.x and self.y==point.y
