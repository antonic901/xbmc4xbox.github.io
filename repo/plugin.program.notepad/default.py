##############################################################################
#
# Notepad - Program plugin for XBMC
#
# Version 1.4
# 
# Coding by Dan Dar3 
# http://dandar3.blogspot.com
#

# 
# Constants
#
__plugin__  = "Notepad"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "14 August 2010"
__version__ = "1.4"


#
# Imports
#
import os
import sys
import urllib
import xbmcgui
import xbmcplugin

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR) 

#
# Edit window
#
if ( "action=edit" in sys.argv[ 2 ] ):
    #
    # Check if a file was passed as a parameter...
    #
    params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
    file   = urllib.unquote_plus( params.get( "file", "" ) )
    
    #
    # Browse for movie file...
    #
    if file == "" :
        browse = xbmcgui.Dialog()
        file   = browse.browse(1, xbmc.getLocalizedString(30200), "files", "")
    
    #
    # Open in editor window...
    #
    if file != "" :   
        import notepad_edit as plugin
        gui = plugin.GUI( "notepad_edit.xml", os.getcwd(), "default", file=file)
        gui.doModal()
        del gui
        
        xbmc.executebuiltin("Container.Refresh")
#
# Main menu
#
else :
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    import notepad_main as plugin
    plugin.Main()    
