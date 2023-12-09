# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export

@export
class BlueToothInfo:
    """
    SoundTouch device BlueToothInfo configuration object.
       
    This class contains the attributes and sub-items that represent the 
    BlueToothInfo configuration of the device.      
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._MacAddress:str = None

        if (root is None):
            
            pass
        
        elif root.tag == 'BluetoothInfo':

            self._MacAddress = root.get('BluetoothMACAddress')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def MacAddress(self) -> str:
        """ MAC address (media access control address) assigned to the bluetooth adapter. """
        return self._MacAddress


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'BlueToothInfo:'
        msg = '%s MacAddress="%s"' % (msg, str(self._MacAddress))
        return msg 
