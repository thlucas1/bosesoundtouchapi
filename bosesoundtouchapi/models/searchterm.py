# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtouchsources import SoundTouchSources
from .searchfiltertypes import SearchFilterTypes
from .searchsorttypes import SearchSortTypes

@export
class SearchTerm(SoundTouchModelRequest):
    """
    SoundTouch device SearchTerm configuration object.
       
    This class contains the attributes and sub-items that represent
    SearchTerm criteria.
    """

    def __init__(self, searchText:str=None, filterType:SearchFilterTypes=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            searchText (str):
                Text to search for.
            filterType (SearchFilterTypes|str):
                Filter type used by the Music Service to filter the returned items by.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchError:
                startItem argument was not of type int.  
        """
        self._FilterType:str = None
        self._SearchText:str = None
        
        if (root is None):
            
            # convert enums to strings.
            if isinstance(filterType, SearchFilterTypes):
                filterType = str(filterType.value)
               
            self._FilterType = filterType
            self._SearchText = searchText
        
        else:

            self._FilterType = root.get('filter')
            self._SearchText = root.text
            

    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def FilterType(self) -> str:
        """ Filter type used by the Music Service to filter the returned items by. """
        return self._FilterType

    @FilterType.setter
    def FilterType(self, value:str):
        """ 
        Sets the FilterType property value.
        """
        if isinstance(value, SearchFilterTypes):
            value = value.value
        self._FilterType = value


    @property
    def SearchText(self) -> str:
        """ Text to search for. """
        return self._SearchText

    @SearchText.setter
    def SearchText(self, value:str):
        """ 
        Sets the SearchText property value.
        """
        if value is not None:
            if isinstance(value, str):
                self._SearchText = value


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('searchTerm')
        if self._FilterType and len(self._FilterType) > 0: elm.set('filter', str(self._FilterType))

        if self._SearchText and len(self._SearchText) > 0: 
            elm.text = self._SearchText

        return elm
        
        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SearchTerm:'
        msg = '%s SearchText="%s"' % (msg, str(self._SearchText))
        if self._FilterType is not None: msg = '%s FilterType=%s' % (msg, str(self._FilterType))
        return msg 
    