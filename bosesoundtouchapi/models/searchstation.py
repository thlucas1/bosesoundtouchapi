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
class SearchStation(SoundTouchModelRequest):
    """
    SoundTouch device SearchStation configuration object.
       
    This class contains the attributes and sub-items that represent
    SearchStation criteria.
    """

    def __init__(self, source:str=None, sourceAccount:str=None, searchText:str=None, 
                 sortType:SearchSortTypes=None, filterType:SearchFilterTypes=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                Music service source to search (e.g. "PANDORA", "SPOTIFY", etc).
            sourceAccount (str):
                Music service source account (e.g. the music service user-id).
            searchText (str):
                Text to search for in the Music service.
            sortType (SearchSortTypes|str):
                Sort type used by the Music Service to sort the returned items by.
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
        self._SortType:str = None
        self._Source:str = None
        self._SourceAccount:str = None
        
        if (root is None):
            
            # convert enums to strings.
            if isinstance(source, SoundTouchSources):
                source = str(source.value)
            if isinstance(sortType, SearchSortTypes):
                sortType = str(sortType.value)
            if isinstance(filterType, SearchFilterTypes):
                filterType = str(filterType.value)
               
            self._FilterType = filterType
            self._SearchText = searchText
            self._SortType = sortType
            self._Source = source
            self._SourceAccount = sourceAccount
        
        else:

            self._FilterType = root.get('filter')
            self._SortType = root.get('sortOrder')
            self._Source = root.get('source')
            self._SourceAccount = root.get('sourceAccount')
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
        """ Text to search for in the Music service. """
        return self._SearchText

    @SearchText.setter
    def SearchText(self, value:str):
        """ 
        Sets the SearchText property value.
        """
        if value is not None:
            if isinstance(value, str):
                self._SearchText = value


    @property
    def SortType(self) -> str:
        """ Sort type used by the Music Service to sort the returned items by. """
        return self._SortType

    @SortType.setter
    def SortType(self, value:str):
        """ 
        Sets the SortType property value.
        """
        if isinstance(value, SearchSortTypes):
            value = value.value
        self._SortType = value


    @property
    def Source(self) -> str:
        """ Music service source to search (e.g. "PANDORA", "SPOTIFY", etc). """
        return self._Source

    @Source.setter
    def Source(self, value:str):
        """ 
        Sets the Source property value.
        """
        if value is not None:
            if isinstance(value, SoundTouchSources):
                self._Source = value.value
            elif isinstance(value, str):
                self._Source = value


    @property
    def SourceAccount(self) -> str:
        """ The account associated with the Source. """
        return self._SourceAccount

    @SourceAccount.setter
    def SourceAccount(self, value:str):
        """ 
        Sets the SourceAccount property value.
        """
        if value is not None:
            if isinstance(value, str):
                self._SourceAccount = value


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('search')
        if self._Source and len(self._Source) > 0: elm.set('source', str(self._Source))
        if self._SourceAccount and len(self._SourceAccount) > 0: elm.set('sourceAccount', str(self._SourceAccount))
        if self._SortType and len(self._SortType) > 0: elm.set('sortOrder', str(self._SortType))
        if self._FilterType and len(self._FilterType) > 0: elm.set('filter', str(self._FilterType))

        if self._SearchText and len(self._SearchText) > 0: 
            elm.text = self._SearchText

        return elm
        
        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SearchStation:'
        msg = '%s Source="%s"' % (msg, str(self._Source))
        msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        msg = '%s SearchText="%s"' % (msg, str(self._SearchText))
        if self._SortType is not None and len(self._SortType) > 0: msg = '%s SortType="%s"' % (msg, str(self._SortType))
        if self._FilterType is not None: msg = '%s FilterType=%s' % (msg, str(self._FilterType))
        return msg 
    