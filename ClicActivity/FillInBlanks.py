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
from TextGrid import TextGrid
from Grid import Grid
from styleCell import StyleCell


class FillInBlanks(Activity):

    TextGrid = None
    PrevGrid = None
    targets = {} #Diccionari amb parells (idCell,encert) util quan hi ha optionLists
    options = None
    pressedCell = None
    idPressed = -1 #indica el numero de cell seleccionada respecte al response cell
    previous = False
    
    def Load(self, display_surf ):
        self.setBgColor(display_surf)
        
        try:
            xmlPrevious = self.xmlActivity.getElementsByTagName('prevScreen')[0]
            self.previous = True
            self.PrevGrid = Grid()
            self.PrevGrid.Load(1,1,Constants.ACTIVITY_WIDTH, Constants.ACTIVITY_HEIGHT, Constants.MARGIN_TOP, Constants.MARGIN_LEFT,display_surf)
            self.styleCell = StyleCell(xmlPrevious)
            self.printxmlCellinCell(self.PrevGrid.Cells[0],xmlPrevious, self.styleCell)
        except:
            pass
        
        '''Loading constants for the activity'''
        xmlTextGrid = self.xmlActivity.getElementsByTagName('document')[0]
        
        self.TextGrid = TextGrid(xmlTextGrid,self.mediaInformation,self.pathToMedia)
        
        self.targets = self.TextGrid.Load(display_surf,xmlTextGrid)
        
        opt = xmlTextGrid.getElementsByTagName('optionList')

        if len(opt) > 0:
            self.options = True
        else:
            self.options = False
        
    def OnEvent(self,PointOfMouse):
        if self.previous:
            '''Quan es fa el primer clic es passa a resoldre l'activitat'''
            self.previous = False
        else:
            for i in self.targets.keys():
                print self.TextGrid.textCells[i].type
                if self.TextGrid.textCells[i].type == 'option':
                    encert = self.TextGrid.textCells[i].isOverCell(PointOfMouse[0],PointOfMouse[1])
                    if encert:
                        self.targets[i] = encert
                        print self.targets
                
                else:
                    id = self.TextGrid.textCells[i].isOverCell(PointOfMouse[0],PointOfMouse[1])
                    if id != None:
                        self.pressedCell = self.TextGrid.textCells[i]
                        self.idPressed = id
                        print 'he asignado el pressedcell', self.pressedCell.idCell
                        return
                    else:
                        self.pressedCell = None
                 
    def OnKeyEvent(self,key):
        print 'idpressed', self.idPressed
        if self.pressedCell != None:
            if key == 'backspace' or key == 'delete':
                self.pressedCell.contentCell.writed[self.idPressed] = '_'
                self.pressedCell.contentCell.Cells[self.idPressed].contentCell.letter = '_'
            else:
                self.pressedCell.contentCell.writed[self.idPressed] = key
                self.pressedCell.contentCell.Cells[self.idPressed].contentCell.letter = key
            
            self.idPressed = self.pressedCell.contentCell.printLetter()
                
            

    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))

        if self.previous:
            self.PrevGrid.OnRender(display_surf)
        else:
            '''repintamos el grid'''
            self.TextGrid.OnRender(display_surf)
        

    def isGameFinished(self):
        j = 0
        for i in self.targets.keys():
            if self.TextGrid.textCells[i].type == 'option':
                status = self.targets.values()
                '''Mira si els targets estan correctes o no'''
                if not status[j]:
                    return False
                
            else:   
                if self.TextGrid.textCells[i].contentCell.answer != self.TextGrid.textCells[i].contentCell.writed:                     
                    return False
            j += 1
            
        '''Si no ha retornat abans, tot esta correcte'''
        return True
    
