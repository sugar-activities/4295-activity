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

class DoublePuzzle(Activity):

    Grid1 = None
  
    activity = None
    PressedCell = None
    FinishGame = False


    def Load(self, display_surf ):
        self.setBgColor(display_surf)

        '''Loading xml values'''
        xmlGrid1 = self.xmlActivity.getElementsByTagName('cells')[0]
        self.styleCell = StyleCell(xmlGrid1)
        self.Grid1 = Grid(xmlGrid1)
        self.Grid2 = Grid(xmlGrid1)
        
        
        ''' Calculate Real size'''
        height = self.Grid1.cellHeight * self.Grid1.numRows
        width = self.Grid1.cellWidth * self.Grid1.numCols 
        print 'widht:', width, 'height:', height

        try:
            layout =self.xmlActivity.getElementsByTagName('layout')[0].getAttribute('position')
        except:
            layout = 'AB'
        if layout == 'AB':
            width = width*2 + 5
        else:
            height = height*2 + 5
        
        '''Maximize size'''
        coef = self.calculateCoef(width, height)      
        height = int(height * coef)
        width = int(width * coef)
        print 'maximized -> widht:', width, 'height:', height
        

        '''Loading constants for the activity'''
        
        xActual=Constants.MARGIN_TOP
        yActual=Constants.MARGIN_LEFT
        
        if layout == 'AB':
            width = (width - 5) / 2
            xGrid1 = (Constants.ACTIVITY_WIDTH - width*2 - 10) / 2
            yGrid1 = (Constants.ACTIVITY_HEIGHT - height) / 2
        else:
            height = (height - 5) /2
            xGrid1 = (Constants.ACTIVITY_WIDTH - width) / 2
            yGrid1 = (Constants.ACTIVITY_HEIGHT - height*2 - 10) / 2
        
        xGrid1 = max(xGrid1,xActual)
        yGrid1 = max(yGrid1, yActual)
        
        ''' 1 Imagen de fondo '''
        self.Grid1.imagePath = self.mediaInformation[self.Grid1.imagePath]
        self.Grid1.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid1 ,yGrid1, display_surf,self.pathToMedia)
        
        if layout == 'AB':
            xGrid2 = xGrid1 + width + 10
            yGrid2 = yGrid1
        else:
            xGrid2 = xGrid1
            yGrid2 = yGrid1 + height + 10
        
        xGrid2 = max(xGrid2,xActual)
        yGrid2 = max(yGrid2, yActual)
        
        self.Grid2.imagePath = self.mediaInformation[self.Grid2.imagePath]
        self.Grid2.LoadWithImage(self.Grid1.numRows,self.Grid1.numCols,width,height,xGrid2 ,yGrid2, display_surf,self.pathToMedia)
        
        for cell in self.Grid1.Cells:
            cell.contentCell.img.fill(Constants.colorBackground)
           
        self.Grid2.unsort()
    
        ''' A image 1 le quitamos la imagen'''
    

    def OnEvent(self,PointOfMouse):
        '''
            -----------LOGICS OF THE GAME-----------
            self.PressedCell = celda anterior
            cell = celda actual
        '''
        
        '''Hay una celda apretada.. anteriormente'''
        if self.PressedCell  != None:
            ''' si click en alguna celda izkierda '''
            for cell in self.Grid1.Cells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    ''' si ids son iguales --> cambiamos celdas.. '''
                    if cell.contentCell.id == self.PressedCell.contentCell.id:
                        tmpImg = self.PressedCell.contentCell.img
                        self.PressedCell.contentCell.img = cell.contentCell.img
                        cell.contentCell.img = tmpImg
                        self.PressedCell.contentCell.id = -1
                        self.play_sound(Constants.Sounds.OK)
                    else:
                        self.play_sound(Constants.Sounds.ERROR)

                    ''' desmarcamos pressedCell'''
                    self.PressedCell.actualColorCell = Constants.colorCell
                    self.PressedCell = None
                   
            
            '''si click en derecha.. '''
            for cell in self.Grid2.Cells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    if cell.contentCell.id != -1:
                        ''' cambiamos el pressedCell '''
                        self.PressedCell.actualColorCell = Constants.colorCell
                        self.PressedCell = None
                        self.PressedCell = cell
                        self.PressedCell.actualColorCell = Constants.colorPressedCell
                       

        else:
            self.play_sound(Constants.Sounds.CLICK)
            ''' si click en alguna celda izkierda nothing...--> no ponemos nada '''
             
            
            '''si click en derecha.. '''
            for cell in self.Grid2.Cells:
                if cell.isOverCell(PointOfMouse[0],PointOfMouse[1]):
                    ''' cambiamos el pressedCell a esta celda..-> si no ha sido ya cambiada...'''
                    if cell.contentCell.id != -1:
                    
                        self.PressedCell = cell
                        self.PressedCell.actualColorCell = Constants.colorPressedCell


        
    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))
        '''repintamos el grid...'''
        self.Grid1.OnRender(display_surf)
        self.Grid2.OnRender(display_surf)
        
        '''si la celda anterior  se ha apretado, la repintamos para que se vean los margenes bien'''
        if self.PressedCell != None :
            self.PressedCell.OnRender(display_surf)
       


    def isGameFinished(self):
        for cell in self.Grid2.Cells:
            if cell.contentCell.id != -1:
                return False
        return True

        