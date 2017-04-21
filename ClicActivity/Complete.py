'''
Created on 09/05/2009

@author: mbenito
'''
import pygame

from Activity import Activity

class Complete(Activity):
    
     
    def Load(self, display_surf):
        self.setBgColor(display_surf)
        
        #contains the text to show in the button
        buttonText = self.xmlActivity.getElementsByTagName('checkButton')[0].childNodes[0].data
        #contains the text to show in the text entry
        section = self.xmlActivity.getElementsByTagName('section')[0]
        print 'Complete.Load'
    
    def OnEvent(self,PointOfMouse):
        print 'Complete.OnEvent'
        
    def OnRender(self,display_surf):
        print 'Complete.OnRender'
        
    def isGameFinished(self):
        print 'Complete.isGameFinished'