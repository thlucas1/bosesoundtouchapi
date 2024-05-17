# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFindInt
from ..soundtouchsources import SoundTouchSources
from .navigateitem import NavigateItem

@export
class NavigateResponse:
    """
    SoundTouch device NavigateResponse configuration object.
       
    This class contains the attributes and sub-items that represent the
    navigate response configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Items:list[NavigateItem] = []
        self._Source:str = None
        self._SourceAccount:str = None
        self._TotalItems:int = None
        
        # helper properties (non-xml).
        self._SourceTitle:str = None

        if (root is None):
            
            pass
        
        elif root.tag == 'navigateResponse':
                
            self._Source = root.get('source')
            self._SourceAccount = root.get('sourceAccount')
            self._TotalItems = _xmlFindInt(root, 'totalItems')
            
            rootItems = root.find('items')
            if rootItems is not None:
                for item in rootItems.findall('item'):
                    self._Items.append(NavigateItem(root=item))


    def __iter__(self) -> Iterator:
        return iter(self._Items)


    def __len__(self) -> int:
        return len(self._Items)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ItemCount(self) -> int:
        """ 
        The number of items in the `Items` list.  
        
        Note that this could be different than the `TotalItems` property if
        the user is limiting the returned results.
        """
        return len(self._Items)


    @property
    def Items(self) -> list[NavigateItem]:
        """ 
        The list of `NavigateItem` items. 
        """
        return self._Items


    @property
    def Source(self) -> str:
        """ Music service source where the result was obtained from (e.g. "PANDORA", etc). """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ The account associated with the Source. """
        return self._SourceAccount


    @property
    def SourceTitle(self) -> str:
        """ 
        The source title of media content (e.g. "Pandora (userid)", etc). 
        
        This property is not part of the returned xml of the configuration, but is set after
        a call to `SoundTouchClient.GetMusicServiceStations` and `SoundTouchClient.GetMusicLibraryItems` 
        so that the source title can be displayed by user-interfaces.
        """
        return self._SourceTitle

    @SourceTitle.setter
    def SourceTitle(self, value:str):
        """ 
        Sets the SourceTitle property value.
        """
        self._SourceTitle = value


    @property
    def TotalItems(self) -> int:
        """ 
        The total number of items in the list, as reported by the music service.
        """
        return self._TotalItems


    def GetItemByName(self, name:str) -> NavigateItem:
        """
        Searches the items collection for an item with the specified Name
        and returns the matching item if found; otherwise, None is returned.
        
        Args:
            name (str):
                Name value to search for (case-sensitive).
        """
        result:NavigateItem = None
        item:NavigateItem
        for item in self._Items:
            if item.Name == name:
                result = item
                break
        return result


    def ContainsLocation(self, source:str, location:str) -> NavigateItem:
        """
        Searches the items collection for an item with the specified Source and ContentItem.Location
        property values and returns the item if found; otherwise, None is returned.
        
        Args:
            source (str):
                Music Service Source value to search for.
            location (str):
                ContentItem.Location value to search for.
        """
        if isinstance(source, SoundTouchSources):
            source = str(source.value)
        
        result:NavigateItem = None
        item:NavigateItem
        for item in self._Items:
            if item.ContentItem.Location == location and item.ContentItem.Source == source:
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
            
        result:dict = {}

        # self._Items:list[NavigateItem] = []

        if self._Source is not None: 
            result['Source'] = self._Source
        if self._SourceAccount is not None: 
            result['SourceAccount'] = self._SourceAccount
        if self._SourceTitle is not None: 
            result['SourceTitle'] = self._SourceTitle
        if self._TotalItems is not None: 
            result['TotalItems'] = self._TotalItems
        result['ItemCount'] = self.ItemCount
        result['Items'] = [ item.ToDictionary(encoding) for item in self._Items ]

        return result


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('items')
        elm.set('totalItems', str(self._TotalItems))
        elm.set('itemCount', str(self.ItemCount))

        # include the source title if this is not a request body.
        if isRequestBody == False:
            if self._SourceTitle is not None and len(self._SourceTitle) > 0: elm.set('SourceTitle', str(self._SourceTitle))

        # include all items.
        item:NavigateItem
        for item in self._Items:
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
        msg:str = 'NavigateResponse:'
        msg = '%s Source="%s"' % (msg, str(self._Source))
        msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        if self._SourceTitle is not None: msg = '%s SourceTitle="%s"' % (msg, str(self._SourceTitle))
        if self._TotalItems is not None: msg = '%s TotalItems="%s"' % (msg, str(self.TotalItems))
        
        if includeItems == True:
            
            msg = "%s\n(%d items)" % (msg, self.ItemCount)
            item:NavigateItem
            for item in self._Items:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
