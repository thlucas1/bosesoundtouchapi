# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlGetAttrInt
from ..soundtouchmodelrequest import SoundTouchModelRequest
from .usertrackcontroltypes import UserTrackControlTypes

@export
class UserTrackControl(SoundTouchModelRequest):
    """
    SoundTouch device UserTrackControl configuration object.
       
    This class contains the attributes and sub-items that represent the 
    UserTrackControl configuration of the device.      
    """

    def __init__(self, trackControl:UserTrackControlTypes=None, startSecond:int=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            trackControl (str):
                User track control value to set.
            startSecond (int):
                Starting position (in seconds) of where to start playing the media content.
                This argument is only valid for UserTrackControlTypes.SEEK_TO_TIME requests.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._StartSecond:int = None
        self._TrackControl:str = None

        if (root is None):
            
            if startSecond is not None and (not isinstance(startSecond, int) or startSecond < 1):
                startSecond = 0
                
            if isinstance(trackControl, UserTrackControlTypes):
                trackControl = trackControl.value
            
            self._StartSecond = startSecond
            self._TrackControl = trackControl

        else:

            self._StartSecond = _xmlGetAttrInt(root,'startSecond', None)
            self._TrackControl = root.text


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def TrackControl(self) -> str:
        """ User track control value (e.g. "NEXT_TRACK", "SEEK_TO_TIME", etc). """
        return self._TrackControl

    @TrackControl.setter
    def TrackControl(self, value:str):
        """ Sets the TrackControl property value. """
        if value != None:
            if isinstance(value, UserTrackControlTypes):
                self._TrackControl = value.value
            elif isinstance(value, str):
                self._TrackControl = value

    
    @property
    def StartSecond(self) -> int:
        """ Starting position (in seconds) of where to start playing the media content. """
        return self._StartSecond

    @StartSecond.setter
    def StartSecond(self, value:str):
        """ Sets the StartSecond property value. """
        if isinstance(value, int) and value > 0:
            self._StartSecond = value

    
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

                if self._TrackControl == UserTrackControlTypes.SeekToTime.value:
                    if self._StartSecond is not None: elm.set('startSecond', str(self._StartSecond))
            
        else:
            
            if self._StartSecond is not None: elm.set('startSecond', str(self._StartSecond))
            if self._TrackControl is not None and len(self._TrackControl) > 0: elm.text = self._TrackControl
                
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'TrackControl:'
        if self._StartSecond is not None: msg = '%s StartSecond=%s' % (msg, str(self._StartSecond))
        if self._TrackControl is not None: msg = '%s TrackControl="%s"' % (msg, self._TrackControl)
        return msg 
    