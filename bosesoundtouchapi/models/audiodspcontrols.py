# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtoucherror import SoundTouchError

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SISession
_logsi:SISession = SIAuto.Si.GetSession(__package__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__package__, True)
_logsi.SystemLogger = logging.getLogger(__package__)


@export
class AudioDspControls(SoundTouchModelRequest):
    """
    SoundTouch device AudioDspControls configuration object.
       
    This class contains the attributes and sub-items that represent the 
    Audio DSP Controls configuration of the device.      
    """

    def __init__(self, audioMode:str=None, videoSyncAudioDelay:int=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            audioMode (str):
                Audio mode value (e.g. "AUDIO_MODE_NORMAL", "AUDIO_MODE_DIALOG", etc).
            videoSyncAudioDelay (int):
                Video syncronization audio delay value.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchError:
                videoSyncAudioDelay argument was not of type int.  
        """
        # initialize storage.
        self._AudioMode:str = None
        self._SupportedAudioModes:str = None
        self._VideoSyncAudioDelay:int = None
        
        if (root is None):
            
            # validations.
            if videoSyncAudioDelay is not None:
                if not isinstance(videoSyncAudioDelay, int):
                    raise SoundTouchError('videoSyncAudioDelay argument was not of type int', logsi=_logsi)

            # base fields.
            self._AudioMode = audioMode
            self._VideoSyncAudioDelay = videoSyncAudioDelay
        
        elif root.tag == 'audiodspcontrols':

            # base fields.
            self._AudioMode = root.get('audiomode', default=None)
            self._SupportedAudioModes = root.get('supportedaudiomodes', default=None)
            self._VideoSyncAudioDelay = int(root.get('videosyncaudiodelay', default=0))


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def AudioMode(self) -> str:
        """ Audio mode value (e.g. "AUDIO_MODE_NORMAL", "AUDIO_MODE_DIALOG", etc). """
        return self._AudioMode


    @property
    def SupportedAudioModes(self) -> str:
        """ Supported audio modes (e.g. "AUDIO_MODE_NORMAL|AUDIO_MODE_DIALOG", etc). """
        return self._SupportedAudioModes


    @property
    def VideoSyncAudioDelay(self) -> int:
        """ Video syncronization audio delay value. """
        return self._VideoSyncAudioDelay


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('audiodspcontrols')
        
        if self._AudioMode is not None and len(self._AudioMode) > 0: elm.set('audiomode', self._AudioMode)
        if self._VideoSyncAudioDelay is not None: elm.set('videosyncaudiodelay', str(self._VideoSyncAudioDelay))
        if isRequestBody == True:
            return elm

        if self._SupportedAudioModes is not None and len(self._SupportedAudioModes) > 0: elm.set('supportedaudiomodes', self._SupportedAudioModes)
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'AudioDspControls:'
        msg = '%s AudioMode="%s"' % (msg, str(self._AudioMode))
        msg = '%s SupportedAudioModes="%s"' % (msg, str(self._SupportedAudioModes))
        msg = '%s VideoSyncAudioDelay=%s' % (msg, str(self._VideoSyncAudioDelay))
        return msg 


    def ToSupportedAudioModesArray(self) -> list[str]:
        """
        Returns a string array of SupportedAudioModes.
        
        An empty list object is returned if the SupportedAudioModes property is None or empty;
        otherwise, a list of the supported audio modes is returned.
        """
        # if supported audio modes is not set then we are done.
        if self._SupportedAudioModes is None:
            return []
        
        # load list of supported audio modes.
        modesList:list[str] = self._SupportedAudioModes.split('|')
        return modesList


    def ToXmlRequestBody(self, encoding:str='utf-8') -> str:
        """ 
        Overridden.
        Returns a POST request body, which is used to update the device configuration.
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.

        Returns:
            An xml string that can be used in a POST request to update the
            device configuration.
        """
        elm = self.ToElement(True)
        xml = tostring(elm, encoding='unicode')
        return xml
