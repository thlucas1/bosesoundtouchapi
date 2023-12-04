# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind
from .searchstationsongs import SearchStationSongs
from .searchstationartists import SearchStationArtists
from .searchresult import SearchResult

@export
class SearchStationResults:
    """
    SoundTouch device SearchStationResults configuration object.
       
    This class contains the attributes and sub-items that represent a
    single search result item configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._ArtistItems:SearchStationArtists = None
        self._DeviceId:str = None
        self._SongItems:SearchStationSongs = None
        self._Source:str = None
        self._SourceAccount:str = None

        if (root is None):
            
            self._ArtistItems = SearchStationArtists()
            self._SongItems = SearchStationSongs()
        
        else:

            self._DeviceId = root.get('deviceID', default=None)
            self._Source = root.get('source', default=None)
            self._SourceAccount = root.get('sourceAccount', default=None)
            
            if (root.tag == 'results'):
                rootSongs = root.find('songs')
                self._SongItems = SearchStationSongs(root=rootSongs)
                rootArtists = root.find('artists')
                self._ArtistItems = SearchStationArtists(root=rootArtists)
                
            
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ArtistItems(self) -> SearchStationArtists:
        """ 
        The `SearchStationArtists` object that contains found artists results.
        """
        return self._ArtistItems


    @property
    def DeviceId(self):
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId

    
    @property
    def SongItems(self) -> SearchStationSongs:
        """ 
        The `SearchStationSongs` object that contains found songs results.
        """
        return self._SongItems


    @property
    def Source(self) -> str:
        """ Music service source where the result was obtained from (e.g. "PANDORA", "SPOTIFY", etc). """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ Music service source account used to obtain the source (e.g. the music service user-id). """
        return self._SourceAccount


    @property
    def TotalArtistItems(self) -> int:
        """ 
        The total number of artists in the list.
        """
        return len(self._ArtistItems)


    @property
    def TotalSongItems(self) -> int:
        """ 
        The total number of songs in the list.
        """
        return len(self._SongItems)


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('results')
        if self._DeviceId and len(self._DeviceId) > 0: elm.set('deviceID', str(self._DeviceId))
        if self._Source and len(self._Source) > 0: elm.set('source', str(self._Source))
        if self._SourceAccount and len(self._SourceAccount) > 0: elm.set('sourceAccount', str(self._SourceAccount))
       
        item:SearchStationSongs
        for item in self._SongItems:
            elm.append(item.ToElement())

        item:SearchStationArtists
        for item in self._ArtistItems:
            elm.append(item.ToElement())
            
        return elm

        
    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'SearchStationResults:'
        msg = '%s Source="%s"' % (msg, str(self._Source))
        msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        
        if includeItems == False:

            msg = '%s TotalSongs=%s' % (msg, self.TotalSongItems)
            msg = '%s TotalArtists=%s' % (msg, self.TotalArtistItems)
            
        else:

            msg = "%s\nSongs (%d items):" % (msg, self.TotalSongItems)
            item:SearchResult
            for item in self._SongItems:
                msg = "%s\n- %s (%s), %s" % (msg, item.Name, item.Token, item.Artist)
            
            msg = "%s\nArtists (%d items):" % (msg, self.TotalArtistItems)
            item:SearchResult
            for item in self._ArtistItems:
                msg = "%s\n- %s (%s)" % (msg, item.Name, item.Token)
            
        return msg
