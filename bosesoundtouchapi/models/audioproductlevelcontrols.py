# external package imports.
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export
from ..soundtouchmodelrequest import SoundTouchModelRequest
from .controllevelinfo import ControlLevelInfo

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SISession
_logsi:SISession = SIAuto.Si.GetSession(__package__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__package__, True)
_logsi.SystemLogger = logging.getLogger(__package__)


@export
class AudioProductLevelControls(SoundTouchModelRequest):
    """
    SoundTouch device AudioProductLevelControls configuration object.
       
    This class contains the attributes and sub-items that represent the 
    Audio Product Level Controls configuration of the device.      
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
        self._FrontCenterSpeakerLevel:ControlLevelInfo = None
        self._RearSurroundSpeakersLevel:ControlLevelInfo = None
        
        if (root is None):
        
            # create empty control objects.
            self._FrontCenterSpeakerLevel:ControlLevelInfo = ControlLevelInfo('frontCenterSpeakerLevel')
            self._FrontCenterSpeakerLevel.Value = 0
            self._RearSurroundSpeakersLevel:ControlLevelInfo = ControlLevelInfo('rearSurroundSpeakersLevel')
            self._RearSurroundSpeakersLevel.Value = 0
        
        else:

            # base fields.
            elmFrontCenterSpkr:Element = root.find('frontCenterSpeakerLevel')
            self._FrontCenterSpeakerLevel = ControlLevelInfo(root=elmFrontCenterSpkr)
            elmRearSurroundSpkr:Element = root.find('rearSurroundSpeakersLevel')
            self._RearSurroundSpeakersLevel = ControlLevelInfo(root=elmRearSurroundSpkr)
            

    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def FrontCenterSpeakerLevel(self) -> ControlLevelInfo:
        """ Audio product level control settings for front center speaker level details. """
        return self._FrontCenterSpeakerLevel


    @property
    def RearSurroundSpeakersLevel(self) -> ControlLevelInfo:
        """ Audio product level control settings for rear surround speaker level details. """
        return self._RearSurroundSpeakersLevel


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('audioproductlevelcontrols')
        elm.append(self._FrontCenterSpeakerLevel.ToElement(isRequestBody))
        elm.append(self._RearSurroundSpeakersLevel.ToElement(isRequestBody))
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'AudioProductLevelControls:'
        msg = '%s\n  %s' % (msg, self._FrontCenterSpeakerLevel.ToString())
        msg = '%s\n  %s' % (msg, self._RearSurroundSpeakersLevel.ToString())
        return msg 
