# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind

@export
class BassCapabilities:
    """
    SoundTouch device BassCapabilities configuration object.
       
    This class contains the attributes and sub-items that represent the 
    bass capabilities configuration of the device.      
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Default:int = None
        self._IsAvailable:bool = None
        self._Maximum:int = None
        self._Minimum:int = None

        if (root is None):
            
            pass
        
        else:

            self._Default = int(_xmlFind(root, 'bassDefault', default=0))
            self._IsAvailable = _xmlFind(root, 'bassAvailable', default='false') == 'true'
            self._Maximum = int(_xmlFind(root, 'bassMax', default=0))
            self._Minimum = int(_xmlFind(root, 'bassMin', default=0))


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Default(self) -> int:
        """ The default value of the bass level. """
        return self._Default


    @property
    def IsAvailable(self) -> bool:
        """ Returns whether bass capabilities are enabled on the device. """
        return self._IsAvailable


    @property
    def Maximum(self) -> int:
        """ The maximum allowed value of the bass level. """
        return self._Maximum


    @property
    def Minimum(self) -> int:
        """ The minimum allowed value of the bass level. """
        return self._Minimum


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'BassCapabilities:'
        msg = '%s available=%s' % (msg, str(self._IsAvailable).lower())
        msg = '%s min=%d' % (msg, self._Minimum)
        msg = '%s max=%d' % (msg, self._Maximum)
        msg = '%s default=%d' % (msg, self._Default)
        return msg 
