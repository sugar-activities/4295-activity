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
from TextCell import *
import Constants

class Response(object):
    
    answer = []
    writed = []
    font = None
    background = None
    textCell = None
    clicked = None #indica el numero de cell clicat
    Cells = []
    totalWidth = 0
    
    def __init__(self,xmlTarget, gridFont, backgroundColor):
        
        self.font = gridFont
        self.background = backgroundColor
        tmpAnswer = xmlTarget.getElementsByTagName('answer')[0].firstChild.data
        tmpAnswer = tmpAnswer.upper()
        self.answer = []
        self.writed = []
        for letter in tmpAnswer:
            self.answer.append(letter)
            self.writed.append('')
        

    def Load(self,posx,posy,display_surf):
        
        self.Cells = []
        width = self.font.size(self.answer[0])[0]
        height = self.font.size(self.answer[0])[1]
        
        '''Crea els cells de la resposta'''
        for i in range(0,len(self.answer)):
            rect = pygame.Rect(posx,posy,width,height)
            textCell = TextCell(rect,i,'text')
            contentCell = ContentCell()
            contentCell.id = i
            contentCell.img = pygame.Surface((width,height)).convert()
            contentCell.img.fill(self.background)
            contentCell.border = False
            contentCell.letter = '_'
            tmpSurf = self.font.render(contentCell.letter,1,Constants.colorBlack)
            contentCell.img.blit(tmpSurf,(0,0))
            textCell.contentCell = contentCell
            
            self.Cells.append(textCell)
            self.totalWidth += width
            posx += rect.width
        
        
    def isOverResponse(self,posx,posy):
        '''Comprova si ha clicat al response i, en cas afirmatiu, retorna sobre quina cell'''

        for cell in self.Cells:
            if cell.isOverCell(posx,posy):
                return cell.contentCell.id
        
        return None
    
    
    def printLetter(self):
        self.Cells[self.clicked].contentCell.img.fill(self.background)
        if self.writed[self.clicked] == '_':
            color = Constants.colorBlack
        elif self.writed[self.clicked] == self.answer[self.clicked]:
            color = Constants.colorBlue
        else:
            color = Constants.colorRed
            
        tmpSurf = self.font.render(self.Cells[self.clicked].contentCell.letter,1,color)
        self.Cells[self.clicked].contentCell.img.blit(tmpSurf,((self.Cells[self.clicked].contentCell.img.get_width() - tmpSurf.get_width())/2,0))
        
        '''Selecciona la seguent lletra'''
        if self.clicked < len(self.answer)-1:
            self.clicked += 1
        
        return self.clicked
    
    def OnRender(self,display_surf):
        
        for cell in self.Cells:
            if self.clicked != None:
                pygame.draw.rect(display_surf,Constants.colorPressedCell,self.Cells[self.clicked].Rect,2)
            cell.OnRender(display_surf)
            
            