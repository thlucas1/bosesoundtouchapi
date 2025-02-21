# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind

@export
class WirelessProfile:
    """
    SoundTouch device WirelessProfile configuration object.
       
    This class contains the attributes and sub-items that represent the
    wireless profile configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Ssid:str = None

        if (root is None):

            pass

        else:

            self._Ssid = _xmlFind(root, 'ssid')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Ssid(self) -> str:
        """ The network service set identifier (SSID) the device is connected to. """       
        return self._Ssid


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'ssid': self._Ssid,
        }
        return result
        

    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'WirelessProfile:'
        if self._Ssid and len(self._Ssid) > 0: msg = '%s ssid="%s"' % (msg, str(self._Ssid))
        return msg
