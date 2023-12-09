# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindInt
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
        self._AppKey:str = None
        self._Service:str = None
        self._Message:str = None
        self._Reason:str = None
        self._Url:str = None
        self._Volume:int = None

        if (root is None):
            
            if appKey is None:
                appKey = BOSE_DEVELOPER_APPKEY
            if service is None:
                service = "Unknown"
            if (volume is None) or (not isinstance(volume, int)) or (volume < 0) or (volume > 100):
                volume = int(30)

            self._AppKey = appKey
            self._Service = service
            self._Message = message
            self._Reason = reason
            self._Url = url
            self._Volume = int(volume)
            
        else:

            self._AppKey = _xmlFind(root, 'app_key')
            self._Service = _xmlFind(root, 'service')
            self._Message = _xmlFind(root, 'message')
            self._Reason = _xmlFind(root, 'reason')
            self._Url = _xmlFind(root, 'url')
            self._Volume = _xmlFindInt(root, 'volume')

        
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
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


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('play_info')
        
        if self._Url is not None:
            elmNode = Element('url')
            elmNode.text = self._Url
            elm.append(elmNode)
            
        # volume should be omitted if it is zero.
        if self._Volume is not None and self._Volume > 0:
            elmNode = Element('volume')
            # SoundTouch will fail the request if volume level is less than 10 or greater than 70.
            if (self._Volume < 10): 
                elmNode.text = "10"
            elif (self._Volume > 70): 
                elmNode.text = "70"
            else: 
                elmNode.text = str(self._Volume)
            elm.append(elmNode)
            
        if self._AppKey is not None:
            elmNode = Element('app_key')
            elmNode.text = self._AppKey
            elm.append(elmNode)
            
        if self._Service is not None:
            elmNode = Element('service')
            elmNode.text = self._Service
            elm.append(elmNode)
            
        if self._Message is not None:
            elmNode = Element('message')
            elmNode.text = self._Message
            elm.append(elmNode)
            
        if self._Reason is not None:
            elmNode = Element('reason')
            elmNode.text = self._Reason
            elm.append(elmNode)
            
        return elm


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'PlayItem:'
        if self._Volume is not None: msg = '%s volume=%s' % (msg, str(self._Volume))
        if self._AppKey is not None and len(self._AppKey) > 0: msg = '%s appKey="%s"' % (msg, str(self._AppKey))
        if self._Service is not None and len(self._Service) > 0: msg = '%s service="%s"' % (msg, str(self._Service))
        if self._Message is not None and len(self._Message) > 0: msg = '%s message="%s"' % (msg, str(self._Message))
        if self._Reason is not None and len(self._Reason) > 0: msg = '%s reason="%s"' % (msg, str(self._Reason))
        if self._Url is not None and len(self._Url) > 0: msg = '%s url="%s"' % (msg, str(self._Url))
        return msg 


    def ToXmlString(self, encoding:str='utf-8') -> str:
        """ 
        Returns an xml string representation of the class. 
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.
        """
        return self.ToXmlRequestBody(encoding)
