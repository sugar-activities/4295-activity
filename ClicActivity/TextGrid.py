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
from OptionList import *
from Response import *
from TextField import *
from Constants import *
import os
import pygame
from pygame import surface
from pygame.locals import *
import random


class TextGrid(object):
    
    Rect = None
    gridSurf = None
    
    textCells = []

    textCells2 = []
    bloc = []
    tipus = []
    canvi = False
    id = 0
    pressedId = -1
    lenTipus2 = 0
    numeracio = []
    numCells = 0
    ids = []
    isOrder = None
    encerts = 0

    backgroundColor = None
    font = None
    
    idCell = 0 #index que indica el id del cell que s'afegeix
    xActCell = 0
    yActCell = 0
    numCells = 0
    mediaBag = None
    pathToMedia = None
    
    X_NEW_LINE = Constants.MARGIN_LEFT + 10
    OFFSET_TOP_NEW_LINE = 0
    
    '''Inicialitza els valors generics de configuracio del textGrid
        com ara el color de fons i el tipus de lletra usada
        @xmlTextGrid es la part del xml corresponent al document de l'activitat
    '''
    def __init__(self,xmlTextGrid,mediaBag = None, pathToMedia = None, isOrd= None):
        style = xmlTextGrid.getElementsByTagName('style')[0]
        try:
            bgColor = style.getAttribute('background')
            r = bgColor[2] + bgColor[3]
            g = bgColor[4] + bgColor[5]
            b = bgColor[6] + bgColor[7]
            r = int(r, 16)
            g = int(g, 16)
            b = int(b, 16)
            self.backgroundColor = (r, g, b)
        except:
            self.backgroundColor = Constants.colorWhite
        
        try:
            family = style.getAttribute('family')
            size = style.getAttribute('size')
            if size < Constants.minFontSize:
                size = Constants.minFontSize
            bold = style.getAttribute('bold')
            if bold == 'true':
                bold = True
            else:
                bold = False
            italic = style.getAttribute('italic')
            if italic == 'true':
                italic = True
            else:
                italic = False
            self.font = pygame.font.SysFont(family,size,bold,italic)
        except:
            self.font = pygame.font.SysFont('Arial', Constants.minFontSize)

        self.mediaBag = mediaBag
        self.pathToMedia = pathToMedia
        self.OFFSET_TOP_NEW_LINE = self.font.size('OFFSET')[1] + 10
        self.textCells = []
        self.encerts = 0
        self.textCells2 = []
        self.bloc = []
        self.ids = []
        self.tipus = []
        self.id = 0
        self.isOrder = isOrd
        
        
    '''Carrega el text del document. Cada paraula es un element del grid.
        Diferencia els diferents tipus de target per tractar-los com cal.
        @display_surf es la superficie de l'activitat on es pintara el grid amb el seu contingut
        @xmlDocument es la part del xml corresponent al document de l'activitat
    '''

    def Load(self, display_surf, xmlDocument, flag=''):      
        self.xActCell = Constants.MARGIN_LEFT + 10
        self.yActCell = Constants.MARGIN_TOP + 10
        self.idCell = 0
        
        solTargets = {}
        
        '''Carrega la superficie on es mostrara el text'''
        self.gridSurf = pygame.Surface((Constants.ACTIVITY_WIDTH, Constants.ACTIVITY_HEIGHT)).convert()
        self.Rect = pygame.Rect(Constants.MARGIN_LEFT, Constants.MARGIN_TOP, Constants.ACTIVITY_WIDTH, Constants.ACTIVITY_HEIGHT)
        
        '''Carrega i mostra el contingut'''
        
        '''Primer agafa els paragrafs (elements <p>)'''
        allP = xmlDocument.getElementsByTagName('p')
         
        '''Mostra el text, per paragrafs, diferenciant els tipus d'elements'''
        for p in allP:
            if flag == 'complete':
                self.Add(display_surf, 'textField', p)
                
            else:
                #nou = p.childNodes
                #print p.childNodes
                nou = p.childNodes
                text = []
                if(self.isOrder!=None):
                    for child in nou:
                        if child.nodeName == 'text':
                            text.append(child)
                else:
                    #Tambe agafar els target.getElementsByName('cell') i restar-li a text
                    text = p.getElementsByTagName('text')
                target = p.getElementsByTagName('target')
                cells = p.getElementsByTagName('cell')
                self.numCells = len(cells)
                
                '''Agafo els fills del node per saber l'ordre en que apareix cada fragment'''
                childs = p.childNodes
                itext = 0 #index per recorrer els nodes text
                itarget = 0 #index per recorrer els nodes target
                iCell = 0 #index per recorrer els nodes cell
                for child in childs:
                    if child.nodeName == 'text':
                        self.Add(display_surf, 'text', text[itext])
                        itext += 1
                    elif child.nodeName == 'target':
                        solTargets[self.idCell] = False
                        if(self.isOrder != None):
                            self.Add(display_surf,'text2',target[itarget])
                        elif flag == 'identify':
                            self.Add(display_surf, 'text', target[itarget])
                        else:
                            self.Add(display_surf, 'target', target[itarget])
                            itext += 1 #incrementem tambe l'index del text per saltar el text intern del target
                        itarget += 1
                    elif child.nodeName == 'cell':
                        self.Add(display_surf,'cell',cells[iCell])
                        iCell += 1
                if(self.isOrder!=None):
                    self.Add(display_surf,'text2','\n')
                if len(cells) > 0:
                    h = int(cells[0].getAttribute('height')) + 10
                    self.yActCell += h
                else:
                    self.xActCell = self.X_NEW_LINE
                    self.yActCell += self.OFFSET_TOP_NEW_LINE
                    
        if(self.isOrder!=None):
            self.unsort()
        return solTargets
        
    '''Funcio que afegeix al grid elements, creant-los de forma diferent segons el tipus
        @display_surf es la superficie de l'activitat on es pintara el grid amb el seu contingut
        @type es el tipus d'element. Pot ser text simple o qualsevol tipus de target
        @xmlObject es la part del xml corresponent al objecte que s'afegeix
    '''
    def Add(self, display_surf, type, xmlObject):

        if type == 'text':
            line = xmlObject.firstChild.data

            words = line.split(' ')

            self.bloc.append(words)
            self.tipus.append('text')

            for word in words:
                tmpSurf = self.font.render(word, 1, Constants.colorBlack)
                surf = pygame.Surface((self.font.size(word))).convert()
                surf.fill(self.backgroundColor)
                if (self.xActCell + self.font.size(word)[0]) > self.Rect.width - 10:
                    self.xActCell = self.X_NEW_LINE
                    self.yActCell += self.OFFSET_TOP_NEW_LINE
                    
                surf.blit(tmpSurf, (0, 0))
                
                rect = pygame.Rect((self.xActCell, self.yActCell), (surf.get_size()))
                textCell = TextCell(rect, self.idCell, 'text')
                
                contentCell = ContentCell()
                contentCell.img = surf.copy()
                if(self.isOrder!=None):
                    contentCell.id = None
                else:
                    contentCell.id = self.idCell
                    self.idCell = self.idCell + 1
                textCell.contentCell = contentCell
                
                self.textCells.append(textCell)
                
                #self.idCell = self.idCell + 1
                self.xActCell += rect.width + 5
                if self.xActCell >= self.Rect.width - 10:
                    self.xActCell = self.X_NEW_LINE
                    self.yActCell += self.OFFSET_TOP_NEW_LINE
        
        elif type == 'text2':

            if (xmlObject == '\n'):
                self.bloc.append('\n')
                self.tipus.append('return')


            else:
                line = xmlObject.firstChild.data

                try:
                    text = xmlObject.getElementsByTagName("text")[0].firstChild.data
                    line = text
                except:
                    pass

                words = line.split(' ')

                self.bloc.append(words)
                self.numeracio.append(self.numCells)
                self.tipus.append('text2')
                self.lenTipus2 += 1

                for word in words:
                    tmpSurf = self.font.render(word,1,Constants.colorLila)
                    surf = pygame.Surface((self.font.size(word))).convert()
                    surf.fill(Constants.colorBlack)
                    if (self.xActCell + self.font.size(word)[0]) > self.Rect.width - 10:
                        self.xActCell = self.X_NEW_LINE
                        self.yActCell += self.OFFSET_TOP_NEW_LINE

                    surf.blit(tmpSurf,(0,0))

                    rect = pygame.Rect((self.xActCell,self.yActCell),(surf.get_size()))
                    textCell = TextCell(rect,self.idCell,'text')

                    contentCell = ContentCell()
                    contentCell.img = surf.copy()
                    contentCell.id = self.id
                    textCell.contentCell = contentCell

                    textCell.contentCell.id = self.id

                    self.textCells2.append(textCell)

                    self.numCells += 1

                    #self.idCell = self.idCell + 1
                    self.xActCell += rect.width + 5
                    if self.xActCell >= self.Rect.width - 10:
                        self.xActCell = self.X_NEW_LINE
                        self.yActCell += self.OFFSET_TOP_NEW_LINE

                self.ids.append(self.id)

                self.id += 1


        elif type == 'cell':
            try:
                width = int(xmlObject.getAttribute('width'))
                height = int(xmlObject.getAttribute('height'))
                image = xmlObject.getAttribute('image')
                image = self.mediaBag[image]
                fullPath = self.pathToMedia + '/' + image
                
                cellRect = pygame.Rect(self.xActCell, self.yActCell, width, height)
                cell = Cell(cellRect, display_surf, self.idCell, True)
                
                contentCell = ContentCell()
                contentCell.id = self.idCell
                contentCell.img = pygame.Surface((width, height))
                cellImg = pygame.image.load(fullPath).convert_alpha()
                cellImg = pygame.transform.scale(cellImg, (width, height))
                
                contentCell.img.blit(cellImg, (0, 0))
                cell.contentCell = contentCell
                
                self.textCells.append(cell)
                self.idCell += 1
                self.xActCell += width + int((Constants.ACTIVITY_WIDTH - (self.numCells*width)) / self.numCells)
            except:
                pass
        
        elif type == 'textField':
            textField = TextField(xmlObject,self.font,self.backgroundColor)
            textField.Load(self.xActCell,self.yActCell,display_surf)
            textCell = TextCell(None,self.idCell,'textField')
            textCell.contentCell = textField
            self.textCells.append(textCell)
            self.idCell += 1
            self.xActCell = self.X_NEW_LINE
            self.yActCell += textField.textCell.Rect.height + self.OFFSET_TOP_NEW_LINE
        
        elif type == 'target':
            try:
                '''Si el target es de tipus optionList'''
                xmlObject.getElementsByTagName('optionList')
                
                if (self.xActCell + Constants.widthOpt + self.font.size('V')[0]) > self.Rect.width:
                    self.xActCell = self.X_NEW_LINE
                    self.yActCell += self.OFFSET_TOP_NEW_LINE
                    
                option = OptionList(xmlObject, self.font)
                option.Load(self.xActCell, self.yActCell, display_surf)
                
                optionCell = TextCell(None, self.idCell, 'option')
                optionCell.contentCell = option
                
                self.textCells.append(optionCell)

                self.idCell = self.idCell + 1
                self.xActCell += option.textCell.Rect.width + option.openCell.Rect.width + 5
                if self.xActCell >= self.Rect.width:
                    self.xActCell = self.X_NEW_LINE
                    self.yActCell += self.OFFSET_TOP_NEW_LINE
                return
            except:
                print 'no es optionList'
            
            try:
                '''Si el target es de tipus response'''
                xmlObject.getElementsByTagName('response')
                print 'es de tipus response'
                resp = Response(xmlObject, self.font, self.backgroundColor)
                resp.Load(self.xActCell, self.yActCell, display_surf)
                
                respCell = TextCell(None, self.idCell, 'response')
                respCell.contentCell = resp
                
                self.textCells.append(respCell)
                
                self.idCell += 1
                self.xActCell += respCell.contentCell.totalWidth + 5
                if self.xActCell >= self.Rect.width:
                    self.xActCell = self.X_NEW_LINE
                    self.yActCell += self.OFFSET_TOP_NEW_LINE
                return
            except:
                print 'no es de tipus response'
            
                
            
    def OnRender(self,display_surf):
        '''Pinta la superficie del text grid'''
        self.gridSurf.fill(self.backgroundColor)
        display_surf.blit(self.gridSurf, (Constants.MARGIN_LEFT, Constants.MARGIN_TOP))
        pygame.draw.rect(display_surf, Constants.colorBlack, self.Rect, Constants.DEFAULT_BORDER_SIZE)
        
        '''Pinta les cells que contenen el text'''
        for i in range(len(self.textCells)-1, -1, -1):
            self.textCells[i].OnRender(display_surf)

    def OnRefresh(self,display_surf):
        '''Pinta la superficie del text grid'''
        self.gridSurf.fill(self.backgroundColor)
        display_surf.blit(self.gridSurf,(Constants.MARGIN_LEFT,Constants.MARGIN_TOP))
        pygame.draw.rect(display_surf,Constants.colorBlack,self.Rect,Constants.DEFAULT_BORDER_SIZE)

        self.xActCell = Constants.MARGIN_LEFT + 10
        self.yActCell = Constants.MARGIN_TOP + 10
        conta = -1
        numCells = 0
        conta2 = -1
        numAux = 0
        self.encerts = 0
        for wordGroup in self.bloc:
            conta +=1
            if(self.tipus[conta]=="return"):
                self.xActCell = self.X_NEW_LINE
                self.yActCell += self.OFFSET_TOP_NEW_LINE/2
            else:
                if (self.tipus[conta]=="text2"):
                        conta2 += 1
                        if self.pressedId == conta2:
                            color = Constants.colorLila
                        elif conta2 == self.textCells2[numAux].contentCell.id:
                            color = Constants.colorGreen
                            self.encerts += 1
                        else:
                            color = Constants.colorRed
                        numAux  += len(wordGroup)
                else:
                        color = Constants.colorBlack
                for word in wordGroup:

                        tmpSurf = self.font.render(word,1,color)
                        surf = pygame.Surface((self.font.size(word))).convert()
                        surf.fill(self.backgroundColor)
                        if (self.xActCell + self.font.size(word)[0]) > self.Rect.width - 10:
                            self.xActCell = self.X_NEW_LINE
                            self.yActCell += self.OFFSET_TOP_NEW_LINE

                        display_surf.blit(tmpSurf,(self.xActCell,self.yActCell))

                        rect = pygame.Rect((self.xActCell,self.yActCell),(surf.get_size()))
                        textCell = TextCell(rect,self.idCell,'text')

                        if (self.tipus[conta]=="text2"):
                            self.textCells2[numCells].Rect = rect
                            numCells += 1

                        self.xActCell = self.xActCell + rect.width + 5
                        if self.xActCell >= self.Rect.width:
                            self.xActCell = self.X_NEW_LINE
                            self.yActCell += self.OFFSET_TOP_NEW_LINE



    def changeImages(self,idCell1, idCell2):

        ''' Change the 2 cell images from a Grid '''

        if idCell1 != idCell2:

            if idCell1 > idCell2:
                idAux = idCell1
                idCell1 = idCell2
                idCell2 = idAux


            aux = []
            cont = 0
            contTotal = 0
            trobat = -1
            # A tipus hi ha el tipus de blocs ordenats
            for tip in self.tipus:
                # Si el bloc es de tipus resposta
                if tip == "text2":
                    # Si trobem l'id de la cela a intercanviar
                    if cont == idCell1:
                        aux = self.bloc[contTotal]
                        trobat = contTotal
                        trobat2 = cont
                    # Si trobem l'id de la segona cela a intercanviar
                    elif cont == idCell2:
                        # Canviem el contingut dels blocs
                        self.bloc[trobat] = self.bloc[contTotal]
                        # Posem a textCells2[trobat2] l'id de la cela actual
                        self.bloc[contTotal] = aux

                    cont += 1
                contTotal += 1

            i = 0
            x = 0
            x2 = 0
            while (x < len(self.bloc)):
                if self.tipus[x]=="text2":
                    for cell in self.bloc[x]:
                        if x2 == idCell1:
                            self.textCells2[i].contentCell.id = self.ids[idCell2]
                        elif x2 == idCell2:
                            self.textCells2[i].contentCell.id = self.ids[idCell1]
                        else:
                            self.textCells2[i].contentCell.id = self.ids[x2]
                        i += 1
                    x2 +=1
                x +=1


            aux = self.ids[idCell1]
            self.ids[idCell1] = self.ids[idCell2]
            self.ids[idCell2] = aux

    def unsort(self):
        i = 0
        ''' We do 50 times!!! maby only 10 loops necessary'''
        while (i< 40):
            self.changeImages(random.randint(0, self.lenTipus2-1),random.randint(0, self.lenTipus2-1))
            i+= 1