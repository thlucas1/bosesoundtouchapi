# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindInt
from ..soundtouchmodelrequest import SoundTouchModelRequest
from .usertrackcontroltypes import UserTrackControlTypes

@export
class UserTrackControl(SoundTouchModelRequest):
    """
    SoundTouch device UserTrackControl configuration object.
       
    This class contains the attributes and sub-items that represent the 
    UserTrackControl configuration of the device.      
    """

    def __init__(self, trackControl:UserTrackControlTypes=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            trackControl (str):
                User track control value to set.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._TrackControl:str = None

        if (root is None):
            
            if isinstance(trackControl, UserTrackControlTypes):
                trackControl = trackControl.value
                
            self._TrackControl = trackControl

        else:

            self._TrackControl = root.text


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def TrackControl(self) -> str:
        """ User TrackControl value. """
        return self._TrackControl

    
    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('TrackControl')
        if isRequestBody == True:
    
            if self._TrackControl is not None:
                elm.text = self._TrackControl
            
        else:
            
            if self._TrackControl and len(self._TrackControl) > 0: elm.text = self._TrackControl
                
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'TrackControl:'
        if self._TrackControl is not None: msg = '%s %s' % (msg, self._TrackControl)
        return msg 
    