import os
import xbmc
import xbmcgui
import xbmcplugin

class GUI( xbmcgui.WindowXMLDialog ):
    # Constants
    ACTION_EXIT_SCRIPT = ( 9, 10, )
    LABEL_CONTROL_ID   = 30010
    LIST_CONTROL_ID    = 30020

    #
    # Init
    #
    def __init__( self, *args, **kwargs ):
        
        # Show dialog window...
        xbmcgui.WindowXML.__init__( self )
        
        # File parameter
        self.file = kwargs[ "file" ]
        
        # Remember file...
        self.rememberRecentFile( self.file )
        
        # Init
        self.fileChanged = False
        self.fileName    = os.path.split( self.file )[1]

    #
    # onInit handler
    #
    def onInit( self ):
        #
        # Init
        #
        self.labelControl = self.getControl( self.LABEL_CONTROL_ID )
        self.listControl  = self.getControl( self.LIST_CONTROL_ID )
        
        self.listControl.setVisible(False);
        
        #
        # Check if file exists...
        #
        if not os.path.isfile( self.file ) :
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30201) % self.file )
            self.close()
            return
        
        # File name...
        self.labelControl.setLabel (" Notepad - %s" % self.file )
        
        dialogWait = xbmcgui.DialogProgress()
        dialogWait.create( xbmc.getLocalizedString(30202), self.file )
        
        #
        # Read file...
        #
        f = open(self.file, "r")
        textLines = f.readlines()
        f.close()
        f = None

        #
        # Populate list control...
        #        
        numLines = len( textLines )
        lineNo   = 0
        for textLine in textLines:
            lineNo       = lineNo + 1
            lineNoString = str( lineNo )
            textLine     = textLine.rstrip( os.linesep ) 
            
            self.listControl.addItem( xbmcgui.ListItem( lineNoString, textLine ) )
            dialogWait.update( lineNo * 100 / numLines, self.file, "%u lines" % numLines )
            if dialogWait.iscanceled() :
                self.close()
                return
        
        dialogWait.close()
        self.listControl.setVisible(True)
    
    #
    # onFocus handler
    #
    def onFocus( self, controlId ):
        pass

    #
    # onAction handler
    #
    def onAction( self, action ):
        #
        # Exit
        #
        if ( action in self.ACTION_EXIT_SCRIPT ):
            # File changed, save?
            if self.fileChanged :
                dialog = xbmcgui.Dialog()
                save   = xbmcgui.Dialog().yesno( self.fileName, xbmc.getLocalizedString(30203) )
                if save : 
                    xbmcgui.lock()
                    numLines  = self.listControl.size()
                    textLines = []
                    for i in range(0, numLines) :
                        textLine = self.listControl.getListItem( i ).getLabel2()
                        if i < numLines - 1 :
                            textLine = textLine + os.linesep
                        textLines.append( textLine )
                    xbmcgui.unlock()
                    
                    # Save file...
                    f = open( self.file, "wb" )
                    f.writelines( textLines )
                    f.close()
            
            # Close window...
            self.close()
            
    #
    # onClick handler
    #
    def onClick( self, controlId ):
        if ( controlId == self.LIST_CONTROL_ID ) :
            selectedItem = self.listControl.getSelectedItem()
            lineNumber   = selectedItem.getLabel()
            textLine     = selectedItem.getLabel2()
            keyboard     = xbmc.Keyboard( textLine, "line %s" % lineNumber )
            keyboard.doModal()
            if keyboard.isConfirmed() :
                textLineNew = keyboard.getText()
                if (textLineNew != textLine) :
                    xbmcgui.lock()
                    selectedItem.setLabel2( textLineNew )
                    self.fileChanged = True 
                    xbmcgui.unlock()
            keyboard = None
                 
    #
    # Remember recent file...
    #
    def rememberRecentFile (self, filename ):
        try :
            recent_files = eval( xbmcplugin.getSetting( "recent_files" ) )
        except :
            recent_files = []
        
        # Add the entry to the list...
        try :
            # ... if not already in the list...
            recent_files.index( filename )
        except :
            recent_files.append( filename )
            
            # Sort the list...
            recent_files.sort()
            
            # Save queries...
            xbmcplugin.setSetting( "recent_files", repr( recent_files ))
