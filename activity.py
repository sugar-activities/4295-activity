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
import gtk
import os
import gobject
# Load our own source code from Manager.py
# There you can find the main class Manager()
from Manager import Manager
# Load sugar libraries
from sugar.activity import activity  
from gettext import gettext as _

class ClicPlayerActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self._name = handle

        # Set title for our Activity
        self.set_title(_('Clic Player'))

        # Attach sugar toolbox (Share, ...)
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        # Create the main container
        self._main_view = gtk.VBox()
        
        # Import our class Manager():

        # Step 1: Load class, which creates Manager.widget
        self.Manager = Manager()

        # Step 2: Remove the widget's parent
        if self.Manager.widget.parent:
            self.Manager.widget.parent.remove(self.Manager.widget)
 
        # Step 3: We attach that widget to our window
        self._main_view.pack_start(self.Manager.widget)

        # Display everything
        self.Manager.widget.show()
        self._main_view.show()
        self.set_canvas(self._main_view)
        self.show()
        
        #called every 250 miliseconds (for pygame)
        gobject.timeout_add(250, self.Manager.updating)

