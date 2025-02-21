# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export

@export
class ProductHdmiAssignmentControls:
    """
    SoundTouch device ProductHdmiAssignmentControls configuration object.
       
    This class contains the attributes and sub-items that represent the 
    Product HDMI Assignment Controls configuration of the device.      
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
        self._HdmiInputSelection01:str = None

        if (root is None):

            pass

        elif root.tag == 'producthdmiassignmentcontrols':

            # base fields.
            self._HdmiInputSelection01 = root.get('hdmiinputselection_01')

    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def HdmiInputSelection01(self) -> str:
        """ The HDMI input selection 1 value. """
        return self._HdmiInputSelection01


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'hdmi_input_selection_01': self._HdmiInputSelection01,
        }
        return result
        

    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'ProductHdmiAssignmentControls:'
        msg = '%s HdmiInputSelection01="%s"' % (msg, str(self._HdmiInputSelection01))
        return msg 
