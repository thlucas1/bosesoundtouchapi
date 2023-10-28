# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr
from .mediaserver import MediaServer

@export
class MediaServerList:
    """
    SoundTouch device MediaServerList configuration object.
       
    This class contains the attributes and sub-items that represent the
    UPnP media server configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._servers = []
        
        if (root is None):
            pass  # no other parms to process.
        else:

            # base fields.
            for server in root.findall('media_server'):
                self.append(MediaServer(server))


    def __getitem__(self, key) -> MediaServer:
        return self._servers[key]


    def __iter__(self) -> Iterator:
        return iter(self._servers)


    def __len__(self) -> int:
        return len(self._servers)


    def __repr__(self) -> str:
        return self.ToString()


    def append(self, value: MediaServer):
        """
        Append a new `MediaServer` item to the list.
        
        Args:
            value:
                The `MediaServer` object to append.
        """
        self._servers.append(value)


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'MediaServerList:'
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            item:MediaServer
            for item in self:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
