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

import pygame
from pygame import *

from Activity import  Activity
from Grid import Grid
from styleCell import StyleCell

class MemoryGame(Activity):

    Grid1 = None
    PressedCell = None

    color = None
 
     
    def Load(self, display_surf ):
        self.setBgColor(display_surf)
        ''' ----Dos posibilidades en XML----
            
            -1 Grid: Hay que doblar el tamano del Grid para duplicar las posibilidades
            -2 Grids: Hay que printar todas las posibilidades
        '''
        
        '''Loading xml values'''
  
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        self.Grid1 = Grid(xmlGrid1)
        self.styleCell = StyleCell(xmlGrid1)

        orientation =self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')

        ''' Calculate Real size'''
        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            self.Grid1.numRows  = self.Grid1.numRows *2
            
        else:
            '''Sumamos el width al tamano total'''
            self.Grid1.numCols =  self.Grid1.numCols * 2
        
        width = self.Grid1.cellWidth * self.Grid1.numCols
        height = self.Grid1.cellHeight * self.Grid1.numRows

        
        '''Maximize size'''
        coef = self.calculateCoef(width, height)
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef
        
        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT
        
        '''Calculate position to be centered'''
        xCenter = (Constants.ACTIVITY_WIDTH - width) / 2
        xCenter = max(xActual,xCenter)
        yCenter = (Constants.ACTIVITY_HEIGHT - height) / 2
        yCenter = max(yActual,yCenter)
        
        '''Cargamos grupo de celdas comunes...'''
        cellsPrimary = self.xmlActivity.getElementsByTagName('cells')[0]

        '''Load grid...
            Notar que el NumCols se ha multiplicado x 2 para Duplicar el tamano del Grid...
        '''
        
        self.Grid1.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xCenter ,yCenter, display_surf)
        '''Caso de 2 Grids:'''

        if self.xmlActivity.getElementsByTagName('cells').length == 2:
            
            '''Cargamos secondaryCells'''
            cellsSecondary = self.xmlActivity.getElementsByTagName('cells')[1]
            self.styleCell2 = StyleCell(cellsSecondary)
            
            '''Cargamos primer Grid del XML'''
            cells = cellsPrimary.getElementsByTagName('cell')
            '''indexCell  = Numero de Celda que ocupa:'''
            indexCell = 0
            indexCell = self.doBucle(cells,indexCell, self.styleCell2)
            
            '''Cargamos segundo Grid del XML'''
            cells = cellsSecondary.getElementsByTagName('cell')
            
            self.doBucle(cells,indexCell, self.styleCell2)

        else:
            '''indexCell  = Numero de Celda que ocupa:'''
            indexCell = 0
            
            '''Cargamos primer Grid del XML'''
            cells = cellsPrimary.getElementsByTagName('cell')
            indexCell = self.doBucle(cells,indexCell,self.styleCell)
            
            '''Recargamos el primer Grid del XML'''
            indexCell = self.doBucle(cells,indexCell,self.styleCell)
            
        self.Grid1.unsort()

    def doBucle(self,cells,i, style): 
        id = 0
        for cell in cells:
            copy = self.Grid1.Cells[i].contentCell.img.copy()      
            self.printxmlCellinCell(self.Grid1.Cells[i], cell, style)         

            '''Guardamos las imagenes en el Grid'''   
            self.Grid1.Cells[i].contentCell.img2 = self.Grid1.Cells[i].contentCell.img
            self.Grid1.Cells[i].contentCell.img = copy
            self.Grid1.Cells[i].contentCell.id = id 
            id = id+1
            i = i+1
        return i
    
    def OnEvent(self,PointOfMouse):
        for cell in self.Grid1.Cells:
            print 'antes de la instruccion  pointOfMouse=',PointOfMouse
            x  = PointOfMouse[0]
            y = PointOfMouse[1] 
            if cell.isOverCell(x,y):
                #si la celda ya ha sido 
                if cell.contentCell.img2 !=None:
                    # celda anterior apretada...
                    if self.PressedCell != None:
                        #los dos son iguales
                        print 'id PressedCell = ',self.PressedCell.contentCell.id
                        print 'id cell = ',cell.contentCell.id
                        if self.PressedCell.contentCell.id == cell.contentCell.id:
                            if self.PressedCell.idCell != cell.idCell:
                                print 'COINCIDEN LAS CELDAS!!'
                                 
                                cell.contentCell.img = cell.contentCell.img2
                                #anulamos valor de img2 para indicar k ta ok
                                cell.contentCell.img2 = None
                                self.PressedCell.contentCell.img2 = None
                                
    
                                self.PressedCell = None
                                self.play_sound(Constants.Sounds.OK)
                            #los dos son diferentes..
                        else:
                            self.play_sound(Constants.Sounds.ERROR)
                            self.changeSecondImage(self.PressedCell)

                            self.PressedCell.actualColorCell = Constants.colorCell
                            self.changeSecondImage(cell)

                            self.PressedCell = cell
                       
                    #celda anterior no apretada
                    else:
    
                        self.PressedCell = cell
                        self.changeSecondImage(cell)


    def changeSecondImage(self,cell): 
        tmpImg  = cell.contentCell.img
        cell.contentCell.img = cell.contentCell.img2
        cell.contentCell.img2= tmpImg

        
    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        #repintamos el grid...
        self.Grid1.OnRender(display_surf)
        #si la celda se ha apretado, la pintamos ( por los bordes)
        if self.PressedCell != None :
            self.PressedCell.OnRender(display_surf)
       
          
    def isOverActivity(self,PointOfMouse):
        return True
        
    def isGameFinished(self):
        finish = True
        for cell in self.Grid1.Cells:
            if cell.contentCell.img2 != None:
                finish = False
        return finish
       

        

        