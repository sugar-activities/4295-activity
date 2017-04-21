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

from Activity import  Activity
from Grid import Grid
from styleCell import StyleCell

class SimpleAssociation(Activity):

    Grid1 = None
    PressedCell = None

    color = None


    def Load(self, display_surf ):
        self.setBgColor(display_surf)
        self.desactGrid1 = []
        self.desactGrid2 = []
        ''' ----Dos posibilidades en XML----

         orientation   -1 Grid: Hay que doblar el tamano del Grid para duplicar las posibilidades
            -2 Grids: Hay que printar todas las posibilidades
        '''

        '''Loading xml values'''


	orientation =  self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')

	'''Create 2 Grids'''
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        self.Grid1 = Grid(xmlGrid1, self.pathToMedia)
        xmlGrid2 = self.xmlActivity.getElementsByTagName('cells')[1]
        self.Grid2 = Grid(xmlGrid2, self.pathToMedia)

        try:
            xmlGrid3 = self.xmlActivity.getElementsByTagName('cells')[2]
            self.Grid3 = Grid(xmlGrid3, self.pathToMedia)
        except:
            self.Grid3 = Grid()

        self.Grid3.backgroundColor = self.Grid2.backgroundColor

        ''' Calculate Real size'''
        height = self.Grid1.cellHeight * self.Grid1.numRows
        width = self.Grid1.cellWidth * self.Grid1.numCols


        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            height = height + self.Grid2.cellHeight
        else:
            '''Sumamos el width al tamano total'''
            width = width + self.Grid2.cellWidth

        ''' Calculamos porcentaje...'''

        '''Maximize size'''
        coef = self.calculateCoef(width, height)

        '''Maximize size'''
        #coef = self.calculateCoef(width, height)
	#coefx = self.calculateCoefPart(height)
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef



        '''coef = self.calculateCoef(width2, height2)
	#coefx = self.calculateCoefPart(height2)
        height2 = self.Grid2.cellHeight * self.Grid2.numRows * coef
        width2 = self.Grid2.cellWidth * self.Grid2.numCols * coef'''

	print "paramentres"
	print height
	print self.Grid1.cellHeight
	print self.Grid1.numRows

        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT

        '''Cargamos grupo de celdas comunes...'''
        cellsPrimary = self.xmlActivity.getElementsByTagName('cells')[0]
        xGrid1 = (Constants.ACTIVITY_WIDTH - width) / 2
        yGrid1 = (Constants.ACTIVITY_HEIGHT - height) / 2
        xGrid1 = max(xGrid1,xActual)
        yGrid1 = max(yGrid1,yActual)

        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            newHeight = self.Grid2.cellHeight * coef
            yGrid1 = (Constants.ACTIVITY_HEIGHT - height - newHeight - 10) / 2
            yGrid1 = max(yGrid1,yActual)
            self.Grid2.Load(self.Grid2.numRows,self.Grid2.numCols,width,newHeight,xGrid1 ,yGrid1 + height +10, display_surf)
        else:
            '''Sumamos el width al tamano total'''
            newWidth = self.Grid2.cellWidth *coef
            xGrid1 = (Constants.ACTIVITY_WIDTH - width - newWidth - 10) / 2
            xGrid1 = max(xGrid1,xActual)
            self.Grid2.Load(self.Grid2.numRows,self.Grid2.numCols,newWidth,height,xGrid1 + width +10 ,yGrid1, display_surf)

        if self.Grid1.imagePath == None:
            self.Grid1.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf)

        try:
            '''if cells 2 not exists, only create an empty Grid'''
            if self.Grid3.imagePath == None:
                self.Grid3.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf)
                cells = xmlGrid3.getElementsByTagName('cell')
                self.styleCell = StyleCell(xmlGrid3)
                i = 0
                for i in range(len(cells)):
                    self.printxmlCellinCell(self.Grid3.Cells[i], cells,self.styleCell)
                    #i = i+1
            else:
                self.Grid3.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf,self.pathToMedia)
        except:
            pass

        '''Cargamos secondaryCells'''
        cellsSecondary = self.xmlActivity.getElementsByTagName('cells')[1]
        self.styleCell2 = StyleCell(cellsSecondary)

        '''Cargamos primer Grid del XML'''
        cells = cellsPrimary.getElementsByTagName('cell')
        self.styleCell = StyleCell(cellsPrimary)
        '''indexCell  = Numero de Celda que ocupa:'''
        indexCell = 0
        indexCell = self.doBucle(cells,indexCell)

        '''Cargamos segundo Grid del XML'''
        cells2 = cellsSecondary.getElementsByTagName('cell')

        if self.Grid1.imagePath != None:
            ''' 1 Imagen de fondo '''
            self.Grid1.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf,self.pathToMedia)

        i = 0
        id = 0

        for cell in cells2:
                self.printxmlCellinCell(self.Grid2.Cells[i], cell,self.styleCell2)
                #Guardamos las imagenes en el Grid
                self.Grid2.Cells[i].contentCell.img2 = self.Grid2.Cells[i].contentCell.img
                self.Grid2.Cells[i].contentCell.id = id
                id = id+1
                i = i+1

        #self.Grid3.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf,self.pathToMedia)

        if self.Grid1.imagePath == None:
            self.Grid1.unsort()

        if self.Grid2.imagePath == None:
            self.Grid2.unsort()

    def doBucle(self,cells,i):
        id = 0
        for cell in cells:
            self.printxmlCellinCell(self.Grid1.Cells[i], cell, self.styleCell)         
            '''Guardamos las imagenes en el Grid'''   
            self.Grid1.Cells[i].contentCell.img2 = self.Grid1.Cells[i].contentCell.img
            self.Grid1.Cells[i].contentCell.id = id
            id = id+1
            i = i+1
        return i

    def OnEvent(self,PointOfMouse):
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                #si la celda ya ha sido
                if self.desactGrid1.count(cell) == 0:
                    # celda anterior apretada...
                    if self.PressedCell != None:
                        #los dos son iguales
                        print 'id PressedCell = ',self.PressedCell.contentCell.id
                        print 'id cell = ',cell.contentCell.id
                        if self.PressedCell.contentCell.id == cell.contentCell.id:
                            #COINCIDES CELDAS
			    if self.PressedGrid ==2:
                                self.desactGrid2.append(self.PressedCell)
                                self.desactGrid1.append(cell)
                            	self.PressedCell.actualColorCell = Constants.colorCell
				self.PressedCell.contentCell.img.fill(Constants.colorBackground)
				self.PressedCell.contentCell.borders=False
				cell.contentCell.img.fill(Constants.colorBackground)
                                cell.contentCell.img = self.Grid3.Cells[cell.idCell].contentCell.img
                                cell.contentCell.img2 = None
                                self.PressedCell.contentCell.img2 = None
                                self.PressedCell = None

                            #los dos son diferentes..
                        else:

                            #self.changeSecondImage(self.PressedCell)
                            self.PressedCell.actualColorCell = Constants.colorCell
                            #self.changeSecondImage(cell)
                            self.PressedCell = None

                    #celda anterior no apretada
                    else:
                        self.PressedCell = cell
			self.PressedGrid = 1
                        #self.changeSecondImage(cell)
                    	self.PressedCell.actualColorCell = Constants.colorPressedCell

        for cell in self.Grid2.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                #si la celda ya ha sido
                if self.desactGrid2.count(cell) == 0:
                    # celda anterior apretada...
                    if self.PressedCell != None:
                        #los dos son iguales
                        print 'id PressedCell = ',self.PressedCell.contentCell.id
                        print 'id cell = ',cell.contentCell.id
                        if self.PressedCell.contentCell.id == cell.contentCell.id:
                            #if self.PressedCell.idCell != cell.idCell:
			    if self.PressedGrid == 1:
                                self.desactGrid1.append(cell)
                                self.desactGrid2.append(self.PressedCell)
                                #cell.contentCell.img = cell.contentCell.img2
                            	self.PressedCell.actualColorCell = Constants.colorCell
				self.PressedCell.contentCell.img.fill(Constants.colorBackground)
				self.PressedCell.contentCell.borders=False
				cell.contentCell.img.fill(Constants.colorBackground)
                                self.PressedCell.contentCell.img = self.Grid3.Cells[self.PressedCell.contentCell.id].contentCell.img
				#anulamos valor de img2 para indicar k ta ok
                                cell.contentCell.img2 = None
                                self.PressedCell.contentCell.img2 = None
                                self.PressedCell = None

                            #los dos son diferentes..
                        else:

                            #self.changeSecondImage(self.PressedCell)
                            self.PressedCell.actualColorCell = Constants.colorCell
                            #self.changeSecondImage(cell)
                            self.PressedCell = None
			    #self.PressedGrid = 2
			    #self.PressedCell.actualColorCell = Constants.colorPressedCell

                    #celda anterior no apretada
                    else:
                        self.PressedCell = cell
			self.PressedGrid = 2
                        #self.changeSecondImage(cell)
                    	self.PressedCell.actualColorCell = Constants.colorPressedCell


    def changeSecondImage(self,cell):
        tmpImg  = cell.contentCell.img
        cell.contentCell.img = cell.contentCell.img2
        cell.contentCell.img2= tmpImg


    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        #repintamos el grid...
        self.Grid1.OnRender(display_surf)
	self.Grid2.OnRender(display_surf)
        #si la celda se ha apretado, la pintamos ( por los bordes)
        if self.PressedCell != None :
            self.PressedCell.OnRender(display_surf)


    def isOverActivity(self,PointOfMouse):
        return True

    def isGameFinished(self):
        '''finish = True
        for cell in self.Grid1.Cells:
            if cell.contentCell.img2 != None:
                finish = False'''
        if len(self.desactGrid1) == len(self.Grid1.Cells):
            return True
        return False





