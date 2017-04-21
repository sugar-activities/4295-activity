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
from  ContentCell import ContentCell
import Constants

class Cell(object):
    '''
    classdocs
    '''
    Rect = None
    #Points = None
    idCell = None
    contentCell= None
    borderSize = Constants.DEFAULT_BORDER_SIZE
    #id =  None
    actualColorCell = Constants.colorCell
    hasBorder = True
    redirect = None
   
    
    def __init__(self,rect,display_surf,id,hasBorder):

        self.Rect = rect
        self.Point=[]
        self.idCell = id
        #self.Points = points
        self.hasBorder = hasBorder
        if hasBorder:
            pygame.draw.rect(display_surf,Constants.colorCell,self.Rect,self.borderSize)

    def isOverCell(self,x,y):
        #print 'x=',x,' y=',y,' Rect=',self.Rect
        print 'llego a la funcion isovercell'
        if self.Rect.collidepoint(x,y):
                return True
        else:
            return False
    def OnRender(self,display_surf):
        
        #display_surf.fill(Constants.colorBackground,self.Rect)
        display_surf.blit(self.contentCell.img,self.Rect)
        
        ''' Draw borders'''
        if self.hasBorder == True or self.actualColorCell != Constants.colorCell:
            pygame.draw.rect(display_surf,self.actualColorCell ,self.Rect,self.borderSize)
        
    def OnRenderPressedCell(self,display_surf):
        if self.hasBorder == True or self.actualColorCell != Constants.colorCell:
            pygame.draw.rect(display_surf,self.actualColorCell ,self.Rect,self.borderSize)
