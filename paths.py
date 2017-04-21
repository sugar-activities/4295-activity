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
from sugar.activity import activity
import os

# paths used in the application
application_data_path = ''      #path where the application can store permanent data
application_bundle_path = ''    #path where the application is installed (/home/olpc/Activities/ClicPlayer.activity
        
clics_path =  ''                #path to the folder that contains default clics
new_clics_path = ''             #path to the folder that contains new clics
about_path = ''                 #path to the folder that contains the about info
manual_path = ''                #path to the folder that contains the manual
        
db_downloaded = ''              #path to db of new clics
db_default = ''                 #path to db of default clics

icons_path = ''                 #path to the icons used in the application (clics icon, button icons,...)
views_path = ''                 #path to the views of the application


#Returns the absolute path of the clic folder
def get_clic_path(clic_name, is_default):
    p = new_clics_path
    if is_default == '1':
        p = application_bundle_path + '/data/clics'
    return os.path.join(p , clic_name)
    
def set_environment(is_Xo):
    global application_bundle_path, application_data_path, clics_path, about_path, manual_path, new_clics_path, db_downloaded, db_default, icons_path, views_path
    if is_Xo : #Sets environment for a XO-laptop.
        
        application_data_path = os.path.join(activity.get_activity_root(), 'data')
        application_bundle_path = activity.get_bundle_path()
        
        clics_path = os.path.join(application_bundle_path , 'data/clics') 
        new_clics_path = application_data_path + '/clics'
        about_path = application_bundle_path + '/data/clics/about'
        manual_path = application_bundle_path + '/data/clics/sugar_clic_help'
        
        db_downloaded = os.path.join(application_data_path , 'downloaded.xml')
        db_default = os.path.join(application_bundle_path , 'data/default.xml')
        
        img_app_path = os.path.join(application_bundle_path, 'img/app') 
        views_path = os.path.join(img_app_path, 'appViews')
        icons_path = os.path.join(img_app_path, 'appIcons')
        
    else: #Sets environment for a UNIX computer.
        
        current_path = os.getcwd()
        application_data_path = os.path.join(current_path, 'new/data')
        application_bundle_path = current_path
        
        clics_path = os.path.join(application_bundle_path , 'data/clics')
        new_clics_path = application_data_path + '/clics'
        about_path = application_bundle_path + '/data/clics/about'
        manual_path = application_bundle_path + '/data/clics/sugar_clic_help'
        
        db_downloaded = os.path.join(application_data_path , 'downloaded.xml')
        db_default = os.path.join(application_bundle_path , 'data/default.xml')
        
        img_app_path = os.path.join(application_bundle_path, 'img/app') 
        views_path = os.path.join(img_app_path, 'appViews')
        icons_path = os.path.join(img_app_path, 'appIcons')
        
    __create_clics_path()
        

def __create_clics_path():        
    if not os.path.exists(clics_path):
            t = os.system('mkdir ' + clics_path)
    
    