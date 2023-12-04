# external package imports.
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtouchhdmicecmodes import SoundTouchHdmiCecModes

@export
class ProductCecHdmiControl(SoundTouchModelRequest):
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

            pass

        elif root.tag == 'productcechdmicontrol':

            # base fields.
            self._CecMode = root.get('cecmode', default=None)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def CecMode(self) -> str:
        """ 
        The HDMI CEC mode value.
       
        See `SoundTouchProductCecHdmiModes` for more information.
        """
        return self._CecMode
    
    @CecMode.setter
    def CecMode(self, value:str):
        """ 
        Sets the CecMode property value.
        """
        if value != None:
            if isinstance(value, SoundTouchHdmiCecModes):
                self._CecMode = value.value
            elif isinstance(value, str):
                self._CecMode = value


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('productcechdmicontrol')
        
        if self._CecMode is not None and len(self._CecMode) > 0: elm.set('cecmode', self._CecMode)
        if isRequestBody == True:
            return elm

        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'ProductCecHdmiControl:'
        msg = '%s CecMode="%s"' % (msg, str(self._CecMode))
        return msg 
