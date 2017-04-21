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

class TextCell(object):
    '''
    classdocs
    '''
    Rect = None
    idCell = None
    type = None #if only text then type = "text", else type = target type
    contentCell= None #can be ContentCell object or any type of target object
    
    def __init__(self,rect,id,type):
        
        self.Rect = rect
        self.idCell = id
        self.type = type
        
    def isOverCell(self,x,y):
        
        if self.type == 'text':
            return self.Rect.collidepoint(x,y)
        
        elif self.type == 'option':
            '''mira si ha clicat a la llista i en quina part'''
            id = self.contentCell.isOverList(x,y)
            encert = self.contentCell.listClicked(id)
            return encert
        
        elif self.type == 'response':
            id = self.contentCell.isOverResponse(x,y)
            print 'el id de response clicado:', id
            self.contentCell.clicked = id
            return id
        
        elif self.type == 'textField':
            return self.contentCell.isOverTextField(x,y)
            
        '''TO DO if self.type == others'''

        return False
        
    def OnRender(self,display_surf):
        if self.type == 'text':
            display_surf.blit(self.contentCell.img,self.Rect)
        elif self.type == 'option':
            self.contentCell.OnRender(display_surf)
        elif self.type == 'response':
            self.contentCell.OnRender(display_surf)
        elif self.type == 'textField':
            self.contentCell.OnRender(display_surf)
        
    def OnRenderPressedCell(self,display_surf):
        if self.contentCell.border == True:
            pygame.draw.rect(display_surf,self.actualColorCell ,self.Rect,self.borderSize)
