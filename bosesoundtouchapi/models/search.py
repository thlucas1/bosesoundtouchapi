# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindInt
from ..soundtoucherror import SoundTouchError
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtouchsources import SoundTouchSources
from .navigateitem import NavigateItem
from .searchsorttypes import SearchSortTypes
from .searchterm import SearchTerm

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SISession
_logsi:SISession = SIAuto.Si.GetSession(__package__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__package__, True)
_logsi.SystemLogger = logging.getLogger(__package__)


@export
class Search(SoundTouchModelRequest):
    """
    SoundTouch device Search configuration object.
       
    This class contains the attributes and sub-items that represent
    Search criteria.
    """

    def __init__(self, source:str=None, sourceAccount:str=None, 
                 searchTerm:SearchTerm=None, containerItem:NavigateItem=None,
                 startItem:int=None, numItems:int=None, sortType:SearchSortTypes=None, 
                 containerTitle:str=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                Music library source to Search (e.g. "STORED_MUSIC", etc).
            sourceAccount (str):
                Music library source account (e.g. the Music Library user-id).
            searchTerm (SearchTerm):
                Search term object that controls what and how to search for.
            containerItem (NavigateItem):
                Music llibrary container item to search.  
            startItem (int):
                Starting item number to return information for.
            numItems (int):
                Number of items to return.
            sortType (SearchSortTypes|str):
                Sort type used by the Music Library to sort the returned items by.
            containerTitle (str):
                Title to assign to the `ContainerTitle`; also supports formatting - see the
                `ContainerTitleFormatString` property for more details.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchError:
                startItem argument was not of type int.  
        """
        self._NumItems:int = None
        self._ContainerItem:NavigateItem = None
        self._SearchTerm:SearchTerm = None
        self._SortType:str = None
        self._Source:str = None
        self._SourceAccount:str = None
        self._StartItem:int = None
        
        # helper attributes (not part of the xml definition).
        self._ContainerTitleFormatString:str = None
        
        if (root is None):
            
            # convert enums to strings.
            if isinstance(source, SoundTouchSources):
                source = str(source.value)
            if isinstance(sortType, SearchSortTypes):
                sortType = str(sortType.value)
                
            # validations.
            if numItems is not None and (not isinstance(numItems, int)):
                raise SoundTouchError('numItems argument was not of type int', logsi=_logsi)
            if startItem is not None and (not isinstance(startItem, int)):
                raise SoundTouchError('startItem argument was not of type int', logsi=_logsi)
            if not isinstance(searchTerm, SearchTerm):
                raise SoundTouchError('searchTerm argument was not of type SearchTerm', logsi=_logsi)
            if not isinstance(containerItem, NavigateItem):
                raise SoundTouchError('containerItem argument was not of type NavigateItem', logsi=_logsi)

            # helper properties (not part of xml declaration).
            self._ContainerTitleFormatString = containerTitle

            # for STORED_MUSIC sources, ensure we have limits specified.
            # startItem is required; otherwise, the search fails.
            if source == SoundTouchSources.STORED_MUSIC.value:
                if startItem is None or startItem < 1:
                    startItem = 1
                if numItems is None or startItem < 1:
                    numItems = 1000

            self._NumItems = numItems
            self._ContainerItem = containerItem
            self._SearchTerm = searchTerm
            self._SortType = sortType
            self._Source = source
            self._SourceAccount = sourceAccount
            self._StartItem = startItem
        
        elif root.tag == 'search':

            self._SortType = root.get('sort')
            self._Source = root.get('source')
            self._SourceAccount = root.get('sourceAccount')
            
            self._NumItems = _xmlFindInt(root, 'numItems')
            self._StartItem = _xmlFindInt(root, 'startItem')
            
            elmNode:Element = root.find('searchTerm')
            if elmNode is not None:
                self._SearchTerm:SearchTerm = SearchTerm(root=elmNode)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ContainerItem(self) -> NavigateItem:
        """ Music llibrary container item to search. """
        return self._ContainerItem

    @ContainerItem.setter
    def ContainerItem(self, value:NavigateItem):
        """ 
        Sets the ContainerItem property value.
        """
        if value is not None:
            if not isinstance(value, NavigateItem):
                return
        self._ContainerItem = value


    @property
    def ContainerTitle(self) -> str:
        """ 
        Returns formatted container title information for the navigation criteria.
        Format is controlled by the `ContainerTitleFormatString` property value.
        
        This allows the caller to easily retrieve (and format) information for display
        about the current navigation path without having to check for null values.
        """
        result = self.ContainerTitleFormatString

        source:str = self._Source or ''
        sourceAccount:str = self._SourceAccount or ''
        name:str = "Root"
        location:str = "0"
        searchterm:str = "*not specified*"

        SOURCE:str = '{source}'
        SOURCEACCOUNT:str = '{sourceaccount}'
        NAME:str = '{name}'
        LOCATION:str = '{location}'
        SEARCHTERM:str = '{searchterm}'

        if self._SearchTerm is not None:
            searchterm = "\"%s\"" % self._SearchTerm.SearchText
            
        if self._ContainerItem is not None:
            name = self._ContainerItem._Name or ''
            if self._ContainerItem._ContentItem is not None:
                location = self._ContainerItem._ContentItem._Location or ''
            
        if result.find(SOURCE) > -1:
            result = result.replace(SOURCE, source)
        if result.find(SOURCEACCOUNT) > -1:
            result = result.replace(SOURCEACCOUNT, sourceAccount)
        if result.find(NAME) > -1:
            result = result.replace(NAME, name)
        if result.find(LOCATION) > -1:
            result = result.replace(LOCATION, location)
        if result.find(SEARCHTERM) > -1:
            result = result.replace(SEARCHTERM, searchterm)

        return result        


    @property
    def ContainerTitleFormatString(self) -> str:
        """ 
        Gets container title format string.
        
        This property controls how the `ContainerTitle` property value is formatted.
        
        The following keywords are supported:
        * `{source}` - Music Library source to navigate.  
        * `{sourceaccount}` - Music Library source account.  
        * `{name}` - Name of the container to navigate.  
        * `{location}` - Location of the container to navigate.  
        
        Default is "{name} ({source}, '{sourceaccount}', '{location}')".
        """
        if self._ContainerTitleFormatString is None:
            self._ContainerTitleFormatString = "{name} [{location}], for {searchterm}"
        return self._ContainerTitleFormatString

    @ContainerTitleFormatString.setter
    def ContainerTitleFormatString(self, value:str):
        """ 
        Sets the ContainerTitleFormatString property value.
        """
        if value is not None:
            self._ContainerTitleFormatString = value


    @property
    def NumItems(self) -> int:
        """ Number of items to return. """
        return self._NumItems

    @NumItems.setter
    def NumItems(self, value:int):
        """ 
        Sets the NumItems property value.
        """
        if isinstance(value, int):
            self._NumItems = value


    @property
    def SearchTerm(self) -> str:
        """ Search term object that controls what and how to search for. """
        return self._SearchTerm

    @SearchTerm.setter
    def SearchTerm(self, value:str):
        """ 
        Sets the SearchTerm property value.
        """
        if value is not None:
            if not isinstance(value, SearchTerm):
                return
        self._SearchTerm = value


    @property
    def SortType(self) -> str:
        """ Sort type used by the Music Library to sort the returned items by. """
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
        """ Music library source to Search (e.g. "STORED_MUSIC", etc). """
        return self._Source

    @Source.setter
    def Source(self, value:str):
        """ 
        Sets the Source property value.
        """
        if isinstance(value, SoundTouchSources):
            value = value.value
        self._Source = value


    @property
    def SourceAccount(self) -> str:
        """ Music library source account (e.g. the Music Library user-id). """
        return self._SourceAccount

    @SourceAccount.setter
    def SourceAccount(self, value:str):
        """ 
        Sets the SourceAccount property value.
        """
        self._SourceAccount = value


    @property
    def StartItem(self) -> int:
        """ 
        Starting item number to return information for. 
        
        StartItem is required, otherwise the search fails.
        """
        return self._StartItem

    @StartItem.setter
    def StartItem(self, value:int):
        """ 
        Sets the StartItem property value.
        """
        if isinstance(value, int):
            self._StartItem = value


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
        if self._Source is not None and len(self._Source) > 0: elm.set('source', str(self._Source))
        if self._SourceAccount is not None and len(self._SourceAccount) > 0: elm.set('sourceAccount', str(self._SourceAccount))
        if self._SortType is not None and len(self._SortType) > 0: elm.set('sortOrder', str(self._SortType))

        if self._StartItem is not None:
            elmNode = Element('startItem')
            elmNode.text = str(self._StartItem)
            elm.append(elmNode)

        if self._NumItems is not None:
            elmNode = Element('numItems')
            elmNode.text = str(self._NumItems)
            elm.append(elmNode)

        if self._SearchTerm is not None:
            elmNode = self._SearchTerm.ToElement()
            elm.append(elmNode)
            
        if self._ContainerItem is not None:
            elmNode = self._ContainerItem.ToElement()
            elm.append(elmNode)
            
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Search:'
        msg = '%s Source="%s"' % (msg, str(self._Source))
        msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        if self._SortType is not None and len(self._SortType) > 0: msg = '%s SortType="%s"' % (msg, str(self._SortType))
        msg = '%s StartItem=%s' % (msg, str(self._StartItem))
        if self._NumItems is not None: msg = '%s NumItems=%s' % (msg, str(self._NumItems))
        if self._SearchTerm is not None: msg = '%s %s' % (msg, str(self._SearchTerm))
        if self._ContainerItem is not None: msg = '%s %s' % (msg, str(self._ContainerItem))
        return msg 
