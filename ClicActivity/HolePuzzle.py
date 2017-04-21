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

class HolePuzzle(Activity):

    Grid1 = None
  
    PressedCell = None
    FinishGame = False

     
    def Load(self, display_surf ):
        self.setBgColor(display_surf)

        '''Loading xml values'''
        xmlGrid = self.xmlActivity.getElementsByTagName('cells')[0]
        self.styleCell = StyleCell(xmlGrid)
        
        self.Grid1 = Grid(xmlGrid)
        self.Grid2 = Grid(xmlGrid)
         

        ''' Calculate Real size'''
        height = self.Grid1.cellHeight * self.Grid1.numRows
        width = self.Grid1.cellWidth * self.Grid1.numCols
        

        '''Sumamos el width al tamano total'''
        ''' 30 -> Margin over Grids'''
        width = width + self.Grid1.cellWidth + 30
        
        ''' Calculamos porcentaje...'''
        
        '''Maximize size'''
        
        coef = self.calculateCoef(width, height)
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef
        
        
        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT
        
        
        '''calculamos espacio para 1 celda mas...'''

       
        if self.Grid1.imagePath!=None:
            ''' 1 Imagen de fondo '''
            width= Constants.ACTIVITY_WIDTH 
            height =Constants.ACTIVITY_HEIGHT
            
            self.Grid1.imagePath = self.mediaInformation[self.Grid1.imagePath]
            self.Grid1.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf,self.pathToMedia)
            
           
        else:
            ''' 1 Imagen por cada celda ( tipo texto)''' 
            xGrid = (Constants.ACTIVITY_WIDTH - width) / 2
            xGrid = max(xGrid,xActual)
            yGrid = (Constants.ACTIVITY_HEIGHT - height) / 2
            yGrid = max(yGrid,yActual)

            self.Grid1.Load(self.numRows,self.numCols,width,height,xGrid ,yGrid, display_surf)
            cells = xmlGrid.getElementsByTagName('cell')
            i = 0
           
            for cell in cells: 
                '''Recuperamos el texto de la celda y lo  bliteamos en imagen actual de celda.. ''' 
                
                self.printxmlCellinCell(self.Grid1.Cells[i], cell, self.styleCell)
                i = i+1
        
        self.Grid1.unsort()
        
        '''Load second Grid only with 1 cell..'''
        print self.Grid1.cellHeight , self.Grid1.cellWidth
        self.Grid2.Load(1,1,self.Grid1.cellHeight,self.Grid1.cellWidth,xActual+  width + 20,(height/2)-(self.Grid1.cellWidth/2), display_surf)
        self.Grid2.Cells[0].contentCell.img = self.Grid1.Cells[0].contentCell.img.copy()
        self.Grid1.Cells[0].contentCell.img.fill(Constants.colorBackground)
        self.Grid1.Cells[0].contentCell.id = -1

    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
            self.PressedCell = celda anterior
            cell = celda actual
        '''
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                print cell.idCell
                print len(self.Grid1.Cells)
                '''celda anterior apretada ''' 
                if cell.contentCell.id != -1:
                    idCelda = cell.idCell
                    try:
                        ''' celda gris esta a al izkierda'''
                        if self.Grid1.Cells[idCelda -1].contentCell.id == -1:
                            print 'idcelda =',idCelda,'mod=',((idCelda)% self.Grid1.numCols)
                            if ((idCelda-1)% self.Grid1.numCols) !=(self.Grid1.numCols-1) :
                                self.Grid1.changeImages(cell.idCell,self.Grid1.Cells[idCelda -1].idCell )
                        
                        elif self.Grid1.Cells[int(idCelda - self.Grid1.numCols)].contentCell.id == -1:
                            ''' celda gris esta arriba '''
                            print 'idcelda',idCelda
                            print 'calculo=',(idCelda - self.Grid1.numCols)
                            self.Grid1.changeImages(cell.idCell,self.Grid1.Cells[int(idCelda - self.Grid1.numCols)].idCell )
                        
                        elif self.Grid1.Cells[idCelda +1].contentCell.id == -1:
                                ''' celda gris esta a la derecha'''
                                '''evitem laterals'''
                                if ((idCelda+1)% self.Grid1.numCols) !=0:
                                    self.Grid1.changeImages(cell.idCell,self.Grid1.Cells[idCelda + 1].idCell )

                        elif self.Grid1.Cells[int(idCelda + self.Grid1.numCols)].contentCell.id == -1:
                            ''' celda gris esta abajo '''
                            print 'calculo=',(idCelda + self.Grid1.numCols)
                            self.Grid1.changeImages(cell.idCell,self.Grid1.Cells[int(idCelda + self.Grid1.numCols)].idCell )
                        
                    except:
                        pass
                    

    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)
        self.Grid2.OnRender(display_surf)
  
    def isGameFinished(self):
        for cell in self.Grid1.Cells:
            if cell.idCell != cell.contentCell.id:
                return False
        return True

        