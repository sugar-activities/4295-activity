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

class PanelsExplore(Activity):

    Grid1 = None
  
    PressedCell = None

    
    
    def Load(self, display_surf ):
        self.setBgColor(display_surf)

        '''Loading xml values'''
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        xmlGrid2 = self.xmlActivity.getElementsByTagName('cells')[1]
        self.Grid1 = Grid(xmlGrid1)
        self.Grid2 = Grid(xmlGrid2)
        self.Grid3 = Grid(xmlGrid2)

        self.styleCell = StyleCell(xmlGrid1)
        self.styleCell2 = StyleCell(xmlGrid2)
        
        orientation =  self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')

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
              
        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef
        
        
        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT

        xGrid1 = (Constants.ACTIVITY_WIDTH - width) / 2
        yGrid1 = (Constants.ACTIVITY_HEIGHT - height) / 2
        xGrid1 = max(xGrid1,xActual)
        yGrid1 = max(yGrid1,yActual)
            
        
        if orientation == 'AUB' or orientation == 'BUA':
            '''Sumamos el height al tamano'''
            newHeight = self.Grid2.cellHeight * coef
            yGrid1 = (Constants.ACTIVITY_HEIGHT - height - newHeight) / 2
            yGrid1 = max(yGrid1,yActual)
            self.Grid2.Load(1,1,width,newHeight,xGrid1 ,yGrid1 + height, display_surf)
            '''Grid auxiliar...'''
            self.Grid3.Load(self.Grid1.numRows,self.Grid1.numCols,width*self.Grid1.numCols,newHeight,0,0, display_surf)
        else:
            '''Sumamos el width al tamano total'''
            newWidth = self.Grid2.cellWidth * coef
            xGrid1 = (Constants.ACTIVITY_WIDTH - width - newWidth) / 2
            xGrid1 = max(xGrid1,xActual)
            self.Grid2.Load(1,1,newWidth,height,xGrid1 + width ,yGrid1, display_surf)
            '''Grid auxiliar...'''
            self.Grid3.Load(self.Grid1.numRows,self.Grid1.numCols,newWidth,height*self.Grid1.numRows,0,0, display_surf)
        
        self.Grid1.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf)
        
        self.Grid2.Cells[0].contentCell.img2 = self.Grid2.Cells[0].contentCell.img.copy()

        cells = xmlGrid1.getElementsByTagName('cell')
        i = 0
        for cell in cells: 
            self.printxmlCellinCell(self.Grid1.Cells[i], cell, self.styleCell)
            idCell = cell.getAttribute('id')
            if len(idCell)>0:
                self.Grid1.Cells[i].contentCell.id = int(idCell)
            else :
                self.Grid1.Cells[i].contentCell.id = -1
            i = i+1
        cells = xmlGrid2.getElementsByTagName('cell')
        i = 0 
        copia = self.Grid2.Cells[0].contentCell.img.copy()
        for i in range(len(self.Grid1.Cells)):
            copia = self.Grid2.Cells[0].contentCell.img.copy()
            self.Grid3.Cells[i].contentCell.img = copia
            self.printxmlCellinCell(self.Grid3.Cells[i], cells[i],self.styleCell2)
        

    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
            self.PressedCell = celda anterior
            cell = celda actual
        '''
        
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                print cell.contentCell.id
                if cell.contentCell.id != -1:
                    self.Grid2.Cells[0].contentCell.img  = self.Grid3.Cells[cell.contentCell.id].contentCell.img
                else:
                    self.Grid2.Cells[0].contentCell.img = self.Grid2.Cells[0].contentCell.img2

    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)
        self.Grid2.OnRender(display_surf)

    def isGameFinished(self):
        return False

    
   
        
        