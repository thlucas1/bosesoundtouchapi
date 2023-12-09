# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind

@export
class SearchResult:
    """
    SoundTouch device SearchResult configuration object.
       
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
        self._Artist:str = None
        self._Logo:str = None
        self._Name:str = None
        self._Source:str = None
        self._SourceAccount:str = None
        self._Token:str = None

        if (root is None):
            
            pass
        
        else:

            self._Source = root.get('source')
            self._SourceAccount = root.get('sourceAccount')
            self._Token = root.get('token')
            
            self._Artist = _xmlFind(root, 'artist')
            self._Logo = _xmlFind(root, 'logo')
            self._Name = _xmlFind(root, 'name')
            
            
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    # implement sorting support.
    def __eq__(self, other):
        try:
            return self.Name == other.Name
        except Exception as ex:
            if (isinstance(self, SearchResult )) and (isinstance(other, SearchResult )):
                return self.Name == other.Name
            return False

    def __lt__(self, other):
        try:
            return self.Name < other.Name
        except Exception as ex:
            if (isinstance(self, SearchResult )) and (isinstance(other, SearchResult )):
                return self.Name < other.Name
            return False


    @property
    def Artist(self) -> str:
        """ Name of the artist (for song result), or None (if not present). """
        return self._Artist


    @property
    def Logo(self) -> str:
        """ A url that contains the artwork for the artist or song. """
        return self._Logo


    @property
    def Name(self) -> str:
        """ Name of the artist (for artists result) or the track (for songs result). """
        return self._Name


    @property
    def Source(self) -> str:
        """ Music service source where the result was obtained from (e.g. "PANDORA", "SPOTIFY", etc). """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ Music service source account used to obtain the source (e.g. the music service user-id). """
        return self._SourceAccount


    @property
    def Token(self) -> str:
        """ Token value that uniquely identifies the song or artist. """
        return self._Token


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('searchResult')
        if self._Source and len(self._Source) > 0: elm.set('source', str(self._Source))
        if self._SourceAccount and len(self._SourceAccount) > 0: elm.set('sourceAccount', str(self._SourceAccount))
        if self._Token and len(self._Token) > 0: elm.set('token', str(self._Token))
            
        if self._Name is not None and len(self._Name) > 0:
            elmNode = Element('name')
            elmNode.text = self._Name
            elm.append(elmNode)

        if self._Artist is not None and len(self._Artist) > 0:
            elmNode = Element('artist')
            elmNode.text = self._Artist
            elm.append(elmNode)

        if self._Logo is not None and len(self._Logo) > 0:
            elmNode = Element('logo')
            elmNode.text = self._Logo
            elm.append(elmNode)
            
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SearchResult:'
        msg = '%s Source="%s"' % (msg, str(self._Source))
        msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        msg = '%s Token="%s"' % (msg, str(self._Token))
        if self._Name is not None and len(self._Name) > 0: msg = '%s Name="%s"' % (msg, str(self._Name))
        if self._Artist is not None and len(self._Artist) > 0: msg = '%s Artist="%s"' % (msg, str(self._Artist))
        if self._Logo is not None and len(self._Logo) > 0: msg = '%s Logo="%s"' % (msg, str(self._Logo))
        return msg 
