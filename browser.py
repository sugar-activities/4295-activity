from hulahop.webview import WebView
import gtk
import xpcom

from xpcom.nsError import *
from xpcom import components
from xpcom.components import interfaces
from xpcom.server.factory import Factory

from downloadmanager import Download
from downloadmanager import HelperAppLauncherDialog



class Browser(WebView):
    def __init__(self):
        WebView.__init__(self)

    
components.registrar.registerFactory('{64355793-988d-40a5-ba8e-fcde78cac631}',
                                     'ClicPlayer Launcher',
                                     '@mozilla.org/helperapplauncherdialog;1',
                                     Factory(HelperAppLauncherDialog))

components.registrar.registerFactory('{23c51569-e9a1-4a92-adeb-3723db82ef7c}',
                                     'ClickPlayer Download',
                                     '@mozilla.org/transfer;1',
                                     Factory(Download))