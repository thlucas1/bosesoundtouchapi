# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr
from .networkinfointerface import NetworkInfoInterface

@export
class NetworkInfo:
    """
    SoundTouch device NetworkInfo configuration object.
       
    This class contains the attributes and sub-items that represent the
    network information configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._interfaces = []

        if (root is None):
            pass  # no other parms to process.
        else:

            # base fields.
            self._WifiProfileCount:int = int(root.get('wifiProfileCount', default='0'))
            
            for interface in root.find('interfaces'):
                self.append(NetworkInfoInterface(interface))


    def __getitem__(self, key) -> NetworkInfoInterface:
        return self._interfaces[key]


    def __iter__(self) -> Iterator:
        return iter(self._interfaces)


    def __len__(self):
        return len(self._interfaces)


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def InterfaceCount(self) -> int:
        """ 
        The total number of network interfaces defined, including both
        wired and wireless. 
        """
        return len(self._interfaces)


    @property
    def WifiProfileCount(self) -> int:
        """ The number of wireless (wifi) network interfaces defined. """
        return self._WifiProfileCount


    def append(self, value:NetworkInfoInterface):
        """
        Append a new `NetworkInfoInterface` item to the list.
        
        Args:
            value:
                The `NetworkInfoInterface` object to append.
        """
        self._interfaces.append(value)


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'NetworkInfo:'
        msg = '%s wifiProfileCount=%d' % (msg, self._WifiProfileCount)
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            item:NetworkInfoInterface
            for item in self:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
