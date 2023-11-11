# external package imports.
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export
from ..soundtouchmodelrequest import SoundTouchModelRequest
from .audioproducttonecontrol import AudioProductToneControl

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
        self._Bass:AudioProductToneControl = None
        self._Treble:AudioProductToneControl = None
        
        if (root is None):
        
            # create empty control objects.
            self._Bass:AudioProductToneControl = AudioProductToneControl('bass')
            self._Bass.Value = 0
            self._Treble:AudioProductToneControl = AudioProductToneControl('treble')
            self._Treble.Value = 0
        
        else:

            # base fields.
            elmBass:Element = root.find('bass')
            self._Bass = AudioProductToneControl(root=elmBass)
            elmTreble:Element = root.find('treble')
            self._Treble = AudioProductToneControl(root=elmTreble)
            

    def __repr__(self) -> str:
        return self.ToString()


    @property
    def Bass(self) -> AudioProductToneControl:
        """ Audio product tone control settings for bass details. """
        return self._Bass


    @property
    def Treble(self) -> AudioProductToneControl:
        """ Audio product tone control settings for treble details. """
        return self._Treble


    def ToElement(self) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 
        """
        elm = Element('audioproducttonecontrols')
        elm.append(self._Bass.ToElement())
        elm.append(self._Treble.ToElement())
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
        elm = self.ToElement()
        xml = tostring(elm, encoding='unicode')
        return xml
