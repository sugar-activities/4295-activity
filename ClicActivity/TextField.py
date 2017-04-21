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

class TextField(object):
    
    answer = ''
    writed = ''
    original = ''
    numCharsBefore = 0
    numCharsAdded = 0
    font = None
    background = None
    textCell = None
    resposta = ""

    
    def __init__(self,xmlTarget, gridFont, backgroundColor):

        self.font = gridFont
        self.background = backgroundColor
        text = xmlTarget.getElementsByTagName('text')
        target = xmlTarget.getElementsByTagName('target')
        idText = 0
        idTarget = 0
        self.resposta = ""
        childs = xmlTarget.childNodes
        for child in childs:
            if child.nodeName == 'text':
                '''Si hi ha text definit, s'afegeix'''
                self.answer += text[idText].firstChild.data + ' '
                self.writed += text[idText].firstChild.data + ' '
                idText += 1
            elif child.nodeName == 'target':
                '''Els targets no es mostren: es el que ha d'introduir l'usuari'''
                self.answer = text[idTarget].firstChild.data + ' '
                idTarget += 1
        self.answer = self.answer.upper()
        self.writed.strip()
        self.original = self.writed

    def Load(self,posx,posy,display_surf):

        width = self.font.size(self.answer)[0] + 100
        height = self.font.size(self.answer)[1]
        
        rect = pygame.Rect(posx, posy, width, height)
        self.textCell = TextCell(rect,0,'text')
        contentCell = ContentCell()
        contentCell.id = 0
        contentCell.img = pygame.Surface((width,height))
        contentCell.img.fill(self.background)
        
        self.textCell.contentCell = contentCell
        
        
    def isOverTextField(self,posx,posy):
        
        if self.textCell.isOverCell(posx,posy):
            self.printCursor(posx,posy)
            return True
        else:
            index = self.writed.find('|')
            if index != -1: #si es -1 no ha trobat el caracter
                textPart = self.writed.partition('|')
                self.numCharsAdded -= 1 #resta el char del cursor
                print textPart
                self.writed = textPart[0] + textPart[2]
                print self.writed
            return False

    def printCursor(self,posx,posy):
        if self.writed.find('|') == -1:
            textPart = ''
            if self.numCharsAdded == 0:
                rectPos = posx - self.textCell.Rect.left #posicio del ratoli respecte el rect del textField
                b = False
                for l in self.writed:
                    textPart += l
                    
                    if not b and self.font.size(textPart)[0] >= rectPos:
                        if len(textPart) <= len(self.writed):
                            self.numCharsBefore = len(textPart)
                            b = True
                            textPart += '|'
                            self.numCharsAdded += 1
            else:
                for i in range(self.numCharsBefore+self.numCharsAdded):
                    if self.writed[i] != '|':
                        textPart += self.writed[i]
                    else:
                        self.numCharsAdded -= 1
                textPart += '|'
                for i in range(self.numCharsBefore+self.numCharsAdded, len(self.writed)):
                    textPart += self.writed[i]
                self.numCharsAdded += 1
            self.writed = textPart
    
    def processKey(self,key):
        textPart = self.writed.partition('|')
        tmp = textPart[0]
        print key
        if key == 'backspace':
            if self.numCharsAdded > 1: #si nomes queda el cursor, no esborro mes
                self.numCharsAdded -= 1
                tmp = ''
                for i in range(len(textPart[0])-1): #copio tot menys la ultima lletra (s'esborra)
                    tmp += textPart[0][i]
        elif key == 'return':
            '''comproba si el contingut del TextField es correcte'''
            '''self.writed = tmp + textPart[2]
            if self.writed.upper() == self.answer:
                return True
            return False'''
            self.resposta = tmp
            print self.resposta
        else:
            tmp += key
            self.numCharsAdded += 1
        
        self.writed = tmp + textPart[1] + textPart[2]
        return self.resposta

    def borraTmp(self):
        tmp = ''
        
    def OnRender(self,display_surf):
        self.textCell.contentCell.img.fill(self.background)
        if self.numCharsAdded > 0:
            '''Printa el text per parts per pintar el text introduit diferent al original'''
            textPart = ''
            for i in range(self.numCharsBefore):
                textPart += self.writed[i]
            tmpSurf = self.font.render(textPart,1,Constants.colorBlack)
            textWidth = tmpSurf.get_width()
            self.textCell.contentCell.img.blit(tmpSurf,(0,0))
            
            textPart = ''
            print self.numCharsBefore, self.numCharsAdded, len(self.writed)
            for i in range(self.numCharsBefore, self.numCharsBefore+self.numCharsAdded):
                textPart += self.writed[i]
            tmpSurf = self.font.render(textPart,1,Constants.colorBlue)
            self.textCell.contentCell.img.blit(tmpSurf,(textWidth,0))
            textWidth += tmpSurf.get_width()
            
            textPart = ''
            for i in range(self.numCharsBefore+self.numCharsAdded,len(self.writed)):
                textPart += self.writed[i]
            tmpSurf = self.font.render(textPart,1,Constants.colorBlack)
            self.textCell.contentCell.img.blit(tmpSurf,(textWidth,0))
        
        else:
            
            tmpSurf = self.font.render(self.writed,1,Constants.colorBlack)
            self.textCell.contentCell.img.blit(tmpSurf,(0,0))
        self.textCell.OnRender(display_surf)
            
