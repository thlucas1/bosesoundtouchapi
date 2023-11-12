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
class AudioProductToneControls(SoundTouchModelRequest):
    """
    SoundTouch device AudioProductToneControls configuration object.
       
    This class contains the attributes and sub-items that represent the 
    Audio Product Tone Controls configuration of the device.      
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
        self._Bass:ControlLevelInfo = None
        self._Treble:ControlLevelInfo = None
        
        if (root is None):
        
            # create empty control objects.
            self._Bass:ControlLevelInfo = ControlLevelInfo('bass')
            self._Bass.Value = 0
            self._Treble:ControlLevelInfo = ControlLevelInfo('treble')
            self._Treble.Value = 0
        
        else:

            # base fields.
            elmBass:Element = root.find('bass')
            self._Bass = ControlLevelInfo(root=elmBass)
            elmTreble:Element = root.find('treble')
            self._Treble = ControlLevelInfo(root=elmTreble)
            

    def __repr__(self) -> str:
        return self.ToString()


    @property
    def Bass(self) -> ControlLevelInfo:
        """ Audio product tone control settings for bass details. """
        return self._Bass


    @property
    def Treble(self) -> ControlLevelInfo:
        """ Audio product tone control settings for treble details. """
        return self._Treble


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('audioproducttonecontrols')
        elm.append(self._Bass.ToElement(isRequestBody))
        elm.append(self._Treble.ToElement(isRequestBody))
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'AudioProductToneControls:'
        msg = '%s\n  %s' % (msg, self._Bass.ToString())
        msg = '%s\n  %s' % (msg, self._Treble.ToString())
        return msg 


    def ToXmlRequestBody(self, encoding:str='utf-8') -> str:
        """ 
        Overridden.
        Returns a POST request body for changing the audio tone control value. 
        
        Returns:
            An xml string that can be used in a POST request to update the
            device configuration.
        """
        elm = self.ToElement(True)
        xml = tostring(elm, encoding='unicode')
        return xml
