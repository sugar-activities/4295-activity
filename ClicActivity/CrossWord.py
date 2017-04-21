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
import Constants

from Activity import  Activity
from Grid import Grid
from styleCell import StyleCell
import pygame
import random

class CrossWord(Activity):

    textGrid = None
    cellsAcrossGrid = None
    cellsDownGrid = None
    acrossClues = []
    downClues = []
    text = [] #Solucio per comprovar correctesa
    acrossItems = [] #item que li correspon a la cela
    downItems = []
    blancs = 0
    cols = 0
    pressedTextCell = None #Cell of textGrid where to type
    pressedDirectionCell = None #Cell across or down
    acrossCell = None
    downCell = None
    direction = None #'across' or 'down'
    xmlCellsAcross = None
    xmlCellsDown = None
    xmlText = None
    textHasBorder = False

    
    
    def Load(self, display_surf ):
        self.setBgColor(display_surf)
        
        '''Loading xml values'''
        
        '''xml amb la solucio del crossword'''
        self.xmlText = self.xmlActivity.getElementsByTagName('textGrid')[0]
        '''xml amb les definicions de les paraules'''
        self.xmlCellsAcross = self.xmlActivity.getElementsByTagName('cells')[0]
        self.xmlCellsDown = self.xmlActivity.getElementsByTagName('cells')[1]
        
        '''Crea el grid del crossword'''
        self.textGrid = Grid(self.xmlText)
        self.styleCell = StyleCell(self.xmlText)
        '''Crea el grid de les definicions horitzontals'''
        self.cellsAcrossGrid = Grid(self.xmlCellsAcross)
        '''Crea el grid de les definicions verticals'''
        self.cellsDownGrid = Grid(self.xmlCellsDown)
            
        orientation =  self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')   
        
        ''' Calculate Real size'''
        heightText = self.textGrid.cellHeight * self.textGrid.numRows
        widthText = self.textGrid.cellWidth * self.textGrid.numCols

        '''Dimensions de acrossGrid = downGrid, nomes agafo tamany amb un'''
        heightCells = self.cellsAcrossGrid.cellHeight
        widthCells = self.cellsAcrossGrid.cellWidth #+ self.cellsAcrossGrid.cellHeight #el cell de l'orientacio es igual d'alt, que d'ample
        
        '''Maximize size'''
        if orientation == 'AB' or 'BA':
            coef = self.calculateCoef(widthText+widthCells,heightText)
        else:
            if widthText >= (widthCells*2):
                coef = self.calculateCoef(widthText,heightText+heightCells)
            else:
                coef = self.calculateCoef(widthCells*2,heightText+heightCells)

        heightText = heightText * coef
        widthText = widthText * coef
        
        heightCells = heightCells * coef
        widthCells = widthCells * coef
        print 'heightCell: ' , heightCells
        print 'widthCell: ', widthCells

        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT
        
        if orientation == 'AB':
            xText = (Constants.ACTIVITY_WIDTH - widthText - widthCells - 10) / 2
            xText = max(xActual,xText)
            yText = (Constants.ACTIVITY_HEIGHT - heightText) / 2
            xCells = xText + widthText + 10
            yCells = (Constants.ACTIVITY_HEIGHT - heightCells*2) / 2
            self.textGrid.Load(self.textGrid.numRows,self.textGrid.numCols,widthText,heightText,xText,yText, display_surf)
            self.cellsAcrossGrid.Load(self.cellsAcrossGrid.numRows,self.cellsAcrossGrid.numCols,widthCells,heightCells,xCells,yCells, display_surf)
            self.cellsDownGrid.Load(self.cellsDownGrid.numRows,self.cellsDownGrid.numCols,widthCells,heightCells,xCells,yCells+heightCells, display_surf)
        elif orientation == 'BA':
            xCells = (Constants.ACTIVITY_WIDTH - widthText - widthCells - 10) / 2
            yCells = (Constants.ACTIVITY_HEIGHT - heightCells*2) / 2
            xCells = max(xCells,xActual)
            xText = xCells + widthCells + 10
            yText = (Constants.ACTIVITY_HEIGHT - heightText) / 2
            self.textGrid.Load(self.textGrid.numRows,self.textGrid.numCols,widthText,heightText,xText,yText, display_surf)
            self.cellsAcrossGrid.Load(self.cellsAcrossGrid.numRows,self.cellsAcrossGrid.numCols,widthCells,heightCells,xCells,yCells, display_surf)
            self.cellsDownGrid.Load(self.cellsDownGrid.numRows,self.cellsDownGrid.numCols,widthCells,heightCells,xCells,yCells+heightCells, display_surf)
        elif orientation == 'AUB':
            xText = (Constants.ACTIVITY_WIDTH - widthText) / 2
            yText = (Constants.ACTIVITY_HEIGHT - heightText - heightCells - 10) / 2
            xCells = (Constants.ACTIVITY_WIDTH - widthCells*2) / 2
            yCells = yText + heightText + 10
            self.textGrid.Load(self.textGrid.numRows,self.textGrid.numCols,widthText,heightText,xText,yText, display_surf)
            self.cellsAcrossGrid.Load(self.cellsAcrossGrid.numRows,self.cellsAcrossGrid.numCols,widthCells,heightCells,xCells,yCells, display_surf)
            self.cellsDownGrid.Load(self.cellsDownGrid.numRows,self.cellsDownGrid.numCols,widthCells,heightCells,xCells+widthCells,yCells, display_surf)
        elif orientation == 'BUA':
            xCells = (Constants.ACTIVITY_WIDTH - widthCells*2) / 2
            yCells = (Constants.ACTIVITY_HEIGHT - heightText - heightCells - 10) / 2
            xText = (Constants.ACTIVITY_WIDTH - widthText) / 2
            yText = yCells + heightCells + 10
            self.textGrid.Load(self.textGrid.numRows,self.textGrid.numCols,widthText,heightText,xText,yText, display_surf)
            self.cellsAcrossGrid.Load(self.cellsAcrossGrid.numRows,self.cellsAcrossGrid.numCols,widthCells,heightCells,xCells,yCells, display_surf)
            self.cellsDownGrid.Load(self.cellsDownGrid.numRows,self.cellsDownGrid.numCols,widthCells,heightCells,xCells+widthCells,yCells, display_surf)
                
        self.textHasBorder = self.textGrid.hasBorder
        self.text = []
        '''Agafem la solucio del textGrid per comprovar al final la correctesa'''
        rows = self.xmlText.getElementsByTagName('row')
        for row in rows:
            row = row.firstChild.data
            self.cols = len(row)
            for i in range(0,self.cols):
                self.text.append(row[i])
        item = 0
        for i in range(0,len(self.text)):
            if i % self.cols == self.cols:
                item = 0
            if self.text[i] == '*':
                self.textGrid.Cells[i].contentCell.letter = self.text[i]
                self.textGrid.Cells[i].contentCell.img.fill(Constants.colorBlack)
            else:
                self.acrossItems = item
                item += 1
                self.textGrid.Cells[i].contentCell.letter = ' '
                #imprimeixo en blanc per pintar la cell, sino dixa color per defecte
                self.printLetterinCell(self.textGrid.Cells[i],self.xmlText)
                self.blancs += 1 #per saber quants espais hi ha per omplir
        
        '''Carreguem les definicions'''
        self.loadClues()
        
        '''Per defecte la direccio es across i seleccionem la primera cell del text disponible'''
        self.direction = 'across'
        self.pressedDirectionCell = self.cellsAcrossGrid.Cells[0]
        self.pressedDirectionCell.actualColorCell = Constants.colorPressedCell
        self.pressedTextCell = self.textGrid.Cells[0]
        self.pressedTextCell.contentCell.id = -1 #per que seleccioni la primera possible
        self.acrossCell = self.cellsAcrossGrid.Cells[1]
        self.downCell = self.cellsDownGrid.Cells[1]
        self.selectNextCell()
        self.showClues()
        
    def OnEvent(self,PointOfMouse):
        
        '''Si click al textGrid'''
        for cell in self.textGrid.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                print cell.contentCell.id
                if cell.contentCell.letter != '*':
                    '''Reset actual pressedCell'''
                    self.pressedTextCell.contentCell.border = self.textHasBorder
                    self.pressedTextCell.actualColorCell = Constants.colorCell
                    '''Select new pressedCell'''
                    self.pressedTextCell = cell
                    self.pressedTextCell.actualColorCell = Constants.colorPressedCell
                    '''Show definitions'''
                    self.showClues()
        
        '''Si click al acrossGrid'''
        if self.cellsAcrossGrid.Cells[0].isOverCell(PointOfMouse[0],PointOfMouse[1]):
            self.pressedDirectionCell.actualColorCell = Constants.colorCell
            self.direction = 'across'
            self.pressedDirectionCell = self.cellsAcrossGrid.Cells[0]
            self.pressedDirectionCell.actualColorCell = Constants.colorPressedCell
        
        '''Si click al downGrid'''
        if self.cellsDownGrid.Cells[0].isOverCell(PointOfMouse[0],PointOfMouse[1]):
            self.pressedDirectionCell.actualColorCell = Constants.colorCell
            self.direction = 'down'
            self.pressedDirectionCell = self.cellsDownGrid.Cells[0]
            self.pressedDirectionCell.actualColorCell = Constants.colorPressedCell
        
    def OnKeyEvent(self,keyPressed):
        ''' keyPressed is the identifier of the key, like a letter,"delete","backspace"...'''
        print 'Entry in KeyEvent!!'
        if keyPressed == 'delete' or keyPressed == 'backspace':
            self.pressedTextCell.contentCell.letter = ' '
            self.blancs += 1

        else: #Si es una lletra l'escrivim a la cell selccionada
            if self.pressedTextCell.contentCell.letter == ' ':
                '''Si no hi havia cap lletra restem en 1 els blancs,
                    si ja hi havia alguna lletra, es sobreescriu i no resta blancs'''
                self.blancs -= 1
            
            self.pressedTextCell.contentCell.letter = keyPressed
            print 'letra grabada: ',self.pressedTextCell.contentCell.letter
        
        '''Imprimeix el canvi i selecciona la seguent'''
        self.printLetterinCell(self.pressedTextCell,self.xmlText)
        self.selectNextCell()
    
    def selectNextCell(self):
        actualId = self.pressedTextCell.contentCell.id
        ok = False
        if self.direction == 'across':
            while(not ok):
                actualId += 1
                if actualId >= len(self.text): 
                    actualId = 0
                if self.text[actualId] != '*':
                    ok = True
                            
        else: #direction == down
            while(not ok):
                if actualId == len(self.text) - 1: 
                    '''estava a la ultima cell->tornem al principi'''
                    actualId = 0
                elif actualId+self.cols >= len(self.text):
                    '''estava al final d'una columna -> saltem a la seguent'''
                    saltCol = len(self.text) - self.cols
                    actualId = actualId - saltCol + 1
                else:
                    actualId += self.cols
                    
                if self.text[actualId] != '*':
                    ok = True
                    
        '''Reset actual pressedCell'''
        if self.pressedTextCell.contentCell.id == -1:
            self.pressedTextCell.contentCell.id = 0
        self.pressedTextCell.contentCell.border = self.textHasBorder
        self.pressedTextCell.actualColorCell = Constants.colorCell
        '''Select new pressedCell'''
        self.pressedTextCell = self.textGrid.Cells[actualId]
        self.pressedTextCell.actualColorCell = Constants.colorPressedCell
        self.showClues()
      
    def loadClues(self):
        self.acrossClues = []
        self.downClues = []
        for i in range(self.textGrid.numRows):
            self.acrossClues.append('')
        for i in range(self.cols):
            self.downClues.append('')
            
        across = self.xmlCellsAcross.getElementsByTagName('cell')
        for cell in across:
            try:
                definition = cell.getElementsByTagName('p')[0].firstChild.data
            except:
                definition = None
            if definition != None:
                id = int(cell.getAttribute('id'))
                #item = int(cell.getAttribute('item'))
                self.acrossClues[id] = definition
                
        down = self.xmlCellsDown.getElementsByTagName('cell')
        for cell in down:
            try:
                definition = cell.getElementsByTagName('p')[0].firstChild.data
            except:
                definition = None
            if definition != None:
                id = int(cell.getAttribute('id'))
                #item = int(cell.getAttribute('item'))
                self.downClues[id] = definition
          
            
        for i in range(0,12):
            try:
                print i
                print self.acrossClues[i]
            except:
                pass
        for i in range(0,12):
            try:
                print i
                print self.downClues[i]
            except: pass
    
    def showClues(self):
        fila = int(self.pressedTextCell.contentCell.id // self.cols)
        columna = self.pressedTextCell.contentCell.id % self.cols
        
        self.acrossCell.contentCell.letter = self.acrossClues[fila]
        self.downCell.contentCell.letter = self.downClues[columna]
        
        self.printLetterinCell(self.acrossCell,self.xmlCellsAcross)
        self.printLetterinCell(self.downCell,self.xmlCellsAcross)
    
    
    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        '''repintamos el grid...'''
        self.textGrid.OnRender(display_surf)
        self.cellsAcrossGrid.OnRender(display_surf)
        self.cellsDownGrid.OnRender(display_surf)
        
        if self.pressedTextCell != None:
            self.pressedTextCell.contentCell.border = True
            self.pressedTextCell.OnRenderPressedCell(display_surf)
        
    def isGameFinished(self):
        return self.completeAndCorrect()
 
    def completeAndCorrect(self):
        if self.blancs > 0:
            return False
        else:
            for i in range(0,len(self.text)):
                if self.textGrid.Cells[i].contentCell.letter != self.text[i]:
                    return False
        '''Si no retorna abans, significa que esta tot correcte i acaba l'activitat'''
        return True
        
        