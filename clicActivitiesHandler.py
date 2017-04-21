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
import pygame
import xml.dom.minidom
from pygame.locals import *
from ClicActivity.Point import Point
from ClicActivity.ExchangePuzzle  import ExchangePuzzle
from ClicActivity.MemoryGame  import MemoryGame
from ClicActivity.DoublePuzzle import DoublePuzzle 
from ClicActivity.InformationScreen import InformationScreen 
from ClicActivity.HolePuzzle import HolePuzzle
from ClicActivity.IdentifyPanels import IdentifyPanels
from ClicActivity.FinishActivity import FinishActivity
from ClicActivity.PanelsExplore import PanelsExplore
from ClicActivity.GeneralDialog import GeneralDialog
from ClicActivity.SimpleAssociation import SimpleAssociation
from ClicActivity.ComplexAssociation import ComplexAssociation
from ClicActivity.WordSearch import WordSearch
from ClicActivity.CrossWord import CrossWord
from ClicActivity.FillInBlanks import FillInBlanks
from ClicActivity.Complete import Complete
from ClicActivity.Order import Order
from ClicActivity.Identify import Identify
from ClicActivity.TextComplete import TextComplete
from ClicActivity import Constants


class ClicActivities:
    display = None
    path_to_clic = None
    mediaBagTag = None
    settingsTag = None
    
    def __init__(self, path, mediaTag, settingsTag, clic_name):
        print 'clicname = ',clic_name
        print 'path = ',path
        self.path_to_clic = path
        self.mediaBagTag = mediaTag
        self.settingsTag = settingsTag
        

        
    #starts the activity declared in activityTag
    def start_activity(self, activityTag, pygameScreen, first = False, last = False):

        self.screen = pygameScreen
        self.dialog = GeneralDialog(first, last)
        self.dialog.renderDialog(self.screen)
        
        '''HardCodded:creating the subsurface for ACTIVITIES'''
        weidth = Constants.MAX_WIDTH- Constants.MARGIN_RIGHT
        height = Constants.MAX_HEIGHT-(Constants.MARGIN_BOTTOM-15)

        rectborder= Rect(0,0,weidth,height)
        self.activity_surf = self.screen.subsurface(rectborder)
       
        '''por si acaso no hay actividad'''
        
       
       
        if self.canExecuteActivity(activityTag):                
            self.activityInUse = self.executeActivity(activityTag, self.mediaBagTag, self.settingsTag)
            self.activityInUse.pathToMedia = self.path_to_clic
            self.activityInUse.Load(self.activity_surf)
            '''Cogemos previous message si existe'''
            self.prevMess = self.activityInUse.getPreviousMessage()
            if self.prevMess != None:
                self.dialog.printMessage(self.screen,self.prevMess)
            else:
                self.dialog.printMessage(self.screen,self.activityInUse.getInitMessage())
            #audio = self.activityInUse.getInitMessageAudio()
            #if audio!="":
            #    self.activityInUse.play_sound(audio)
            #aqui s'hauria de reproduir l'audio del principi
        
        else: 
            ''' this case never ocurss.. teorically... heheheh'''
            self.activityInUse = FinishActivity(activityTag)
            
            self.dialog.printMessage(self.screen,'activitat no disponible' )
        
        '''Initial rendering'''
        self.activityInUse.OnRender( self.activity_surf)
        pygame.display.flip()
	
       



    def update_activity(self, evento,isFirstActivity=False,isLastActivity=False):
        event = False

        result = None

        if evento.type == pygame.MOUSEBUTTONDOWN:
            event = True
            pointMouse = Point(pygame.mouse.get_pos())
            
            
            #Retornem -2 tractant la seguent activitat
            if self.dialog.isOverNextButton(pointMouse):                
                return -2

	        #Retornem -3 tractant l'activitat anterior
            if self.dialog.isOverPreviousButton(pointMouse):
                return -3

            #Retornem -4 tractant l'activitat primera
            if self.dialog.isOverFirstButton(pointMouse):
                return -4

            #Retornem -5 tractant l'activitat ultima
            if self.dialog.isOverLastButton(pointMouse):
                return -5

            #Retornem -6 tractant el reinici de l'activitat
            if self.dialog.isOverRetryButton(pointMouse):
                return -6

            #Retornem -1 perque es tracti al clic_player per tornar a comensar
            if self.dialog.isOverChangeClicButton(pointMouse):
                return -1
            
            if self.prevMess != None and self.dialog.isOverActivity(pointMouse):
                self.prevMess = None
                self.dialog.printMessage(self.screen,self.activityInUse.getInitMessage())
                
            if self.dialog.isOverActivity(pointMouse):
                result = self.activityInUse.OnEvent((pointMouse.getX(),pointMouse.getY()))
        
        elif evento.type == pygame.KEYDOWN:
            event = True
            print 'evento de teclado'
            key = pygame.key.name(evento.key) #retorna l'identificador de la tecla
            k = self.validKey(key)
            if k != None: #Si no es valida, no fem res
                print k
                self.activityInUse.OnKeyEvent(k)
        
        #Si ha hagut event, renderitzem i mirem si s'ha acabat l'activitat
        if event:
            self.activityInUse.OnRender( self.activity_surf)
            
            '''EXTRA:  if activity end, then print the end message '''
            if self.activityInUse.isGameFinished():
                self.dialog.printMessage(self.screen,self.activityInUse.getFinishMessage())
                pygame.display.flip()

                a, b, c, d = pygame.cursors.load_xbm(Constants.Images.CURSOR2, Constants.Images.CURSOR2_MASK)
                pygame.mouse.set_cursor(a, b, c, d)
            #     audio = self.activityInUse.getFinishMessageAudio()
            #     if audio!="":
            #        self.activityInUse.play_sound(audio)
                 #Aqui s'hauria de reproduir l'audio del final
                
            
        return result
        #self.activityInUse.onRender(self.screen)
        # TODO
        # activity_class.update()
	# return resultats, temps, ...
    
    def validKey(self,key):
        '''Llista de tecles que ens interessa processar i la traduccio'''
        validKeyList = {'delete':'delete','backspace':'backspace','space':' ','return':'return',
                        'a':'A','b':'B','c':'C','d':'D','e':'E','f':'F','g':'G','h':'H','i':'I',
                        'j':'J','k':'K','l':'L','m':'M','n':'N','o':'O','p':'P','q':'Q','r':'R',
                        's':'S','t':'T','u':'U','v':'V','w':'W','x':'X','y':'Y','z':'Z'}
        
        if key in validKeyList:
            return validKeyList[key]
        
        return None
    
    
    def canExecuteActivity(self,node):
        print 'classtype=',node.getAttribute('class')
        if  node.getAttribute('class') =='@puzzles.ExchangePuzzle':
                        return True
        elif  node.getAttribute('class') =='@memory.MemoryGame':
                        return True
        elif  node.getAttribute('class') =='@puzzles.DoublePuzzle':
                        return True
        elif  node.getAttribute('class') =='@panels.InformationScreen':
                        return True
        elif  node.getAttribute('class') =='@puzzles.HolePuzzle':
                        return True
        elif  node.getAttribute('class') =='@panels.Identify':
                        return True
        elif  node.getAttribute('class') =='@panels.Explore':
                        return True
        elif  node.getAttribute('class') =='@associations.SimpleAssociation':
                        return True
        elif  node.getAttribute('class') =='@associations.ComplexAssociation':
                        return True
        elif  node.getAttribute('class') =='@textGrid.WordSearch':
                        return True
        elif  node.getAttribute('class') =='@textGrid.CrossWord':
                        return True
        elif  node.getAttribute('class') =='@text.FillInBlanks':
                        return True
        elif  node.getAttribute('class') =='@text.Identify':
                        return True
        elif node.getAttribute('class') == '@text.Complete':
                        return True
        elif node.getAttribute('class') == '@text.Order':
                        return True
        elif  node.getAttribute('class') =='@text.FillInBlanks':
                        return True
        else:
             return False
    def executeActivity(self, node, media, settings):
        if node.getAttribute('class') =='@puzzles.ExchangePuzzle':
                        return ExchangePuzzle(node, media, settings)
        elif  node.getAttribute('class') =='@memory.MemoryGame':
                        return MemoryGame(node, media, settings)
        elif  node.getAttribute('class') =='@puzzles.DoublePuzzle':
                        return DoublePuzzle(node, media, settings)
        elif  node.getAttribute('class') =='@panels.InformationScreen':
                        return InformationScreen(node, media, settings)
        elif  node.getAttribute('class') =='@puzzles.HolePuzzle':
                        return HolePuzzle(node, media, settings)
        elif  node.getAttribute('class') =='@panels.Identify':
                        return IdentifyPanels(node, media, settings)
        elif  node.getAttribute('class') =='@panels.Explore':
                        return PanelsExplore(node, media, settings)
        elif  node.getAttribute('class') =='@associations.SimpleAssociation':
                        return SimpleAssociation(node, media, settings)
        elif  node.getAttribute('class') =='@associations.ComplexAssociation':
                        return ComplexAssociation(node, media, settings)
        elif  node.getAttribute('class') =='@textGrid.WordSearch':
                        return WordSearch(node, media, settings)
        elif  node.getAttribute('class') =='@textGrid.CrossWord':
                        return CrossWord(node, media, settings)
        elif node.getAttribute('class') == '@text.Complete' :
                        return TextComplete(node, media, settings)
        elif node.getAttribute('class') == '@text.FillInBlanks' :
                        return FillInBlanks(node, media, settings)
        elif node.getAttribute('class') == '@text.Order' :
                        return Order(node, media, settings)
        elif node.getAttribute('class') == '@text.Identify' :
                        return Identify(node, media, settings)

