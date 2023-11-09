#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__( self ):
        #
        # Clean
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30001), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=clean' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=False)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )