#
# Imports
#
import sys
import xbmc
import urllib
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__( self ):
        #
        # Open file...
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30001), iconImage="DefaultFolder.png" )
        ok = xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = sys.argv[ 0 ] + '?action=edit', listitem=listitem, isFolder=False)

        #
        # Recent files...
        #
        try :
            recent_files = eval( xbmcplugin.getSetting( "recent_files" ) )
        except :
            recent_files = []
        
        for file in recent_files :
            listitem = xbmcgui.ListItem( file, iconImage="DefaultFile.png" )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), 
                                         url = '%s?action=edit&file=%s' % ( sys.argv[ 0 ], urllib.quote_plus( file) ), 
                                         listitem=listitem, 
                                         isFolder=False )

        #
        # Disable sorting...
        #
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

        #
        # End of list...
        #        
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )        
