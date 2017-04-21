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
from pygame.locals import *
from Point import *
import pygame.font
class GeneralDialog(object):
    '''
    classdocs
    '''
    pointPrevious = None
    pointNext = None

    ImgNext = None
    ImgPrevious = None
    ImgBackground = None
    rectNext = None
    rectPrev = None
    changeClic = None
    def __init__(self, first, last):

        if(last == True):
            self.ImgNext     =  pygame.image.load(Constants.Images.NEXT_DES).convert_alpha()
        else:
            self.ImgNext     =  pygame.image.load(Constants.Images.NEXT).convert_alpha()

        if(first == True):
            self.ImgPrevious =  pygame.image.load(Constants.Images.PREV_DES).convert_alpha()
        else:
            self.ImgPrevious =  pygame.image.load(Constants.Images.PREV).convert_alpha()
            
        self.ImgChangeClic =  pygame.image.load(Constants.Images.HOME).convert_alpha()
        self.ImgFirst =  pygame.image.load(Constants.Images.FIRST).convert_alpha()
        self.ImgLast =  pygame.image.load(Constants.Images.LAST).convert_alpha()
        self.ImgRetry =  pygame.image.load(Constants.Images.RETRY).convert_alpha()
        self.ImgLogo2 =  pygame.image.load(Constants.Images.LOGO).convert_alpha()
        self.ImgLogo = pygame.transform.scale(self.ImgLogo2,(190,210))

        self.pointLogo = Point((Constants.MAX_WIDTH-210, 20))
        self.pointPrevious = Point((Constants.MAX_WIDTH-210, 60 + 200))
        self.pointNext =  Point((Constants.MAX_WIDTH-210, 130 + 200))
        self.pointFirst = Point((Constants.MAX_WIDTH-210, 200 + 200))
        self.pointLast =  Point((Constants.MAX_WIDTH-210, 270 + 200))
        self.pointRetry =  Point((Constants.MAX_WIDTH-210, 340 + 200))
        self.pointChangeClic = Point((Constants.MAX_WIDTH-210, 410 + 200))

    def renderDialog(self, display_surf):
        ''' Print all rectancles form the General Dialog'''

        ''' THIS PART CAN BE IMPROOVED!!!'''
        rectExt = Rect(0,Constants.MAX_HEIGHT-Constants.MARGIN_BOTTOM,Constants.MAX_WIDTH,Constants.MARGIN_BOTTOM)
        rectInt=    Rect(0,Constants.MAX_HEIGHT-Constants.MARGIN_BOTTOM - 4,Constants.MAX_WIDTH,Constants.MARGIN_BOTTOM)
        #display_surf.fill(Constants.colorBorderDark,rectExt)
        display_surf.fill(Constants.colorGroc,rectInt)

        ''' TEXT Dialog'''
        self.rectTextExt= Rect(20,Constants.MAX_HEIGHT-(Constants.MARGIN_BOTTOM-20),Constants.MAX_WIDTH - 40,Constants.MARGIN_BOTTOM-26)
        self.rectTextInt= Rect(15, Constants.MAX_HEIGHT - (Constants.MARGIN_BOTTOM -20) ,Constants.MAX_WIDTH - 30, Constants.MARGIN_BOTTOM - 30 )
        display_surf.fill(Constants.colorBorderDark,self.rectTextExt)
        display_surf.fill(Constants.colorGroc,self.rectTextInt)


        self.rectDreta= Rect(Constants.MAX_WIDTH-Constants.MARGIN_RIGHT,0,800,800)
        display_surf.fill(Constants.colorGroc,self.rectDreta)

        ''' Buttons'''
        self.rectPrev = display_surf.blit(self.ImgPrevious, (self.pointPrevious.getX(), self.pointPrevious.getY()) )
        self.rectNext = display_surf.blit(self.ImgNext,     (self.pointNext.getX(), self.pointNext.getY()) )
        self.rectFirst = display_surf.blit(self.ImgFirst,     (self.pointFirst.getX(), self.pointFirst.getY()) )
        self.rectLast = display_surf.blit(self.ImgLast,     (self.pointLast.getX(), self.pointLast.getY()) )
        self.rectRetry = display_surf.blit(self.ImgRetry,     (self.pointRetry.getX(), self.pointRetry.getY()) )
        self.rectChangeClic = display_surf.blit(self.ImgChangeClic,     (self.pointChangeClic.getX(), self.pointChangeClic.getY()) )
        self.rectLogo = display_surf.blit(self.ImgLogo,     (self.pointLogo.getX(), self.pointLogo.getY()) )



    def isOverNextButton(self, PointOfMouse):
        x = PointOfMouse.getX()
        y = PointOfMouse.getY()
        if self.rectNext.collidepoint(x,y):
            return True
        else:
            return False

    def printMessage(self,display_surf,message):
        rectText= Rect(37,Constants.MAX_HEIGHT-(Constants.MARGIN_BOTTOM-20),786,Constants.MARGIN_BOTTOM - 20)
        font = pygame.font.Font(None,int(60) )
        text  = font.render(message, True, (255,255,255),Constants.colorLila)

	#self.renderText(message,rectText,font,display_surf,Constants.colorLila)

        #display_surf.fill(Constants.colorBorderDark,self.rectTextExt)
        display_surf.fill(Constants.colorLila,self.rectTextInt)

        if message != None:
            self.renderText(message,self.rectTextInt, 60, display_surf,(255,255,255))

        #display_surf.blit(text,rectText)

    def isOverPreviousButton(self,PointOfMouse):
        x = PointOfMouse.getX()
        y = PointOfMouse.getY()
        if self.rectPrev.collidepoint(x,y):
            return True
        else:
            return False

    def isOverFirstButton(self,PointOfMouse):
        x = PointOfMouse.getX()
        y = PointOfMouse.getY()
        if self.rectFirst.collidepoint(x,y):
            return True
        else:
            return False

    def isOverLastButton(self,PointOfMouse):
        x = PointOfMouse.getX()
        y = PointOfMouse.getY()
        if self.rectLast.collidepoint(x,y):
            return True
        else:
            return False

    def isOverRetryButton(self,PointOfMouse):
        x = PointOfMouse.getX()
        y = PointOfMouse.getY()
        if self.rectRetry.collidepoint(x,y):
            return True
        else:
            return False

    def isOverChangeClicButton(self,PointOfMouse):
        x = PointOfMouse.getX()
        y = PointOfMouse.getY()
        if self.rectChangeClic.collidepoint(x,y):
            return True
        else:
            return False
    def isOverActivity(self,PointOfMouse):
            return True

    def renderText(self,text,rect,fontSize,surf,colour):
        b = False
        
        while not b:
            lines = []
            line = ''
            words = text.split(' ')
            font = pygame.font.Font(None,fontSize)
            for word in words:
                test_line = line + word + ' '
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + ' '
            lines.append(line)
            
            '''Mira si cap el text, sino fa la font mes petita i intenta de nou'''
            total_height = font.size(lines[0])[1] * len(lines)
            
            if total_height > rect.height:
                fontSize -= 2
            else:
                b = True
            
        acum_heigth = 0
	yCord = rect.y + 5

        for line in lines:
            if line != "":
                textline = font.render(line,1,colour)
                surf.blit(textline,(rect.x,yCord))
	    yCord = yCord + font.size(line)[1]+3

            acum_heigth += font.size(line)[1]

