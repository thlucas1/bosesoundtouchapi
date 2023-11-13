# external package imports.
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..bstconst import (
    BOSE_DEVELOPER_APPKEY,
)

@export
class PlayInfo(SoundTouchModelRequest):
    """
    SoundTouch device PlayInfo configuration object.
       
    This class contains the attributes and sub-items that represent a
    play info configuration of the device.
    """

    def __init__(self, url:str=None, service:str=None, message:str=None, reason:str=None, volume:int=30, appKey:str=None, 
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            url (str):
                The URL to be played.
            service (str):
                The service text that will appear in the NowPlaying Artist node.
            message (str):
                The message text that will appear in the NowPlaying Album node.
            reason (str):
                The reason text that will appear in the NowPlaying Track node.
            volume (int):
                The volume level (0-100) to set for the notification.
            appKey (str):
                Bose Developer API application key.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        if (root is None):
            
            if appKey is None:
                appKey = BOSE_DEVELOPER_APPKEY
            if service is None:
                service = "Unknown"
            if (volume is None) or (not isinstance(volume, int)) or (volume < 0) or (volume > 100):
                volume = int(30)

            self._AppKey:str = appKey
            self._Service:str = service
            self._Message:str = message
            self._Reason:str = reason
            self._Url:str = url
            self._Volume:int = int(volume)
            
        else:

            self._AppKey:str = _xmlFind(root, 'app_key')
            self._Service:str = _xmlFind(root, 'service')
            self._Message:str = _xmlFind(root, 'message')
            self._Reason:str = _xmlFind(root, 'reason')
            self._Url:str = _xmlFind(root, 'url')
            self._Volume:int = int(_xmlFind(root, 'volume', default=0))

        
    def __repr__(self) -> str:
        return self.ToString()


    @property
    def AppKey(self) -> str:
        """ Bose Developer API application key. """
        return self._AppKey


    @property
    def Service(self) -> str:
        """ The service text that will appear in the NowPlaying Artist node. """
        return self._Service


    @property
    def Message(self) -> str:
        """ The message text that will appear in the NowPlaying Album node. """
        return self._Message


    @property
    def Reason(self) -> str:
        """ The reason text that will appear in the NowPlaying Track node. """
        return self._Reason


    @property
    def Url(self) -> str:
        """ The URL to be played. """
        return self._Url


    @property
    def Volume(self) -> int:
        """ 
        The volume level (0-100) to set for the notification.  
        Specify a value of 0 to play the notification at the current volume level.
        """
        return self._Volume


    def ToElement(self) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 
        """
        elm = Element('play_info')
        
        subelm = Element('url')
        subelm.text = self._Url
        elm.append(subelm)

        if self._Volume > 0:
            subelm = Element('volume')
            subelm.text = str(self._Volume)
            elm.append(subelm)
        if self._AppKey != None: 
            subelm = Element('app_key')
            subelm.text = self._AppKey
            elm.append(subelm)
        if self._Service != None: 
            subelm = Element('service')
            subelm.text = self._Service
            elm.append(subelm)
        if self._Message != None: 
            subelm = Element('message')
            subelm.text = self._Message
            elm.append(subelm)
        if self._Reason != None: 
            subelm = Element('reason')
            subelm.text = self._Reason
            elm.append(subelm)
        return elm


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'PlayItem:'
        msg = '%s volume=%s' % (msg, str(self._Volume))
        if self._AppKey and len(self._AppKey) > 0: msg = '%s appKey="%s"' % (msg, str(self._AppKey))
        if self._Service and len(self._Service) > 0: msg = '%s service="%s"' % (msg, str(self._Service))
        if self._Message and len(self._Message) > 0: msg = '%s message="%s"' % (msg, str(self._Message))
        if self._Reason and len(self._Reason) > 0: msg = '%s reason="%s"' % (msg, str(self._Reason))
        if self._Url and len(self._Url) > 0: msg = '%s url="%s"' % (msg, str(self._Url))
        return msg 


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
        elm = self.ToElement()
        xml = tostring(elm, encoding='unicode')
        return xml


    def ToXmlString(self, encoding:str='utf-8') -> str:
        """ 
        Returns an xml string representation of the class. 
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.
        """
        return self.ToXmlRequestBody(encoding)
