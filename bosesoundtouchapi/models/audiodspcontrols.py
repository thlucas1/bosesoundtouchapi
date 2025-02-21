# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlGetAttrInt
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtoucherror import SoundTouchError
from .audiodspaudiomodes import AudioDspAudioModes

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

    def __init__(self, audioMode:AudioDspAudioModes=None, videoSyncAudioDelay:int=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            audioMode (AudioDspAudioModes|str):
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
            self._AudioMode = root.get('audiomode')
            self._SupportedAudioModes = root.get('supportedaudiomodes')
            self._VideoSyncAudioDelay = _xmlGetAttrInt(root, 'videosyncaudiodelay')
            

    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def AudioMode(self) -> str:
        """ Audio mode value (e.g. "AUDIO_MODE_NORMAL", "AUDIO_MODE_DIALOG", etc). """
        return self._AudioMode

    @AudioMode.setter
    def AudioMode(self, value:str):
        """ 
        Sets the AudioMode property value.
        """
        if value != None:
            if isinstance(value, AudioDspAudioModes):
                self._AudioMode = value.value
            elif isinstance(value, str):
                self._AudioMode = value


    @property
    def SupportedAudioModes(self) -> str:
        """ Supported audio modes (e.g. "AUDIO_MODE_NORMAL|AUDIO_MODE_DIALOG", etc). """
        return self._SupportedAudioModes


    @property
    def VideoSyncAudioDelay(self) -> int:
        """ Video syncronization audio delay value. """
        return self._VideoSyncAudioDelay

    @VideoSyncAudioDelay.setter
    def VideoSyncAudioDelay(self, value:int):
        """ 
        Sets the VideoSyncAudioDelay property value.
        """
        if value != None:
            if isinstance(value, int):
                self._VideoSyncAudioDelay = value


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'audio_mode': self._AudioMode,
            'supported_audio_modes': self._SupportedAudioModes,
            'video_sync_audio_delay': self._VideoSyncAudioDelay,
        }
        return result
        

    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
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
        if self._AudioMode is not None: msg = '%s AudioMode="%s"' % (msg, str(self._AudioMode))
        if self._SupportedAudioModes is not None: msg = '%s SupportedAudioModes="%s"' % (msg, str(self._SupportedAudioModes))
        if self._VideoSyncAudioDelay is not None: msg = '%s VideoSyncAudioDelay=%s' % (msg, str(self._VideoSyncAudioDelay))
        return msg 


    def ToSupportedAudioModesArray(self) -> list[str]:
        """
        Returns a string array of SupportedAudioModes.
        
        An empty list object is returned if the SupportedAudioModes property is None or empty;
        otherwise, a list of the supported audio modes is returned.
        """
        # build list of supported audio modes, and sort the values.
        modesList:list[str] = []
        if self._SupportedAudioModes is not None:
            modesList = self._SupportedAudioModes.split('|')
            modesList.sort()
        return modesList


    def ToSupportedAudioModeTitlesArray(self) -> list[str]:
        """
        Returns a string array of titles for SupportedAudioModes.
        """
        # build list of supported audio mode titles; results are already sorted by enum name.
        result:list[str] = []
        if self._SupportedAudioModes is not None:
            modes:list[str] = self._SupportedAudioModes.split('|')
            mode:str
            enum:AudioDspAudioModes
            for enum in AudioDspAudioModes:
                for mode in modes:
                    if enum.value == mode:
                        result.append(enum.name)
        return result
       