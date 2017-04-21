# -*- coding: utf-8 -*-
# Copyright (C) 2007, One Laptop Per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os

import time
import tempfile
import urlparse
import urllib
import xpcom
from xpcom.nsError import *
from xpcom import components
from xpcom.components import interfaces

import paths
import controller


_MIN_TIME_UPDATE = 5        # In seconds
_MIN_PERCENT_UPDATE = 10

_active_downloads = []
_dest_to_window = {}

#component to decide action to do with file (in our case, download only file with extension .xmlclic)
class HelperAppLauncherDialog:
    _com_interfaces_ = interfaces.nsIHelperAppLauncherDialog

    #method to check if the MIME type is .xmlclic (if is .xmclic then start the download)
    def promptForSaveToFile(self, launcher, window_context,
                            default_file, suggested_file_extension,
                            force_prompt=False):
        
        
        file_class = components.classes['@mozilla.org/file/local;1']
        dest_file = file_class.createInstance(interfaces.nsILocalFile)


        if default_file:
            default_file = default_file.encode('utf-8', 'replace')
            base_name, extension = os.path.splitext(default_file)
        else:
            base_name = ''
            if suggested_file_extension:
                extension = '.' + suggested_file_extension
            else:
                extension = ''

        if extension == '.xmlclic':
            temp_path = paths.application_data_path
            file_path = (temp_path + '/' + default_file)
            dest_file.initWithPath(file_path)

            requestor = window_context.queryInterface(interfaces.nsIInterfaceRequestor)
            dom_window = requestor.getInterface(interfaces.nsIDOMWindow)
            _dest_to_window[file_path] = dom_window
        
        return dest_file
                            
    def show(self, launcher, context, reason):
        launcher.saveToDisk(None, False)
        return NS_OK

#component used to download files
class Download:
    _com_interfaces_ = interfaces.nsITransfer
    
    def init(self, source, target, display_name, mime_info, start_time,
             temp_file, cancelable):
        
        #initialize download_file variables
        self._source = source
        self._mime_type = mime_info.MIMEType
        self._temp_file = temp_file
        self._target_file = target.queryInterface(interfaces.nsIFileURL).file
        self._display_name = display_name
        self.cancelable = cancelable

        #variables to check downloading progress
        self._last_update_time = 0
        self._last_update_percent = 0
        
        dom_window = _dest_to_window[self._target_file.path]
        del _dest_to_window[self._target_file.path]

        
        return NS_OK


    #method to check if the download is finished
    def onStateChange(self, web_progress, request, state_flags, status):
        if state_flags & interfaces.nsIWebProgressListener.STATE_STOP:
            if NS_FAILED(status): # download cancelled
                return
            self.controller = controller.Controller()
            self.controller.install_new_clic(self._get_file_name())            

#    #method to follow downloading progress (not necessary, but show the progress)
    def onProgressChange64(self, web_progress, request, cur_self_progress,
                           max_self_progress, cur_total_progress,
                           max_total_progress):
        
        percent = (cur_self_progress  * 100) / max_self_progress

        if (time.time() - self._last_update_time) < _MIN_TIME_UPDATE and \
           (percent - self._last_update_percent) < _MIN_PERCENT_UPDATE:
            return

        self._last_update_time = time.time()
        self._last_update_percent = percent
        print percent


    #method to get the name of the file downloaded
    def _get_file_name(self):
        if self._display_name:
            return self._display_name
        else:
            path = urlparse.urlparse(self._source.spec).path
            location, file_name = os.path.split(path)
            file_name = urllib.unquote(file_name.encode('utf-8', 'replace'))
            return file_name



