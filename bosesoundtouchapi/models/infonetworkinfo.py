# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind

@export
class InformationNetworkInfo:
    """
    SoundTouch device Information NetworkInfo configuration object.
       
    This class contains the attributes and sub-items that represent the 
    Information NetworkInfo configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._IpAddress:str = None
        self._MacAddress:str = None
        self._TypeValue:str = None
        
        if (root is None):
            
            pass
        
        else:

            self._IpAddress = _xmlFind(root, 'ipAddress')
            self._MacAddress = _xmlFind(root, 'macAddress')
            self._TypeValue = root.get('type')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def MacAddress(self) -> str:
        """ MAC address (media access control address) assigned to the adapter. """
        return self._MacAddress


    @property
    def IpAddress(self) -> str:
        """ IPV4 address assigned by the network. """
        return self._IpAddress


    @property
    def TypeValue(self) -> str:
        """ Network interface adapter type (e.g. WIFI, ETHERNET). """
        return self._TypeValue


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'NetworkInfo:'
        if self._MacAddress is not None and len(self._MacAddress) > 0: msg = '%s macAddress="%s"' % (msg, str(self._MacAddress))
        if self._IpAddress is not None and len(self._IpAddress) > 0: msg = '%s ipAddress="%s"' % (msg, str(self._IpAddress))
        if self._TypeValue is not None and len(self._TypeValue) > 0: msg = '%s type="%s"' % (msg, str(self._TypeValue))
        return msg 
    