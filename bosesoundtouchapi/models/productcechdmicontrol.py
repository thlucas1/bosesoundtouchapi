# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export

@export
class ProductCecHdmiControl:
    """
    SoundTouch device ProductCecHdmiControl configuration object.
       
    This class contains the attributes and sub-items that represent the 
    Product CEC HDMI Control configuration of the device.      
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        # initialize storage.
        self._CecMode:str = None

        if (root is None):
            
            pass  # no other parms to process.
        
        elif root.tag == 'productcechdmicontrol':

            # base fields.
            self._CecMode = root.get('cecmode', default=None)


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def CecMode(self) -> str:
        """ The HDMI CEC mode value. """
        return self._CecMode


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'ProductCecHdmiControl:'
        msg = '%s CecMode="%s"' % (msg, str(self._CecMode))
        return msg 
