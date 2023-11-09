#
# Imports
#
import os
import sys
import glob
import time
import xbmc
import xbmcgui
import xbmcplugin
import traceback
from BeautifulSoup import BeautifulSoup
from sets          import Set

from urllib import quote_plus, unquote_plus
from os import linesep

#
# Main class
#
class GUI( xbmcgui.WindowXMLDialog ):
    ACTION_EXIT_SCRIPT = ( 9, 10, 216, 257, 61448, )
    THUMB_SUB_DIRS     = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "fanart" ]

    #
    #
    #
    def __init__( self, *args, **kwargs ):
        # Show dialog window...
        self.doModal()

    #
    #
    #
    def onInit( self ):
        #
        # Init
        #
        
        #
        # Scan UserData\Thumbnails...
        #
        try :
            #
            # Init
            #
            THUMBNAILS_PATH = os.path.join( xbmc.translatePath("special://profile/"), "Thumbnails" )
            textboxControl  = self.getControl( 5 )
            output_text     = ""
            
            #
            # Start...
            #
            dialogProgress = xbmcgui.DialogProgress()
            dialogProgress.create( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30200) )

            #
            # (1) Music thumbs (no cleanup)...
            #
            musicThumbPath = os.path.join( THUMBNAILS_PATH, "Music" )
            
            dialogProgress.update( 10, xbmc.getLocalizedString(30201), "Thumbnails\Music")            
            before_file_count, before_total_size = self.scanPath( musicThumbPath )
            
            # Print results...
            output_text = self.getResults( "Thumbnails\Music", before_file_count, before_total_size, before_file_count, before_total_size )
            textboxControl.setText( output_text )
            
            #
            # (3) Picture thumbs...
            #
            picturesThumbPath = os.path.join( THUMBNAILS_PATH, "Pictures" )
                        
            # Scan thumbnails folder (before)...
            dialogProgress.update( 20, xbmc.getLocalizedString(30201), "Thumbnails\Pictures")
            before_file_count, before_total_size = self.scanPath( picturesThumbPath )
            
            # Clean thumbnails...
            dialogProgress.update( 25, xbmc.getLocalizedString(30202), "Thumbnails\Pictures")
            self.cleanThumbnails( picturesThumbPath )
            
            # Scan thumbnails folder (after)...
            dialogProgress.update( 30, xbmc.getLocalizedString(30201), "Thumbnails\Pictures")
            after_file_count, after_total_size   = self.scanPath( picturesThumbPath )
            
            # Print results...
            output_text = output_text + self.getResults( "Thumbnails\Pictures", before_file_count, before_total_size, after_file_count, after_total_size )
            textboxControl.setText( output_text )
            
            #
            # (4) Program thumbnails...
            #
            programsThumbPath = os.path.join( THUMBNAILS_PATH, "Programs" )

            # Scan thumbnails folder (before)...
            dialogProgress.update( 40, xbmc.getLocalizedString(30201), "Thumbnails\Programs")
            before_file_count, before_total_size = self.scanPath( programsThumbPath )
            
            # Clean thumbnails...
            dialogProgress.update( 45, xbmc.getLocalizedString(30202), "Thumbnails\Programs")
            self.cleanThumbnails( programsThumbPath )
            
            # Scan thumbnails folder (after)...
            dialogProgress.update( 50, xbmc.getLocalizedString(30201), "Thumbnails\Programs")
            after_file_count,  after_total_size  = self.scanPath( programsThumbPath )
            
            # Print results...
            output_text = output_text + self.getResults( "Thumbnails\Programs", before_file_count, before_total_size, after_file_count, after_total_size )
            textboxControl.setText( output_text )
            
            #
            # (5) Video thumbs...
            #
            videoThumbPath = os.path.join( THUMBNAILS_PATH, "Video" )
            
            # Scan thumbnails (before)...
            dialogProgress.update( 60, xbmc.getLocalizedString(30201), "Thumbnails\Video")
            before_file_count, before_total_size = self.scanPath( videoThumbPath )
            
            # Scan library (tbns not to clean)...
            except_tbns = Set()
            
            # Library - Movies...
            dialogProgress.update( 65, xbmc.getLocalizedString(30201), "Library\Video\Movies")
            self.scanMovieLibrary( except_tbns )
            
            # Library - TV Shows...
            dialogProgress.update( 70, xbmc.getLocalizedString(30201), "Library\Video\TV Shows")
            self.scanTvShowLibrary( except_tbns )
            
            # Library - Episodes...
            dialogProgress.update( 75, xbmc.getLocalizedString(30201), "Library\Video\Episodes")
            self.scanEpisodeLibrary( except_tbns )
            
            # Library - Seasons
            dialogProgress.update( 80, xbmc.getLocalizedString(30201), "Library\Video\Seasons")
            self.scanSeasonLibrary( except_tbns )
            
            # Library - Actors...
            dialogProgress.update( 85, xbmc.getLocalizedString(30201), "Library\Video\Actors")
            self.scanActorsLibrary( except_tbns )
            
            # Clean video thumbnails...
            dialogProgress.update( 90, xbmc.getLocalizedString(30202), "Thumbnails\Video")
            self.cleanThumbnails( videoThumbPath, except_tbns )
            
            # Scan thumbnails folder (after)...
            dialogProgress.update( 95, xbmc.getLocalizedString(30201), "Thumbnails\Video")
            after_file_count, after_total_size = self.scanPath( videoThumbPath )
            
            # Print results...
            output_text = output_text + self.getResults( "Thumbnails\Video", before_file_count, before_total_size, after_file_count, after_total_size )
            textboxControl.setText( output_text )
            
            #
            # Finished...
            #
            dialogProgress.update( 100, "")
            dialogProgress.close()

            
        #
        # Aw :(
        #
        except Exception :
            dialogProgress.close()
            
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            output_text = repr(traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback))
            
            textboxControl.setText( output_text )
            
        #
        # The end
        #

    #
    #
    #
    def getResults( self, header, files_count_before, files_size_before, files_count_after, files_size_after ):
        text = ""
        text = text + header          + os.linesep
        text = text + "~~~~~~~~~~~~~" + os.linesep
        text = text + "Before = %u file(s), %s"   % ( files_count_before, self.formatSize( files_size_before ) ) + os.linesep
        text = text + "After    = %u file(s), %s" % ( files_count_after,  self.formatSize( files_size_after  ) ) + os.linesep
        text = text + os.linesep
        
        # return value
        return text
    
    #
    # Scan path for thumbnails...
    #
    def scanPath (self, path ):
        # Init
        files_count = 0
        files_size  = 0        
        
        # Scan thumb sub-folders...
        for subdir in self.THUMB_SUB_DIRS :
            thumb_dir = os.path.join( path, subdir )
            if os.path.isdir( thumb_dir ) :
                # .tbn files
                tbn_files = glob.glob( os.path.join( thumb_dir, "*.tbn" ) )
                for tbn_file in tbn_files :
                    statinfo    = os.stat( tbn_file )
                    files_count = files_count + 1
                    files_size  = files_size  + statinfo.st_size
                    statinfo    = None
                    
                # .dds files
                dds_files = glob.glob( os.path.join( thumb_dir, "*.dds" ) )
                for dds_file in dds_files :
                    statinfo    = os.stat( dds_file )
                    files_count = files_count + 1
                    files_size  = files_size  + statinfo.st_size
                    statinfo    = None
                
        # Return value
        return files_count, files_size
        
    #
    # Clean thumbnails from path...
    #
    def cleanThumbnails(self, path, tbn_exceptions = () ):
        # Scan thumb sub-folders...
        for subdir in self.THUMB_SUB_DIRS :
            thumb_dir = os.path.join( path, subdir )
            if os.path.isdir( thumb_dir ) :
                files = os.listdir( thumb_dir )
                for file in files :
                    ( name, ext ) = os.path.splitext( file )
                    
                    # .tbn
                    if ext == ".tbn" :
                        if not file in tbn_exceptions :
                            # Remove thumbnail...
                            tbn_full_path = os.path.join( thumb_dir, file )
                            os.remove( tbn_full_path )

                    # .dds
                    elif ext == ".dds" :
                        tbn_file = name + ".tbn"
                        if not tbn_file in tbn_exceptions :
                            # Remove thumbnail...
                            dds_full_path = os.path.join( thumb_dir, file )
                            os.remove( dds_full_path )


    #
    # Scan library for Movie thumbnails...
    #
    def scanMovieLibrary( self, tbns_set ):
        # Get movie list...
        sql_movies       = "select strPath, strFilename from movieview"
        xml_movies       = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_movies ), )
        
        beautifulSoup    = BeautifulSoup( xml_movies )
        fieldNodes       = beautifulSoup.findAll( "field" )
        fieldNodesTuples = zip( fieldNodes[::2], fieldNodes[1::2])
        
        for fieldNodePath, fieldNodeFile in fieldNodesTuples:
            movie_path          = fieldNodePath.contents[0]
            movie_file          = fieldNodeFile.contents[0]
            movie_file_path     = os.path.join( movie_path, movie_file )
            
            tbn_movie_path      = xbmc.getCacheThumbName( movie_path )
            tbn_movie_file_path = xbmc.getCacheThumbName( movie_file_path )
            
            tbns_set.add( tbn_movie_path )
            tbns_set.add( tbn_movie_file_path )
            
        # Cleanup
        sql_movies       = None
        xml_movies       = None
        fieldNodesTuples = None
        beautifulSoup    = None        

    #
    # Scan library for Actor thumbnails...
    #
    def scanActorsLibrary( self, tbns_set ):         
        # Get actor list...        
        sql_actors    = "select strActor from actors"
        xml_actors    = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_actors ), )
        
        beautifulSoup = BeautifulSoup( xml_actors )
        fieldNodes    = beautifulSoup.findAll( "field" )
        
        for fieldNode in fieldNodes:
            actor_name     = "actor" + str(fieldNode.contents[0]).lower()
            actor_name_tbn = xbmc.getCacheThumbName( actor_name )
        
            tbns_set.add( actor_name_tbn )
            
        # Cleanup
        sql_actors    = None
        xml_actors    = None
        fieldNodes    = None
        beautifulSoup = None          
    
    #
    # Scan library for TVShow thumbnails...
    #
    def scanTvShowLibrary( self, tbns_set ):
        # Get tv show list...        
        sql_tvshows   = "select strPath from tvshowview"
        xml_tvshows   = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_tvshows ), )
        
        beautifulSoup = BeautifulSoup( xml_tvshows )
        fieldNodes    = beautifulSoup.findAll( "field" )
        
        for fieldNode in fieldNodes:
            tvshow_path     = fieldNode.contents[0]
            tbn_tvshow_path = xbmc.getCacheThumbName( tvshow_path )
            
            tbns_set.add( tbn_tvshow_path )
            
        # Cleanup
        sql_tvshows   = None
        xml_tvshows   = None
        fieldNodes    = None
        beautifulSoup = None       

    #
    # Scan library for episode thumbnails...
    #
    def scanEpisodeLibrary( self, tbns_set ):
        # Get episode list...        
        sql_episodes  = "select strPath || strFilename from episodeview"
        xml_episodes  = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_episodes ), )
        
        beautifulSoup = BeautifulSoup( xml_episodes )
        fieldNodes    = beautifulSoup.findAll( "field" )
        
        for fieldNode in fieldNodes:
            episode_full_path = fieldNode.contents[0]
            episode_thumbnail = xbmc.getCacheThumbName( episode_full_path )
            
            tbns_set.add( episode_thumbnail )
            
        # Cleanup
        sql_episodes  = None
        xml_episodes  = None
        fieldNodes    = None
        beautifulSoup = None

    #
    # Scan library for season thumbnails...
    #
    def scanSeasonLibrary ( self, tbns_set ):
        #
        # *All Seasons
        #
        sql_seasons = "select path.strPath"                                                    \
                      " from path"                                                             \
                      " join tvshowlinkpath on tvshowlinkpath.idPath = path.idPath"
        xml_seasons = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_seasons ), )
        
        # Thumbnails...
        beautifulSoup    = BeautifulSoup( xml_seasons )
        fieldNodes       = beautifulSoup.findAll( "field" )
        
        for fieldNode in fieldNodes:
            season_full_path = "season%s%s" % ( fieldNode.contents[0], xbmc.getLocalizedString(20366) )
            season_thumbnail = xbmc.getCacheThumbName( season_full_path )
            
            tbns_set.add( season_thumbnail )
        
        #
        # Season (1..n)
        #
        sql_seasons = "select episodeview.c12, path.strPath"                                   \
                      " from episodeview"                                                      \
                      " join tvshowlinkpath on tvshowlinkpath.idShow = episodeview.idShow "    \
                      " join path           on path.idPath           = tvshowlinkpath.idPath " \
                      " group by path.strPath, episodeview.c12"
        xml_seasons = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_seasons ), )
        
        # Thumbnails...
        beautifulSoup    = BeautifulSoup( xml_seasons )
        fieldNodes       = beautifulSoup.findAll( "field" )
        fieldNodesTuples = zip( fieldNodes[::2], fieldNodes[1::2])
        
        for fieldNodeSeason, fieldNodePath in fieldNodesTuples:
            season_full_path = "season%s%s %s" % ( fieldNodePath.contents[0], xbmc.getLocalizedString(20373), fieldNodeSeason.contents[0] )
            season_thumbnail = xbmc.getCacheThumbName( season_full_path )
            
            tbns_set.add( season_thumbnail )
            
        # Cleanup
        sql_seasons      = None
        xml_seasons      = None
        fieldNodes       = None
        fieldNodesTuples = None
        beautifulSoup    = None        
                
    #
    # Format file size
    #
    def formatSize(self, size):
        SUFFIXES = [ 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        
        for suffix in SUFFIXES :
            size /= 1024
            if size < 1024 :
                return "%.1f %s" % ( size, suffix )

    #
    # onClick handler
    #
    def onClick( self, controlId ):
        pass

    #
    # onFocus handler
    #
    def onFocus( self, controlId ):
        pass

    #
    # onAction handler
    #
    def onAction( self, action ):
        if action and ( action in self.ACTION_EXIT_SCRIPT ):
            self.close()            
