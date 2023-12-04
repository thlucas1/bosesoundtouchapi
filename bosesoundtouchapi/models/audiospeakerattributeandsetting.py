# external package imports.
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export
from ..soundtouchmodelrequest import SoundTouchModelRequest
from .speakerattributeandsetting import SpeakerAttributeAndSetting

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SISession
_logsi:SISession = SIAuto.Si.GetSession(__package__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__package__, True)
_logsi.SystemLogger = logging.getLogger(__package__)


@export
class AudioSpeakerAttributeAndSetting(SoundTouchModelRequest):
    """
    SoundTouch device AudioSpeakerAttributeAndSetting configuration object.
       
    This class contains the attributes and sub-items that represent the 
    Audio Speaker Attribute And Setting configuration of the device.      
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        # create empty control objects.
        self._Rear:SpeakerAttributeAndSetting = SpeakerAttributeAndSetting('rear')
        self._SubWoofer01:SpeakerAttributeAndSetting = SpeakerAttributeAndSetting('subwoofer01')
        self._SubWoofer02:SpeakerAttributeAndSetting = SpeakerAttributeAndSetting('subwoofer02')
                
        if (root is None):
        
            pass
        
        else:

            elmRear:Element = root.find('rear')
            if (elmRear is not None):
                self._Rear = SpeakerAttributeAndSetting(root=elmRear)
            elmSubWoofer01:Element = root.find('subwoofer01')
            if (elmSubWoofer01 is not None):
                self._SubWoofer01 = SpeakerAttributeAndSetting(root=elmSubWoofer01)
            elmSubWoofer02:Element = root.find('subwoofer02')
            if (elmSubWoofer02 is not None):
                self._SubWoofer02 = SpeakerAttributeAndSetting(root=elmSubWoofer02)
            

    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Rear(self) -> SpeakerAttributeAndSetting:
        """ Speaker attributes and settings for a rear speaker. """
        return self._Rear


    @property
    def SubWoofer01(self) -> SpeakerAttributeAndSetting:
        """ Speaker attributes and settings for subwoofer 01 speaker. """
        return self._SubWoofer01


    @property
    def SubWoofer02(self) -> SpeakerAttributeAndSetting:
        """ Speaker attributes and settings for subwoofer 02 speaker. """
        return self._SubWoofer02


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('audiospeakerattributeandsetting')
        if (self._Rear is not None) and (self._Rear.IsAnyPropertySet == True):
            elm.append(self._Rear.ToElement(isRequestBody))
        if (self._SubWoofer01 is not None) and (self._SubWoofer01.IsAnyPropertySet == True):
            elm.append(self._SubWoofer01.ToElement(isRequestBody))
        if (self._SubWoofer02 is not None) and (self._SubWoofer02.IsAnyPropertySet == True):
            elm.append(self._SubWoofer02.ToElement(isRequestBody))
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'AudioSpeakerAttributeAndSetting:'
        if (self._Rear is not None) and (self._Rear.IsAnyPropertySet == True):
            msg = '%s\n  %s' % (msg, self._Rear.ToString())
        if (self._SubWoofer01 is not None) and (self._SubWoofer01.IsAnyPropertySet == True):
            msg = '%s\n  %s' % (msg, self._SubWoofer01.ToString())
        if (self._SubWoofer02 is not None) and (self._SubWoofer02.IsAnyPropertySet == True):
            msg = '%s\n  %s' % (msg, self._SubWoofer02.ToString())
        return msg 
