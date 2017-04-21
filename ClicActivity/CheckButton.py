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
from pygame import *
import Constants

class CheckButton(object):
    '''
    classdocs
    '''
    Rect = None
    Surf = None
    Text = ''
    
    def __init__(self,checkText):
        self.font = pygame.font.Font(None,30)
        
        self.Surf = pygame.surface.Surface((Constants.ACTIVITY_WIDTH,40))
        self.Surf.fill(Constants.colorCelestial)
        self.Rect = pygame.Rect((Constants.MARGIN_LEFT,Constants.ACTIVITY_HEIGHT + Constants.MARGIN_TOP - 40),(self.Surf.get_size()))
        self.Text = checkText
        
    def isOverCheck(self,x,y):
        
        if self.Rect.collidepoint(x,y):
            return True

        return False
        
    def OnRender(self,display_surf):
        tmpSurf = self.font.render(self.Text,1,Constants.colorBlack)
        self.Surf.blit(tmpSurf,((self.Rect.width - tmpSurf.get_width()) / 2,(self.Rect.height - tmpSurf.get_height())/2))
        display_surf.blit(self.Surf,self.Rect)
        pygame.draw.rect(display_surf,Constants.colorBlack,self.Rect,2)

