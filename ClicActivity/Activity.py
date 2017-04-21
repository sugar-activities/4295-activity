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

# Load GTK
import Constants
import pygame
from styleCell import StyleCell
import os
import sys
class Activity(object):
    xmlActivity = None
    xmlMediaBag = None
    xmlSettings = None
    mediaInformation = dict() #dictionary with the real name of all the media files used in the Activity
    
    containerBg = None
    pathToMedia = None
    
    styleCell = None
    styleCell2 = None
    
    #creates a dictionary <name used in the activity, real name of the file> with all the media used in the Activity 
    def __create_media_dictionary(self, mediaInfo):
        media_dictionary = dict()
        for media in mediaInfo:
            name =  media.getAttribute('name')
            file =  media.getAttribute('file')
            media_dictionary[name] = file
        return media_dictionary
    
    def __init__(self,xmlActivity, xmlMediaBag, xmlSettings):
        #load xml tags 

        self.xmlActivity = xmlActivity

        a, b, c, d = pygame.cursors.load_xbm(Constants.Images.CURSOR, Constants.Images.MASK)

        self.xmlMediaBag = xmlMediaBag
        self.mediaInformation = self.__create_media_dictionary(self.xmlMediaBag.getElementsByTagName('media'))
        self.xmlSettings = xmlSettings

        #load cursor image of OLPC
        a, b, c, d = pygame.cursors.load_xbm(Constants.Images.CURSOR, Constants.Images.MASK)
        pygame.mouse.set_cursor(a, b, c, d)

        '''pygame.mouse.set_cursor(*pygame.cursors.broken_x)'''

        
    def OnEvent(self,PointOfMouse):
        print 'MOTHER CLASS'
    def OnKeyEvent(self,key):
        print 'MOTHER CLASS'   
    def OnLoop(self):
        print 'MOTHER CLASS'
    def OnRender(self,display_surf):
        print 'MOTHER CLASS'
    def setBgColor(self,display_surf):
        self.containerBg = display_surf.copy()
        '''Background Activity'''
        
        try: 
            bgColor = self.xmlActivity.getElementsByTagName('gradient')[0].getAttribute('source')
            r = bgColor[2] + bgColor[3]
            g = bgColor[4] + bgColor[5]
            b = bgColor[6] + bgColor[7]
            r = int(r,16)
            g = int(g,16)
            b = int(b,16)
            self.containerBg.fill((r,g,b))
            print 'color de gradient!'
        except:
            try:
                bgColor = self.xmlActivity.getElementsByTagName('container')[0].getAttribute('bgColor')
                r = bgColor[2] + bgColor[3]
                g = bgColor[4] + bgColor[5]
                b = bgColor[6] + bgColor[7]
                r = int(r,16)
                g = int(g,16)
                b = int(b,16)
                print 'color de container',r,g,b
                self.containerBg.fill((r,g,b))
            except:
                '''No bgColor'''
                self.containerBg.fill(Constants.colorWhite)
        ''' If the activity have image background'''
        
        try:   
            imagePath = self.xmlActivity.getElementsByTagName('image')[0].getAttribute('name')
            imagePath = self.mediaInformation[imagePath]
            image = pygame.image.load(self.pathToMedia+'/'+imagePath).convert_alpha()
            img2 = pygame.transform.scale(image, (pygame.Surface.get_width(self.containerBg), pygame.Surface.get_height(self.containerBg)))
            self.containerBg.blit(img2,(0,0))

        except:
            '''don't have image bg'''
          
  
        

    def Load(self,display_surf):
        print 'MOTHER CLASS'
    def isOverActivity(self,PointOfMouse):
        return True
    def isGameFinished(self):
        print 'MOTHER CLASS'
        
    def getFinishMessage(self):
        '''Recuperamos mensaje de  fin partida'''
        try: 
            cells = self.xmlActivity.getElementsByTagName('messages')[0]
            cells = cells.getElementsByTagName('cell')
            for cell in cells:
                if cell.getAttribute('type')  == 'final':
                    text = cell.getElementsByTagName('p')[0].firstChild.nodeValue
            return text
        except:
            return ""

        def getFinishMessageAudio(self):
            try:
                cells = self.xmlActivity.getElementsByTagName('messages')[0]
                cells = cells.getElementsByTagName('cell')
                for cell in cells:
                    if cell.getAttribute('type')  == 'final':
                        audio = cell.getElementsByTagName('media')
                        if audio.getAttribute('type')=='PLAY_AUDIO':
                            return audio.getAttribute('file')
                return ""
            except:
                return ""


    def getInitMessage(self):
        '''Recuperamos mensaje de  fin partida'''
        try:
            cells = self.xmlActivity.getElementsByTagName('messages')[0]
            cells = cells.getElementsByTagName('cell')
            for cell in cells:
                if cell.getAttribute('type')  == 'initial':
                    text = cell.getElementsByTagName('p')[0].firstChild.nodeValue
                    return text
        except:
            return ""

    def getInitMessageAudio(self):
        try:
            cells = self.xmlActivity.getElementsByTagName('messages')[0]
            cells = cells.getElementsByTagName('cell')
            for cell in cells:
                if cell.getAttribute('type')  == 'initial':
                    audio = cell.getElementsByTagName('media')
                    if audio.getAttribute('type')=='PLAY_AUDIO':
                        return audio.getAttribute('file')
            return ""
        except:
            return ""
    
    def getPreviousMessage(self):
        '''Recuperamos mensaje de  fin partida'''
        try:
            cells = self.xmlActivity.getElementsByTagName('messages')[0]
            cells = cells.getElementsByTagName('cell')
            for cell in cells:
                if cell.getAttribute('type')  == 'previous':
                    text = cell.getElementsByTagName('p')[0].firstChild.nodeValue
                    return text
        except:
            return None
  
    def printxmlCellinCell(self,cell,xmlcell2,style):    

        cell.contentCell.img.fill(style.backgroundColor)

        incremEsq = 0
        incremDreta = 0
        ''' Image in cell'''
        try:
            pathImage =xmlcell2.getAttribute('image')

            overlapping = False
            if (xmlcell2.getAttribute('avoidOverlapping')=="true"):
                overlapping = True

            print overlapping
            try:
                align = xmlcell2.getAttribute('imgAlign')
                alignsplit = align.split(',')
                alignX = alignsplit[0]
                alignY = alignsplit[1]
            except:
                alignX = 0
                alignY = 0

            #audio = xmlcell2.getElementByName('media')

            #if audio != None and audio.getAttribute('type') == 'PLAY_AUDIO':
            #    audioPath = audio.getAttribute('file')
            #    cell.contentCell.audio = audioPath
            
            pathImage = self.mediaInformation[pathImage]
            imagePath = self.pathToMedia+'/'+pathImage
    
            newImg = pygame.image.load(imagePath).convert_alpha()
    
            cellWidth = cell.contentCell.img.get_width()
            cellHeight = cell.contentCell.img.get_height()

            aux = newImg.get_size()
            widthImg, heightImg = aux

            newWidth = 0
            newHeight = 0


            print overlapping


            print cell.contentCell.img.get_width(), ",",cell.contentCell.img.get_height()
            transX = 1
            transY = 1
            if (cell.contentCell.img.get_width()<widthImg):
                transX = widthImg/cell.contentCell.img.get_width()
            if (cell.contentCell.img.get_height()<heightImg):
                transY = heightImg/cell.contentCell.img.get_height()


            if alignX == 0:
                newImg = pygame.transform.scale(newImg, (cell.contentCell.img.get_width(),  cell.contentCell.img.get_height()))

            if alignX == "middle":
                newWidth = (cellWidth - widthImg)/2
            elif alignX == "left":
                newWidth = 0
                widthImg = widthImg/transY
                incremEsq = widthImg
                if(heightImg<cell.contentCell.img.get_height()):
                    newImg = pygame.transform.scale(newImg, (widthImg,  heightImg))
                else:
                    newImg = pygame.transform.scale(newImg, (widthImg, cell.contentCell.img.get_height()))
            elif alignX == "right":
                widthImg = widthImg/transY
                newWidth = cellWidth - widthImg
                incremDreta = widthImg
                if(heightImg<cell.contentCell.img.get_height()):
                    newImg = pygame.transform.scale(newImg, (widthImg,  heightImg))
                else:
                    newImg = pygame.transform.scale(newImg, (widthImg,  cell.contentCell.img.get_height()))

            if alignY == "middle":
                if(heightImg>cell.contentCell.img.get_height()):
                    newHeight = 0
                else:
                    newHeight = (cellHeight - heightImg)/2
                #newHeight = 0
            elif alignY == "top":
                newHeight = 0
            elif alignY == "bottom":
                newHeight == cellHeight - heightImg
                #newHeight = 0

            cell.contentCell.img.blit(newImg,(newWidth,newHeight))
            #tmpSurf = surface.Surface()
        except:
            pass
        '''Text in cell'''
        try:
            elementP = xmlcell2.getElementsByTagName('p')
            texto = ''
            for element in elementP:
                texto = texto + element.firstChild.nodeValue + '\n'
            print texto
            font = pygame.font.Font(None, style.fontSize)
            
            '''Blit text'''
            print "overlapping= ", overlapping
            if (not overlapping):
                incremEsq = 0
                incremDreta = 0

            self.renderText(texto,cell.Rect,font,cell.contentCell.img,cell.actualColorCell, incremEsq, incremDreta)
    
            ''' Border in cell'''
            cell.contentCell.border = style.hasBorder
        except:
            pass
        

        try:
            hola = xmlcell2.getElementsByTagName("media")[0].getAttribute("file")
            if "RUN_CLIC_PACKAGE" == xmlcell2.getElementsByTagName("media")[0].getAttribute("type"):
                cell.redirect = hola
        except:
            pass

    def printLetterinCell(self,cell,xmlcell,letterColour=Constants.colorBlack,backColour=Constants.colorWhite):    
       
        #styleCell  = StyleCell(xmlcell)
        
        cell.contentCell.img.fill(backColour)
    
        '''Print letter in cell'''
        try:
            texto = cell.contentCell.letter
            font = pygame.font.Font(None, self.styleCell.fontSize)
            #text = font.render(texto, True, styleCell.foregroundColor)

            '''Blit text'''
            self.renderText(texto,cell.Rect,font,cell.contentCell.img,letterColour)
        except:
            pass
        '''Border in cell'''
        cell.contentCell.border = self.styleCell.hasBorder
        
    def calculateCoef(self,width,height):
        coefWidth =  Constants.ACTIVITY_WIDTH /width
        coefHeight = Constants.ACTIVITY_HEIGHT / height

        if coefWidth < coefHeight:
            coef = coefWidth
        else:
            coef = coefHeight
        
        return coef
    
    
    def renderText(self,text,rect,font,surf,colour,incremEsquerra = 0, incremDreta = 0):
        
        final_lines = []
        
        requested_lines = text.splitlines()
    
        # Create a series of lines that will fit on the provided
        # rectangle.
    
        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width-4-incremEsquerra - incremDreta:
                words = requested_line.split(' ')
                #si alguna paraula es massa llarga, es trunca
                for j in range(len(words)):
                    word = words[j]
                    if font.size(word)[0] > rect.width-4 -incremEsquerra - incremDreta:
                        numLetters = ((rect.width - 4) / font.size(word[0])[0]) - 1
                        numLines = len(word) // numLetters #calcula quantes linies ocupa
                        if (len(word) % numLetters) != 0:
                            numLines += 1
                        
                        wordCopy = word
                        word = ""
                        for n in range(numLines):
                            for i in range(n*numLetters,(n+1)*numLetters):
                                word = word + wordCopy[i]
                                if i == len(wordCopy)-1: #acaba abans si la paraula no ocupa tota la linea
                                    break
                            word = word + ' '

                        words[j] = word
                
                # Start a new line
                accumulated_line = ""
                for word in words:
                    splitwords = word.split(' ')
                    for splitword in splitwords:
                        test_line = accumulated_line + splitword + " "
                        # Build the line while the words fit.    
                        if font.size(test_line)[0] < rect.width-4 -incremEsquerra - incremDreta:
                            accumulated_line = test_line 
                        else: 
                            final_lines.append(accumulated_line) 
                            accumulated_line = splitword + " " 
                final_lines.append(accumulated_line)
            else: 
                final_lines.append(requested_line) 
    
        # Let's try to write the text out on the surface.
        total_height = len(final_lines) * font.size(final_lines[0])[1]
        accumulated_height = (rect.height - total_height) / 2
        for line in final_lines: 
            if accumulated_height + font.size(line)[1] >= rect.height:
                raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
            if line != "":
                tempsurface = font.render(line, 1, colour)
                surf.blit(tempsurface, ((rect.width + incremEsquerra - (tempsurface.get_width())-incremDreta) / 2, accumulated_height))
                
            accumulated_height += font.size(line)[1] #font.size returns (width,height)

    def play_sound(self,filename):
        #pygame.mixer.pre_init(44100,-16,2, 1024)

        #Al OLPC no funciona 
        if 0==1:#pygame.mixer.get_init():
            try:
                print "hola"
                #music = os.path.join('data','clics','conill', '4.wav')
                #print music
                #pygame.mixer.music.load("/home/roger/NetBeansProjects/sugarhg/src/sounds/action_ok.mp3")
                pygame.mixer.music.load(filename)
                #sound = pygame.mixer.Sound("/home/roger/Escriptori/monkeystomp/data/jump.wav")
                pygame.mixer.music.play()
            except:
                print "No se pudo cargar el sonido:", fullname
                raise SystemExit, message
            
