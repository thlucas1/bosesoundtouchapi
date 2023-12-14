# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindInt
from ..soundtouchmodelrequest import SoundTouchModelRequest
from .userplaycontroltypes import UserPlayControlTypes

@export
class UserPlayControl(SoundTouchModelRequest):
    """
    SoundTouch device UserPlayControl configuration object.
       
    This class contains the attributes and sub-items that represent the 
    UserPlayControl configuration of the device.      
    """

    def __init__(self, playControl:UserPlayControlTypes=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            playControl (str):
                User PlayControl value to set.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._PlayControl:str = None

        if (root is None):
            
            if isinstance(playControl, UserPlayControlTypes):
                playControl = playControl.value
                
            self._PlayControl = playControl

        else:

            self._PlayControl = root.text


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def PlayControl(self) -> str:
        """ User PlayControl value. """
        return self._PlayControl

    
    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('PlayControl')
        if isRequestBody == True:
    
            if self._PlayControl is not None:
                elm.text = self._PlayControl
            
        else:
            
            if self._PlayControl and len(self._PlayControl) > 0: elm.text = self._PlayControl
                
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'PlayControl:'
        if self._PlayControl is not None: msg = '%s %s' % (msg, self._PlayControl)
        return msg 
    