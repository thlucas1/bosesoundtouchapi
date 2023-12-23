# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring
import xmltodict

# our package imports.
from ..bstutils import export
from .sourceitem import SourceItem

@export
class SourceList:
    """
    SoundTouch device SourceList configuration object.
       
    This class contains the attributes and sub-items that represent the
    sources configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._DeviceId:str = None
        self._SourceItems:list[SourceItem] = []
        
        if (root is None):
            
            pass
        
        else:

            # base fields.
            if (root.tag == 'sources'):
                self._DeviceId = root.get('deviceID')
                for item in root:
                    self._SourceItems.append(SourceItem(root=item))
            else:
                source_item_list = root.find('sources')
                if source_item_list is not None:
                    self._DeviceId = root.get('deviceID')
                    for item in root.find('sources'):
                        self._SourceItems.append(SourceItem(root=item))

            # sort items on Source property, descending order.
            if len(self._SourceItems) > 0:
                self._SourceItems.sort(key=lambda x: (x.Source or "").lower(), reverse=False)


    def __getitem__(self, key) -> SourceItem:
        if isinstance(key, str):
            for item in self._SourceItems:
                if item.Source == key:
                    return item
        else:
            return self._SourceItems[key]


    def __iter__(self) -> Iterator:
        return iter(self._SourceItems)


    def __len__(self) -> int:
        return len(self._SourceItems)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId

    
    @property
    def SourceItems(self) -> list[SourceItem]:
        """ 
        The list of `SourceItem` items. 
        """
        return self._SourceItems


    def GetSourceItemByTitle(self, title:str) -> SourceItem:
        """
        Returns a `SourceItem` instance for the given source title value.
        
        Args:
            title (str):
                Source title string to locate in the `SourceItems` list.
                Value is case-sensitive, and must match exactly.
                
        Returns:
            A `SourceItem` if the title argument value was found; otherwise, None.
        """
        item:SourceItem
        for item in self._SourceItems:
            if title == item.SourceTitle:
                return item
        return None
        

    def GetTitleBySource(self, source:str, sourceAccount:str=None) -> str:
        """
        Returns a title for the given source and sourceAccount values.
        
        Args:
            source (str):
                The source of media content (e.g. "TUNEIN", "AIRPLAY", "UPNP", etc).
                Value is case-sensitive, and must match exactly.
            sourceAccount (str):
                The account associated with the Source.
                Value is case-sensitive, and must match exactly.
                
        Returns:
            A `SourceItem`.`SourceTitle` if the title argument value was found; 
            otherwise, None.
        """
        # if source not specified then don't bother.
        if source is None:
            return None
        
        # source list will never contain a 'sourceAccount=""' value; the sourceAccount
        # attribute will not be specified in this case (e.g. TUNEIN, BLUETOOTH, etc).
        # however, sometimes a NowPlaying event will generate a 'sourceAccount=""' value
        # for a source
        item:SourceItem
        for item in self._SourceItems:
            if source == item.Source:
                itemSourceAccount:str = item.SourceAccount
                if (itemSourceAccount == sourceAccount):
                    return item.SourceTitle
                elif (itemSourceAccount is None) and (sourceAccount == ''):
                    return item.SourceTitle
        return None
        

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
        elm = Element('sources')
        if self._DeviceId and len(self._DeviceId) > 0: elm.set('deviceID', str(self._DeviceId))
        
        item:SourceItem
        for item in self._SourceItems:
            elm.append(item.ToElement())
        return elm


    def ToSourceArray(self, includeSourceAccount:bool=False) -> list[str]:
        """
        Returns an array of source names (and optionally source account) strings.
        
        Args:
            includeSourceAccount (bool):
                True to include SourceAccount property values if present;
                otherwise, False to only return Source property values.
        
        If includeSourceAccount=True was specified and a SourceAccount value is present, 
        then it will return the Source entry as "Source:sourceAccount" as well as a 
        second entry of just the "Source" value; otherwise, just the "Source" value is 
        returned for the source item.
        """
        sourceList:list[str] = []
        
        # load list of supported sources.
        item:SourceItem
        for item in self._SourceItems:
            if (item.Source is not None) and (len(item.Source) > 0):
                if (includeSourceAccount == False):
                    sourceList.append(item.Source)
                elif (item.SourceAccount is not None) and (len(item.SourceAccount) > 0):
                    sourceList.append("%s:%s" % (item.Source, item.SourceAccount))
                else:
                    sourceList.append(item.Source)
                        
        return sourceList

        
    def ToSourceTitleArray(self) -> list[str]:
        """
        Returns an array of source title strings.
        """
        result:list[str] = []
        
        # load list of supported sources.
        item:SourceItem
        for item in self._SourceItems:
            result.append(item.SourceTitle)
                        
        return result

        
    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'SourceList:'
        if self._DeviceId is not None: msg = '%s DeviceId="%s"' % (msg, self._DeviceId)
        msg = "%s (%d items)" % (msg, len(self._SourceItems))
        
        if includeItems == True:
            item:SourceItem
            for item in self._SourceItems:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
