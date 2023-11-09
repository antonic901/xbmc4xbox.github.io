##############################################################################
#
# Thumbnails - program plugin
#
# Version 1.2
# 
# Author(s):
#
#  * Dan Dar3 
#    http://dandar3.blogspot.com
#

# 
# Constants
#
__plugin__  = "Thumbnails"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "11 September 2011"
__version__ = "1.2"

#
# Imports
#
import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR) 

#
# Main block
#

# Clean..
if ( "action=clean" in sys.argv[ 2 ] ) :
    import thumbnails_clean as plugin
    try:
        gui = plugin.GUI( "DialogTextViewer.xml", os.getcwd(), "default" )
        del gui
    except :
        gui = plugin.GUI( "DialogScriptInfo.xml", os.getcwd(), "default" )
        del gui    

# Main
else:
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    
    import thumbnails_main as plugin
    plugin.Main()