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

class OptionList(object):
    optionList = []
    answer = ''
    font = None
    Cells = []
    openCell = None
    textCell = None
    listOpen = False
    textRect = None
    optionsRect = None
    
    def __init__(self,xmlTarget, gridFont):

        self.optionList = []

        self.font = gridFont
        self.answer = xmlTarget.getElementsByTagName('answer')[0].firstChild.data
        options = xmlTarget.getElementsByTagName('option')
        '''Agafem les opcions'''
        for opt in options:
            self.optionList.append(opt.firstChild.data)

    def Load(self,posx,posy,display_surf):
        
        self.Cells = []
        
        height = self.font.size(self.optionList[0])[1] + 4 #perque quedi mes espaiat
        posy = posy - 2 #perque quedi centrat amb el nou tamany, respecte la resta del text
        
        '''Crea el cell visible constantment'''
        rect = pygame.Rect(posx,posy,Constants.widthOpt,height)
        self.textCell = TextCell(rect,-2,'text')
        contentCell = ContentCell()
        contentCell.id = -2
        contentCell.img = pygame.Surface((Constants.widthOpt,height)).convert()
        contentCell.img.fill(Constants.colorWhite)
        contentCell.border = False
        self.textCell.contentCell = contentCell
        
        '''Crea el cell del boto per desplegar la llista'''
        rect = pygame.Rect(posx + Constants.widthOpt,posy,height,height)
        self.openCell = TextCell(rect,-1,'text')
        contentCell = ContentCell()
        contentCell.id = -1
        tmpsurf = self.font.render('V',1,Constants.colorBlack)
        
        contentCell.img = pygame.Surface((height,height)).convert()
        contentCell.img.fill(Constants.colorCelestial)
        contentCell.img.blit(tmpsurf,((rect.width - self.font.size('V')[0])/2, 2))
        contentCell.border = True
        self.openCell.contentCell = contentCell
        
        '''Crea els cells amb les opcions disponibles'''
        yActual = posy + height
        id = 0
        self.optionsRect = pygame.Rect(posx, yActual, Constants.widthOpt + self.openCell.Rect.width, height*len(self.optionList))
        for opt in self.optionList:
            rect = pygame.Rect(posx,yActual,Constants.widthOpt,height)
            cell = TextCell(rect,id,'text')
            
            tmpSurf = self.font.render(self.optionList[id],1,Constants.colorBlack)
            
            contentCell = ContentCell()
            contentCell.id = id
            contentCell.img = pygame.Surface((Constants.widthOpt + self.openCell.Rect.width,height))
            contentCell.img.fill(Constants.colorWhite)
            contentCell.img.blit(tmpSurf,(2,2))
            contentCell.border = False
            
            cell.contentCell = contentCell
            self.Cells.append(cell)
            
            yActual += height
            id += 1
        
        
    def isOverList(self,posx,posy):
        '''Comprova si ha clicat a la llista i, en cas afirmatiu, retorna sobre quina cell'''

        if self.listOpen:
            for cell in self.Cells:
                if cell.isOverCell(posx,posy):
                    return cell.contentCell.id

        if self.openCell.isOverCell(posx,posy):
            return self.openCell.contentCell.id
        
        return None #if clic was not over list
    
    def listClicked(self,idCell):
        '''Fa els canvis corresponents depenent on ha fet clic'''
        
        encert = False
        
        if idCell == -1:
            self.listOpen = not self.listOpen
        elif idCell == None:
            self.listOpen = False
        else:
            if self.optionList[idCell] == self.answer:
                color = Constants.colorBlue
                encert = True
            else:
                color = Constants.colorRed
            
            tmpSurf = self.font.render(self.optionList[idCell],1,color)
            self.textCell.contentCell.img.fill(Constants.colorWhite)
            self.textCell.contentCell.img.blit(tmpSurf,(2,2))
            self.listOpen = False
            
        return encert #comunica a l'activitat si ha encertat
            
            
    def OnRender(self,display_surf):
        self.textCell.OnRender(display_surf)
        self.openCell.OnRender(display_surf)
        pygame.draw.rect(display_surf,Constants.colorBlack,self.textCell.Rect,1)
        pygame.draw.rect(display_surf,Constants.colorBlack,self.openCell.Rect,1)
        if self.listOpen:
            for cell in self.Cells:
                cell.OnRender(display_surf)
            pygame.draw.rect(display_surf,Constants.colorBlack,self.optionsRect,1)
            
            