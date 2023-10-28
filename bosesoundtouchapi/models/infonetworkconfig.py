# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind

@export
class InfoNetworkConfig:
    """
    SoundTouch device InfoNetworkConfig configuration object.
       
    This class contains the attributes and sub-items that represent the 
    net connected interfaces configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        if (root is None):
            pass  # no other parms to process.
        else:

            # base fields.
            self._type_item = root.get('type')
            self._mac_address = _xmlFind(root, 'macAddress')
            self._ip_address = _xmlFind(root, 'ipAddress')


    def __repr__(self) -> str:
        return self.toString()


    @property
    def mac_address(self) -> str:
        """The device's mac address."""
        return self._mac_address


    @property
    def type_item(self) -> str:
        """The adapter type (WIFI or ETHERNET)."""
        return self._type_item


    @property
    def ip_address(self) -> str:
        """The mapped ip address."""
        return self._ip_address


    def toString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'InfoNetworkConfig:'
        if self._mac_address and len(self._mac_address) > 0: msg = '%s macAddress="%s"' % (msg, str(self._mac_address))
        if self._ip_address and len(self._ip_address) > 0: msg = '%s ipAddress="%s"' % (msg, str(self._ip_address))
        if self._type_item and len(self._type_item) > 0: msg = '%s type="%s"' % (msg, str(self._type_item))
        return msg 
    