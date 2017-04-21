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
import pygame.font
import pygame.locals
import os.path

from Activity import  Activity
from Grid import Grid
from styleCell import StyleCell

class IdentifyPanels(Activity):

    Grid1 = None


    def Load(self, display_surf ):
        self.setBgColor(display_surf)

        '''Loading xml values'''
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        self.Grid1 = Grid(xmlGrid1)
        try:
            xmlGrid2 = self.xmlActivity.getElementsByTagName('cells')[1]
            self.Grid2 = Grid(xmlGrid2)
            self.styleCell2 = StyleCell(xmlGrid2)
        except:
            self.Grid2 = Grid()
            '''only 1 Grid'''
        
        self.styleCell = StyleCell(xmlGrid1)


        ''' Calculate Real size'''

        width = self.Grid1.cellWidth * self.Grid1.numCols
        height = self.Grid1.cellHeight * self.Grid1.numRows


        ''' Calculamos porcentaje...'''

        '''Maximize size'''
        coef = self.calculateCoef(width, height)

        height = self.Grid1.cellHeight * self.Grid1.numRows * coef
        width = self.Grid1.cellWidth * self.Grid1.numCols * coef

        '''Loading constants for the activity'''

        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT

        xGrid = (Constants.ACTIVITY_WIDTH - width) / 2
        yGrid = (Constants.ACTIVITY_HEIGHT - height) / 2

        xGrid = max(xGrid,xActual)
        yGrid = max(yGrid,yActual)

        '''Cargamos grupo de celdas comunes...'''

        ''' 1 Imagen por cada celda ( tipo texto)'''
        self.Grid1.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid ,yGrid, display_surf)

        cells = xmlGrid1.getElementsByTagName('cell')

        i = 0
        for cell in cells:
            self.printxmlCellinCell(self.Grid1.Cells[i], cell, self.styleCell)

            id  = int(cell.getAttribute('id') )
            self.Grid1.Cells[i].contentCell.id = id
            i = i+1
        try:
            '''if cells 2 not exists, only create an empty Grid'''
            self.Grid2.Load(self.Grid1.numRows,self.Grid1.numCols,width,height,xActual ,yActual, display_surf)




            cells = xmlGrid2.getElementsByTagName('cell')
            i = 0
            for cell in cells:
                self.printxmlCellinCell(self.Grid2.Cells[i], cell, self.styleCell2)

                i = i+1
        except:
            pass



    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
        '''
        for cell in self.Grid1.Cells:
            if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                if cell.contentCell.id != 0:
                    print cell.contentCell.id
                    if cell.contentCell.id == 1:
                        cell.contentCell.img = self.Grid2.Cells[cell.idCell].contentCell.img
                        cell.contentCell.id = -1
                        self.play_sound(Constants.Sounds.OK)
                else:
                        self.play_sound(Constants.Sounds.ERROR)

                        '''pygame.mixer.music.play()'''




    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)


    def isGameFinished(self):
        for cell in self.Grid1.Cells:
            if cell.contentCell.id == 1:
                return False
        return True

        