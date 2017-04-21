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
import random


from Activity import  Activity
from TextGrid import TextGrid


class Order(Activity):

    TextGrid = None

    '''Diccionari amb parells (idCell,encert)'''
    targets = {}
    options = None
    pressedCell = None
    idPressed = -1 #indica el numero de cell seleccionada respecte al response cell

    def Load(self, display_surf ):
        self.setBgColor(display_surf)

        '''Loading constants for the activity'''
        xmlTextGrid = self.xmlActivity.getElementsByTagName('document')[0]

        self.TextGrid = TextGrid(xmlTextGrid,self.mediaInformation,self.pathToMedia, True)

        self.targets = self.TextGrid.Load(display_surf,xmlTextGrid)

    def OnEvent(self,PointOfMouse):
            nou = -1
            nou2 =-1
            id = -1
            paraula = -1
            for cell in self.TextGrid.textCells2:
                encert = cell.isOverCell(PointOfMouse[0],PointOfMouse[1])

                print cell.contentCell.id, " ",cell.Rect



                if (id != cell.contentCell.id):
                    nou2 += 1

                id = cell.contentCell.id


                if encert:
                    cell.contentCell.border = True
                    self.TextGrid.canvi = True

                    if (self.pressedCell != None):
                        self.TextGrid.changeImages(self.pressedCell, nou2)
                        self.pressedCell = None
                        self.TextGrid.pressedId = None

                    else:
                        self.TextGrid.pressedId = nou2
                        self.pressedCell = nou2
 
                    break



    def OnKeyEvent(self,key):
        print 'idpressed', self.idPressed

    def OnRender(self,display_surf):
        display_surf.blit(self.containerBg,(0,0))

        '''repintamos el grid'''
        self.TextGrid.OnRefresh(display_surf)


    def isGameFinished(self):
        print "iguals???", self.TextGrid.encerts," =?=", self.TextGrid.lenTipus2
        if(self.TextGrid.encerts == self.TextGrid.lenTipus2):
            return True

