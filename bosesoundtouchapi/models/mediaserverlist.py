# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export
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
        self._MediaServers:list[MediaServer] = []
        
        if (root is None):

            pass

        else:

            # base fields.
            for mediaServer in root.findall('media_server'):
                self._MediaServers.append(MediaServer(mediaServer))

            # sort items on FriendlyName property, ascending order.
            if len(self._MediaServers) > 0:
                self._MediaServers.sort(key=lambda x: (x.FriendlyName or "").lower(), reverse=False)


    def __getitem__(self, key) -> MediaServer:
        return self._MediaServers[key]


    def __iter__(self) -> Iterator:
        return iter(self._MediaServers)


    def __len__(self) -> int:
        return len(self._MediaServers)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def MediaServers(self) -> list[MediaServer]:
        """ 
        The list of `MediaServer` items. 
        """
        return self._MediaServers


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'MediaServerList:'
        msg = "%s (%d items)" % (msg, len(self._MediaServers))
        
        if includeItems == True:
            item:MediaServer
            for item in self._MediaServers:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
