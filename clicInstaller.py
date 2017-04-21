# -*- coding: utf-8 -*-
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
import re
import threading
import paths
import shutil
import gtk
from gettext import gettext as _
import controller

class Installer:
    def __init__(self):
        self.clics_path = ""
        self.data_path = ""
        self.hasPaths = False

            
    def __getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

    #Parse information about the clic (sequence, mediaBag, settings)
    def get_clic_info(self, file):
        
        if (self.hasPaths == False) :
            #init paths
            self.clics_path = paths.new_clics_path  #folder to install clics
            self.data_path = paths.application_data_path
            self.views_path = paths.views_path
            self.icons_path = paths.icons_path
            #init popup window
            self.xml = gtk.glade.XML(self.views_path + '/DownloadingInfo.glade')
            self.window = self.xml.get_widget('window')
            self.label = self.xml.get_widget('label')
            self.ImageGo = self.xml.get_widget('image') 
            self.ImageGo.set_from_file(self.icons_path + '/si.png')
            self.window.resize(1200, 75)
            self.window.move(0, 825)
            self.hasPaths = True
        
        #unzip the file with metadata
        from_path = os.path.join(self.data_path, file)
        t = self.__unzip_file(from_path, self.data_path)
        
        #parse XML to get all the information about the Clic
        clicInfo = minidom.parse(self.data_path + '/' + file)
        
        #information to download the clic and icon
        urlsC = clicInfo.getElementsByTagName('urlClic')   
        urlsI = clicInfo.getElementsByTagName('urlIcon') 
        
        #information about the clic (subject, author, license, ...)
        subjectElem = clicInfo.getElementsByTagName('Subject')
        authorElem = clicInfo.getElementsByTagName('Author')
        licenseElem = clicInfo.getElementsByTagName('License')
        themeElem = clicInfo.getElementsByTagName('Theme')
        languageElem = clicInfo.getElementsByTagName('Language')
        
        self.subject = ''
        self.author = ''
        self.license = ''
        self.theme = ''
        self.language = ''
       
        #check if all the fields are informed
        if (subjectElem.length != 0 ) : self.subject =  self.__getText(subjectElem[0].childNodes)
        if (authorElem.length != 0) : self.author = self.__getText(authorElem[0].childNodes)
        if (licenseElem.length != 0) : self.license = self.__getText(licenseElem[0].childNodes)
        if (themeElem.length != 0) : self.theme = self.__getText(themeElem[0].childNodes)
        if (languageElem.length != 0) : self.language = self.__getText(languageElem[0].childNodes)
                       
        clic = {'Title': self.subject,
                'Author': self.author,
                'Area': self.theme,
                'Language': self.language,
                'Folder': '',
                'Icon': ''
                }     
        
        
        fileUrls = list()
        iconUrls = list()
        
        #get all the urls (to download clic and to download icon
        for url in  urlsC:
            oneUrl = self.__getText(url.childNodes)
            if oneUrl != "" :
                fileUrls.append(url.childNodes[0].data)
                
        for url in  urlsI:
            iconUrls.append(url.childNodes[0].data)
         
        #put all the information in a list to send it to the thread that downloads the files       
        l = list()
        l.append(clic)
        l.append(fileUrls)
        l.append(iconUrls)
            
        #downloads the new clic file in background (every download has its own thread)
        hilo = threading.Thread(target=self.__download_file, args=(l))
        hilo.start()
        self.__delete_file(self.data_path, file)
        

    def __download_file(self, *urls):
        initial_text = 'ONCE DOWNLOADED, YOU WILL HAVE THE CLIC ON YOUR LIST.'
        self.__show_warning(initial_text, None)
        
        clic = urls[0]
        file_urls_to_download = urls[1]
        icons_url_to_download = urls[2]

        done = False                
        i = 0
        
        #Find a valid url and download the clic.
        while ((done == False) and (i < len(file_urls_to_download))) : 
            
            file =  file_urls_to_download[i].split("/")[-1]
            folder = file.split('.',1)[0]
            clic['Folder'] = folder
            
            t = self.__wget_file(file_urls_to_download[i], self.clics_path)  
            if t == 0:
                from_path = os.path.join(self.clics_path, file)
                to_path = os.path.join(self.clics_path, folder)
                t = self.__unzip_file(from_path, to_path)   
                if t == 0:
                    self.__delete_file(self.clics_path, file)
                    print 'Installed in folder clics/' + folder
                    self.controller = controller.Controller()
                    done = True
                        
            i = i + 1
        
        #If it was possible to download the clic, download its icon.         
        if done == True :
            to_path = os.path.join(self.clics_path, folder)
            t = self.__wget_file(icons_url_to_download[0], to_path)
            if t == 0:
                icon =  icons_url_to_download[0].split("/")[-1]
                clic['Icon'] = icon  
            else :
                clic['Icon'] = ''
            #calls the controller to add a new clic to the db list     
            self.controller.add_new_clic(clic)
                           
        if done == False:
            self.__show_warning('IT WAS NOT POSSIBLE TO DOWNLOAD', clic['Title'])
    
    #removes all the data of a clic's folder.
    def delete_clic_folder(self, clics_folder):
        shutil.rmtree(paths.new_clics_path + '/' + clics_folder)
    
    #removes zip file.
    def __delete_file(self, path, file):
        file_to_remove = os.path.join(path, file)
        t = os.remove(file_to_remove)      
            
    #Unzips a file to a new path (it will overwrite content if exists).
    def __unzip_file(self, from_path, to_path):   
        t = os.system('unzip -o '+ from_path + ' -d ' + to_path)                 
        return t  
    
    #Wget downloads a file from a url and stores it in a path
    def __wget_file(self, url, to_path):
        t = os.system('wget -q ' + url + ' --directory-prefix=' + to_path)  
        return t
    
    #shows an alert to the user to inform about the status of the download (clic).  
    def __show_warning(self, text, clic):     
        if clic == None :
            self.label.set_text(_(text))
        else :
            text = _(text) + ' "' + clic + '".'
            self.label.set_text(text)
        self.window.show()
        self.button = self.xml.get_widget('button')
        self.button.connect('clicked', self.__destroy_win)

    def __destroy_win(self, *args):
        self.window.hide()
    

