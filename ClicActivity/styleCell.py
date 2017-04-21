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
from pygame.locals import *

import pygame
import pygame.locals
from  ContentCell import ContentCell
import Constants

class StyleCell(object):
    transparent = False
    fontFamily = 'Arial'
    fontSize = 30
    fontBold= False
    
    fontItalic= False
    backgroundColor = Constants.colorBackground
    foregroundColor = (0,0,0)
    borderColor = Constants.colorCell
    hasBorder = True
    
     
    
    def __init__(self,xml):
        '''BackGround Color'''
        try:
            bgColor =xml.getElementsByTagName('color')[0].getAttribute('background')
            r = bgColor[2] + bgColor[3]
            g = bgColor[4] + bgColor[5]
            b = bgColor[6] + bgColor[7]
            r = int(r,16)
            g = int(g,16)
            b = int(b,16)
            self.backgroundColor = (r,g,b)
            print 'bgcolor d cell  = ', self.backgroundColor
        except:
            '''Default color'''
            pass
    
        '''foreground Color'''
        try:
            fgColor =xml.getElementsByTagName('color')[0].getAttribute('foreground')
            r = fgColor[2] + fgColor[3]
            g = fgColor[4] + fgColor[5]
            b = fgColor[6] + fgColor[7]
            r = int(r,16)
            g = int(g,16)
            b = int(b,16)
            self.foregroundColor = (r,g,b)
        except:
            '''Default color'''
            pass
        
        '''borderColor Color'''
        try:
            bColor =xml.getElementsByTagName('color')[0].getAttribute('border')
            r = bColor[2] + bColor[3]
            g = bColor[4] + bColor[5]
            b = bColor[6] + bColor[7]
            r = int(r,16)
            g = int(g,16)
            b = int(b,16)
            self.borderColor = (r,g,b)
        except:
            '''Default color'''
            pass
        try:
            border = xml.getAttribute('border')
            if border == 'false':
                self.hasBorder = False
        except:
            ''' Has no border -> default border'''
            pass
        try:
            font = xml.getElementsByTagName('font')[0].getAttribute('size')
            self.fontSize = int(font)
            if self.fontSize < Constants.minFontSize:
                self.fontSize = Constants.minFontSize
        except:
            pass
