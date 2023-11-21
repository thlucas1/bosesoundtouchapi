# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind

@export
class SystemTimeout:
    """
    SoundTouch device SystemTimeout configuration object.
       
    This class contains the attributes and sub-items that represent the
    system timeout configuration of the device.
    """
    
    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._IsPowersavingEnabled:bool = None
        
        if (root is None):

            pass

        else:

            self._IsPowersavingEnabled = bool(_xmlFind(root, 'powersaving_enabled', default='false') == 'true')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def IsPowersavingEnabled(self) -> bool:
        """ True if power saving is enabled on the device; otherwise, False. """
        return self._IsPowersavingEnabled


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SystemTimeout:'
        msg = '%s powersavingEnabled=%s' % (msg, str(self._IsPowersavingEnabled).lower())
        return msg 
