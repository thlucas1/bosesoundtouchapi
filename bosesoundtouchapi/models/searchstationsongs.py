# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring
import xmltodict

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr
from ..soundtouchsources import SoundTouchSources
from .searchresult import SearchResult

@export
class SearchStationSongs:
    """
    SoundTouch device SearchStationSongs configuration object.
       
    This class contains the attributes and sub-items that represent the
    searchStation songs response configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Items:list[SearchResult] = []
        
        if (root is None):
            
            pass
        
        else:

            if (root.tag == 'songs'):
                for item in root.findall('searchResult'):
                    self._Items.append(SearchResult(root=item))
            # do not sort - leave in order returned by the music service.


    def __iter__(self) -> Iterator:
        return iter(self._Items)


    def __len__(self) -> int:
        return len(self._Items)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Items(self) -> list[SearchResult]:
        """ 
        The list of `SearchResult` items. 
        """
        return self._Items


    @property
    def TotalItems(self) -> int:
        """ 
        The total number of items in the list.
        """
        return len(self._Items)


    def ContainsArtist(self, source:str, value:str) -> SearchResult:
        """
        Searches the items collection for an item with the specified Source and Artist
        property values and returns the item if found; otherwise, None is returned.
        
        Args:
            source (str):
                Music Service Source value to search for.
            value (str):
                Artist value to search for.
        """
        if isinstance(source, SoundTouchSources):
            source = str(source.value)
        
        result:SearchResult = None
        item:SearchResult
        for item in self._Items:
            if item.Source == source and item.Artist == value:
                result = item
                break
        return result


    def ContainsName(self, source:str, value:str) -> SearchResult:
        """
        Searches the items collection for an item with the specified Source and Name
        property values and returns the item if found; otherwise, None is returned.
        
        Args:
            source (str):
                Music Service Source value to search for.
            value (str):
                Name value to search for.
        """
        if isinstance(source, SoundTouchSources):
            source = str(source.value)
        
        result:SearchResult = None
        item:SearchResult
        for item in self._Items:
            if item.Source == source and item.Name == value:
                result = item
                break
        return result


    def ToDictionary(self, encoding:str='utf-8') -> dict:
        """ 
        Returns a dictionary representation of the class. 
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.
        """
        if encoding is None:
            encoding = 'utf-8'
        elm = self.ToElement()
        xml = tostring(elm, encoding=encoding).decode(encoding)
        
        # convert xml to dictionary.
        oDict:dict = xmltodict.parse(xml,
                                     encoding=encoding,
                                     process_namespaces=False)
        return oDict


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('songs')
        
        item:SearchResult
        for item in self._SongItems:
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
        msg:str = 'SearchStationSongs:'
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            item:SearchResult
            for item in self._Items:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
