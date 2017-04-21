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



MAX_WIDTH = 1200
MAX_HEIGHT = 825
MARGIN_TOP = 20
MARGIN_BOTTOM = 120
MARGIN_LEFT = 20
MARGIN_RIGHT = 220
ACTIVITY_WIDTH = MAX_WIDTH -MARGIN_RIGHT - MARGIN_LEFT - 20
ACTIVITY_HEIGHT= MAX_HEIGHT  -MARGIN_BOTTOM -MARGIN_TOP
colorCell = (0,0,0)
colorPressedCell =(255,127,36)
colorBorder = (255,127,36)
colorBorderDark = ( 92,51,23)
colorBackground = (171,171,171)

colorGroc = (255,12*15,0)
colorLila = (102,44,146)
#colorVermellSolta(,,)

colorWhite = (255,255,255)
colorBlack = (0,0,0)
colorDefault= (42,42,42)
colorMessage = (171,171,171)
colorBlue = (0,0,255)
colorRed = (255,0,0)
colorGreen = (0,255,0)
colorCelestial = (135, 206, 255)

widthCross = 50 #Ample de la cell de la orientacio al crossword
widthOpt = 160
minFontSize = 25
MIN_CELL = 30

DEFAULT_BORDER_SIZE = 3

class Images:
    CURSOR = "img/standardcursor.xbm"
    CURSOR2 = "img/correcte.xbm"
    CURSOR2_MASK = "img/correct_mask.xbm"
    MASK = "img/arrow_mask.xbm"
    NEXT = "img/siguiente.png"
    NEXT_DES= "img/siguiente_des.png"
    PREV = "img/anterior.png"
    PREV_DES = "img/anterior_des.png"
    FIRST = "img/primero.png"
    LAST = "img/ultimo.png"
    RETRY = "img/reiniciar.png"
    HOME = "img/misclics.png"
    LOGO = "img/logotipo6.png"
    ACROSS = "img/across.png"
    DOWN = "img/down.png"

class Sounds:
    OK = "sounds/action_ok.mp3"
    ERROR = "sounds/action_error.mp3"
    CLICK = "sounds/click.mp3"
    
