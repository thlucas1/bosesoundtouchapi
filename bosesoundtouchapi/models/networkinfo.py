# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlGetAttrInt
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
        self._Interfaces:list[NetworkInfoInterface] = []
        self._WifiProfileCount:int = None

        if (root is None):

            pass

        else:

            self._WifiProfileCount = _xmlGetAttrInt(root, 'wifiProfileCount')
            
            for interface in root.find('interfaces'):
                self._Interfaces.append(NetworkInfoInterface(interface))


    def __getitem__(self, key) -> NetworkInfoInterface:
        return self._Interfaces[key]


    def __iter__(self) -> Iterator:
        return iter(self._Interfaces)


    def __len__(self):
        return len(self._Interfaces)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def InterfaceCount(self) -> int:
        """ 
        Total number of network interfaces defined, including both
        wired and wireless. 
        """
        return len(self._Interfaces)


    @property
    def WifiProfileCount(self) -> int:
        """ Number of wireless (wifi) network interfaces defined. """
        return self._WifiProfileCount


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'interface_count': self.InterfaceCount,
            'wifi_profile_count': self._WifiProfileCount,
            'interfaces': [ item.ToDictionary() for item in self._Interfaces ],
        }
        return result
        

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
        msg = "%s (%d items)" % (msg, len(self._Interfaces))
        
        if includeItems == True:
            item:NetworkInfoInterface
            for item in self._Interfaces:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
