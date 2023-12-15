# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export
from .supportedurl import SupportedUrl

@export
class SupportedUrls:
    """
    SoundTouch device SupportedUrls configuration object.
       
    This class contains the attributes and sub-items that represent the
    supported url's configuration of the device.
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
        self._Urls:list[str] = []
        
        if (root is None):
            
            pass
        
        else:

            self._DeviceId = root.get('deviceID')
            
            for item in root.findall('URL'):
                self._Urls.append(SupportedUrl(root=item))
                
            # sort items on URL property, descending order.
            if len(self._Urls) > 0:
                self._Urls.sort(key=lambda x: (x.Location or "").lower(), reverse=False)


    def __getitem__(self, key) -> SupportedUrl:
        if isinstance(key, str):
            for item in self._Urls:
                if item.Source == key:
                    return item
        else:
            return self._Urls[key]


    def __iter__(self) -> Iterator:
        return iter(self._Urls)


    def __len__(self) -> int:
        return len(self._Urls)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId

    
    @property
    def Urls(self) -> list[SupportedUrl]:
        """ 
        The list of `SupportedUrl` items. 
        """
        return self._Urls

            
    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'SupportedUrls:'
        if self._DeviceId is not None: msg = '%s DeviceId="%s"' % (msg, self._DeviceId)
        msg = "%s (%d items)" % (msg, len(self._Urls))
        
        if includeItems == True:
            item:SupportedUrl
            for item in self._Urls:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
