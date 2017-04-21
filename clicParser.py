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

class Parser:
    def __init__(self):
        self.clic_activities = '' #list of activities that contains the jclic

    #Parse information about the clic (sequence, mediaBag, settings)
    def get_clic_info(self, clic_path, clic_name):
        JClicProject = minidom.parse(clic_path + '/' + clic_name + '.jclic')
        set = JClicProject.getElementsByTagName('settings')
        seq = JClicProject.getElementsByTagName('sequence')
        act = JClicProject.getElementsByTagName('activities')
        med = JClicProject.getElementsByTagName('mediaBag')
        settings = set[0]    
        sequence = seq[0]    
        self.clic_activities = act[0]    
        mediaBag = med[0] 
        return sequence, mediaBag, settings

    #Returns the xml code related with the activity_name
    def get_clic_activity(self, activity_name):
        for clic_activity in self.clic_activities.getElementsByTagName('activity'):
            if clic_activity.getAttribute('name') == activity_name:
                return clic_activity        
        raise SyntaxError, "No activities with this name: " + activity_name  

    
    
    
    
    
    

