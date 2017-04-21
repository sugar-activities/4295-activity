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
from Cell import *
from Constants import *
from pygame import surface
from pygame.locals import *
import os
import pygame
import random


class Grid(object):

    Cells = None
    rows = None
    cols = None
    cellHeight = None
    cellWidth  = None
    transparent = False
    fontFamily = 'Arial'
    fontSize = 30
    fontBold= False
    fontItalic= False
    backgroundColor = Constants.colorBackground
    foregroundColor = Constants.colorWhite
    borderColor = Constants.colorCell
    hasBorder = True
    imagePath = None
    crossClues = False
    across = False
    
    def __init__(self,xml=None, pathToMedia=None):

        '''We can change the try/except by hasAttribute'''
        '''Grid is a vector of cells'''
        self.Cells = []
        '''BackGround Color'''
        if xml != None:
            try:
                bgColor =xml.getElementsByTagName('color')[0].getAttribute('background')
                print 'el color k trae de background es:',bgColor
                r = bgColor[2] + bgColor[3]
                g = bgColor[4] + bgColor[5]
                b = bgColor[6] + bgColor[7]
                r = int(r,16)
                g = int(g,16)
                b = int(b,16)
                self.backgroundColor = (r,g,b)
                print 'he informado bgcolor',bgColor
            except:
                '''Default color'''
                pass
        
            '''foreground Color'''
            try:
                color =xml.getElementsByTagName('color')[0].getAttribute('foreground')
                r = color[2] + color[3]
                g = color[4] + color[5]
                b = color[6] + color[7]
                r = int(r,16)
                g = int(g,16)
                b = int(b,16)
                self.foregroundColor = (r,g,b)
            except:
                '''Default color'''
                pass
            
            '''borderColor Color'''
            try:
                color =xml.getElementsByTagName('color')[0].getAttribute('border')
                self.borderColor = pygame.Color(hex(int(bgcolor, 16)))
            except:
                '''Default color'''
                pass
            try:
                self.cellHeight =  float(xml.getAttribute('cellHeight'))
                
                self.cellWidth =   float(xml.getAttribute('cellWidth'))
                
            except:
                self.cellHeight =  float(30)
                self.cellWidth =   float(40)

            self.hasBorder = False
            try:
                if xml.getAttribute('border') == "true":
                    self.hasBorder = True
            except:
                pass
            try:
                self.numRows = float(xml.getAttribute('rows'))
            except:
                self.numRows = 1
            try:
                self.numCols = float(xml.getAttribute('cols'))
            except:
                try:
                    '''Si l'atribut es columns es textGrid i rows <--> cols'''
                    tmp = self.numRows
                    self.numRows = float(xml.getAttribute('columns'))
                    self.numCols = tmp
                except:
                    self.numCols = 1
        
            self.ids = []
            ids = None
            
            if xml.hasAttribute('image'):
                self.imagePath = xml.getAttribute('image')
                if (pathToMedia !=None):
                    #pathToMedia = "/home/roger/NetBeansProjects/sugarhg/src/new/data/clics/plantes2"
                    img = pygame.image.load(pathToMedia+'/'+self.imagePath)
                    aux = img.get_size()
                    self.cellWidth, self.cellHeight = aux
                    self.cellWidth = self.cellWidth / self.numCols
                    self.cellHeight = self.cellHeight / self.numRows
                try:
                    ids = xml.getElementsByTagName('ids')[0].firstChild.nodeValue
                except:
                    ids = None

            if ids != None:
                idsList = ids.split(' ')
                for id in idsList:
                    self.ids.append(id)

            '''Comprova si el grid es de definicions de crosswords, te tractament diferent en load'''
            try:
                if xml.getAttribute('id') == 'acrossClues' or xml.getAttribute('id') == 'downClues':
                    self.crossClues = True
                    if xml.getAttribute('id') == 'acrossClues':
                        self.across = True
            except:
                pass
    

    def LoadWithImage (self,rows,cols,width,height,xInicial, yInicial,display_surf,pathToMedia):  
        ''' Load 1 image for the full Grid'''
        self.rows = int(rows)
        self.cols = int(cols)
        
        widthPart = width / self.cols
        heightPart  = height / self.rows
        self.cellHeight = heightPart
        self.cellWidth  = widthPart

        print self.imagePath
        
        img = pygame.image.load(pathToMedia+'/'+self.imagePath).convert_alpha()

        img2 = pygame.transform.scale(img, (int(width), int(height)))
        
        surfaceEmpty = surface.Surface((int(width), int(height)))

        if self.transparent == False: 
            print 'surface no transparent bgcolor =',self.backgroundColor
            surfaceEmpty.fill(self.backgroundColor)
        else:
            print 'surface transparent'
        
        surfaceEmpty.blit(img2,(0, 0)) 
        img2 = surfaceEmpty
        
        i = 0;
        actualRow = 0
        actualCol = 0
        xActual=xInicial
        yActual=yInicial
        ''' Calculate the size and the position of Rects'''

        
        while (i < self.rows*self.cols):
            
            '''Initializing the cell'''
            borderCell  = Rect(xActual,yActual,widthPart,heightPart)
            cell = Cell(borderCell,display_surf,i,self.hasBorder)
           
            '''Calculating the rect size and position'''
            rect  = Rect (xActual-xInicial,yActual-yInicial,widthPart,heightPart)
            '''cut the part of the image that goes in this cell'''
            img3 = img2.subsurface(rect)
            contentCell = ContentCell()
            contentCell.img  = img3
            if (self.ids == []):
                contentCell.id = i
            else:
                contentCell.id = int(self.ids[i])
            cell.contentCell = contentCell
            
            '''adding cell to grid..'''
            self.Cells.append(cell)
            
            
            actualCol = actualCol +1
            xActual = xActual+widthPart
            
            
            ''' Counters increment for the loop'''
            if actualCol == self.cols:
                actualCol = 0
                actualRow +=1

                yActual = yActual+heightPart
                xActual = xInicial
                
            i= i+1
            

    def Load (self,rows,cols,width,height,xInicial, yInicial,display_surf):  
        
        if self.crossClues:
            '''Tractament especific per grid de crossClues'''
            
            '''1r Crea el cell amb la imatge de la orientacio'''
            border  = Rect (xInicial,yInicial,width/4,height)
            cell = Cell(border,display_surf,0,self.hasBorder)
            
            surfaceEmpty = surface.Surface((int(width/4),int(height)))
            if self.across:
                img = pygame.image.load(Constants.Images.ACROSS).convert_alpha()
            else:
                img = pygame.image.load(Constants.Images.DOWN).convert_alpha()
            
            img2 = pygame.transform.scale(img,surfaceEmpty.get_size())
            surfaceEmpty.blit(img2,(0,0))

            contentCell = ContentCell()
            
            contentCell.id = 0
            contentCell.img = surfaceEmpty
            contentCell.border = self.hasBorder
            
            cell.contentCell = contentCell
            self.Cells.append(cell)
            
            '''2n Crea el cell per les definicions'''
            border  = Rect (xInicial+(width/4),yInicial,width-(width/4),height)
            cell = Cell(border,display_surf,1,self.hasBorder)
            
            surfaceEmpty = surface.Surface((int(width)-int(width/4),int(height)))
            
            if self.transparent == False: 
                print 'grid-> color fondo = ',self.backgroundColor
                surfaceEmpty.fill(self.backgroundColor)
            
            contentCell = ContentCell()
            
            contentCell.id = 1
            contentCell.img = surfaceEmpty
            contentCell.border = self.hasBorder
            
            cell.contentCell = contentCell
            self.Cells.append(cell)
            
        
        else:
            '''Si no es grid de crossClues, tractament general'''
            
            self.rows = int(rows)
            self.cols = int(cols)
            
            widthPart = width / self.cols
            heightPart  = height / self.rows
           
            
            surfaceEmpty = surface.Surface((int(widthPart),int(heightPart)),0)
                     
            
            '''IF INCORRECTE'''
            if self.transparent == False: 
                print 'grid-> color fondo = ',self.backgroundColor
                surfaceEmpty.fill(self.backgroundColor)
            else:
                
                print 'surface transparent'
    
            self.cellHeight = heightPart
            self.cellWidth  = widthPart    
            
            i = 0;
            actualRow = 0
            actualCol = 0
            xActual=xInicial
            yActual=yInicial
            while (i < self.rows*self.cols):
                
                border  = Rect (xActual,yActual,widthPart,heightPart)
                cell = Cell(border,display_surf,i,self.hasBorder)
    
                contentCell = ContentCell()
                
                contentCell.id = i
                contentCell.img = surfaceEmpty.copy()
                contentCell.border = self.hasBorder
                
                cell.contentCell = contentCell
                self.Cells.append(cell)
                
                actualCol = actualCol +1
                xActual = xActual+widthPart
                
                if actualCol == self.cols:
                    actualCol = 0
                    actualRow +=1
    
                    yActual = yActual+heightPart
                    xActual = xInicial
                    
                i= i+1

    def OnRender(self,display_surf):
        
        for cell in self.Cells:
            cell.OnRender(display_surf)
        for cell in self.Cells:
            cell.OnRenderPressedCell(display_surf)
        

    def changeImages(self,idCell1, idCell2):
        
        ''' Change the 2 cell images from a Grid '''
        contentCell1   = self.Cells[idCell1].contentCell
        contentCell2  = self.Cells[idCell2].contentCell
        
        self.Cells[idCell1].contentCell = contentCell2
        self.Cells[idCell2].contentCell = contentCell1

    def unsort(self, GridAux= None):
        i = 0
        ''' We do 50 times!!! maby only 10 loops necessary'''
        while (i< 50):
            num1 = random.randint(0, (self.rows*self.cols)-1)
            num2 = random.randint(0, (self.rows*self.cols)-1)
            self.changeImages(num1,num2)
            if(GridAux!= None):
                GridAux.changeImages(num1,num2)
            i = i+1