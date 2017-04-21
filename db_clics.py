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
from xml.dom import minidom
import os
import paths

class DbClics:
    def __init__(self):
        self.loaded = False


    #Creation of the DB
    def __load_db(self):
        if not os.path.exists(self.path_db_new):
            self.__create_db(self.path_db_new)     
        
            
    #Returns a list with all the clics (default and downloaded)          
    def get_clics(self, default):  
        if not self.loaded :
            self.path_db = paths.db_default #Absolute path of the default.xml (File with information about clics stored in the same app)    
            self.path_db_new = paths.db_downloaded#Absolute path of the downloaded.xml (File with information about clics downloaded from the web)       
            self.__load_db()
            self.loaded = True      
  
        doc = minidom.parse(self.path_db)        
        files = doc.childNodes[0]
        l = list()
        clic = {'Title': '',
                    'Author': '',
                    'Area': '',
                    'Language': '',
                    'Folder': '',  
                    'Icon': '',
                    'Default': ''            
                }
        
        if default == True :            
            for file in files.childNodes: 
                clic = {'Title': self.__getText(file.childNodes[0].childNodes),
                        'Author': self.__getText(file.childNodes[1].childNodes),
                        'Area': self.__getText(file.childNodes[2].childNodes),
                        'Language': self.__getText(file.childNodes[3].childNodes),
                        'Folder': self.__getText(file.childNodes[4].childNodes),
                        'Icon': self.__getText(file.childNodes[5].childNodes), 
                        'Default' : 1              
                        }
                l.append(clic)
                
        doc = minidom.parse(self.path_db_new)        
        files = doc.childNodes[0]
        
        for file in files.childNodes: 
            clic = {'Title': self.__getText(file.childNodes[0].childNodes),
                    'Author': self.__getText(file.childNodes[1].childNodes),
                    'Area': self.__getText(file.childNodes[2].childNodes),
                    'Language': self.__getText(file.childNodes[3].childNodes),
                    'Folder': self.__getText(file.childNodes[4].childNodes),
                    'Icon': self.__getText(file.childNodes[5].childNodes),
                    'Default' : 0              
                    }
            l.append(clic)
        
        return l

    #insert clic to the DB    
    def insert_clic(self, clic):
        if not self.loaded :
            self.path_db = paths.db_default #Absolute path of the default.xml (File with information about clics stored in the same app)    
            self.path_db_new = paths.db_downloaded#Absolute path of the downloaded.xml (File with information about clics downloaded from the web)       
            self.__load_db()
            self.loaded = True
            
        if ( self.__is_already_installed(clic['Folder']) == True):
            self.remove_clic_from_db(clic['Folder'])
        
        doc = minidom.parse(self.path_db_new)
        wml = doc.childNodes[0]
                
        #Create the main <card> element
        element = doc.createElement('file')
        wml.appendChild(element)
        
        #Add the new file
        title = doc.createElement('title')
        element.appendChild(title)
        nodeTitle = doc.createTextNode(clic['Title'])
        title.appendChild(nodeTitle)
                
        author = doc.createElement('author')
        element.appendChild(author)
        ptext = doc.createTextNode(clic['Author'])
        author.appendChild(ptext)
                        
        area = doc.createElement('area')
        element.appendChild(area)
        ptext = doc.createTextNode(clic['Area'])
        area.appendChild(ptext)
                        
        language = doc.createElement('language')
        element.appendChild(language)
        ptext = doc.createTextNode(clic['Language'])
        language.appendChild(ptext)
                        
        fileName = doc.createElement('file_name')
        element.appendChild(fileName)
        nodeFile = doc.createTextNode(clic['Folder'])
        fileName.appendChild(nodeFile)
            
        iconName = doc.createElement('icon_name')
        element.appendChild(iconName)
        nodeIcon = doc.createTextNode(clic['Icon'])
        iconName.appendChild(nodeIcon)
                
        file = doc.toxml()
        f = open(self.path_db_new, 'w')
        f.write(file)
        f.close()

    #Creates the file downloaded.xml       
    def __create_db(self, path):
        doc = minidom.Document()
        # Create the <wml> base element
        wml = doc.createElement('files')
        doc.appendChild(wml)
        file = doc.toxml()
        f = open(path, 'w')
        f.write(file)
        f.close()
        
    def __getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

    def remove_clic_from_db(self, folder):
        if not self.loaded :
            self.path_db = paths.db_default #Absolute path of the default.xml (File with information about clics stored in the same app)    
            self.path_db_new = paths.db_downloaded#Absolute path of the downloaded.xml (File with information about clics downloaded from the web)       
            self.__load_db()
            self.loaded = True 
            
        doc = minidom.parse(self.path_db_new)        
        files = doc.childNodes[0]
        
        for file in files.childNodes: 
            print file.childNodes[4].childNodes[0].data
            print folder
            if file.childNodes[4].childNodes[0].data == folder:
                files.removeChild(file)
                
        doc.chilNodes = files
        d = doc.toxml()
        f = open(self.path_db_new, 'w')
        f.write(d)
        f.close()
        
    
    def __is_already_installed(self, folder):
        if not self.loaded :
            self.path_db = paths.db_default #Absolute path of the default.xml (File with information about clics stored in the same app)    
            self.path_db_new = paths.db_downloaded#Absolute path of the downloaded.xml (File with information about clics downloaded from the web)       
            self.__load_db()
            self.loaded = True 
            
        doc = minidom.parse(self.path_db_new)        
        files = doc.childNodes[0]
        
        for file in files.childNodes: 
            print file.childNodes[4].childNodes[0].data
            print folder
            if file.childNodes[4].childNodes[0].data == folder:
                return True
                
        doc = minidom.parse(self.path_db)        
        files = doc.childNodes[0]
        
        for file in files.childNodes: 
            print file.childNodes[4].childNodes[0].data
            print folder
            if file.childNodes[4].childNodes[0].data == folder:
                return True 
            
        return False  