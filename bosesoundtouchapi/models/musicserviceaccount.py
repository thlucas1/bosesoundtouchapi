# external package imports.
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind
from ..soundtouchmodelrequest import SoundTouchModelRequest


@export
class MusicServiceAccount(SoundTouchModelRequest):
    """
    SoundTouch device MusicServiceAccount configuration object.
       
    This class contains the attributes and sub-items that represent the 
    Audio DSP Controls configuration of the device.      
    """

    def __init__(self, source:str=None, displayName:str=None, userName:str=None, password:str=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                Account source value (e.g. "STORED_MUSIC", "SPOTIFY", "AMAZON", etc).
            displayName (str):
                Account display name that appears in UI's.
            userName (str):
                User name value used to authenticate to the service.
            password (str):
                Password value used to authenticate to the service.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchError:
                videoSyncAudioDelay argument was not of type int.  
        """
        # initialize storage.
        self._Source:str = None
        self._DisplayName:str = None
        self._UserName:str = None
        self._Password:str = None
        
        if (root is None):
            
            # base fields.
            self._Source = source
            self._DisplayName = displayName
            self._UserName = userName
            self._Password = password
        
        elif root.tag == 'credentials':

            # base fields.
            self._Source = root.get('source', default=None)
            self._DisplayName = root.get('displayName', default=None)
            self._UserName = _xmlFind(root, 'user', default=None)
            self._Password = _xmlFind(root, 'pass', default=None)


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def Source(self) -> str:
        """ Account source value (e.g. "STORED_MUSIC", "SPOTIFY", etc). """
        return self._Source


    @property
    def DisplayName(self) -> str:
        """ Account display name that appears in UI's. """
        return self._DisplayName


    @property
    def UserName(self) -> str:
        """ User name value used to authenticate to the service. """
        return self._UserName


    @property
    def Password(self) -> str:
        """ Password value used to authenticate to the service. """
        return self._Password


    def ToElement(self) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 
        """
        elm = Element('credentials')
        elm.set('source', self._Source or '')
        elm.set('displayName', self._DisplayName or '')
        
        elm_user = Element('user')
        elm_user.text = '%s/0' % (self._UserName or '')
        elm.append(elm_user)

        elm_pass = Element('pass')
        elm_pass.text = self._Password or ''
        elm.append(elm_pass)

        return elm


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'MusicServiceAccount:'
        msg = '%s Source="%s"' % (msg, self._Source)
        msg = '%s DisplayName="%s"' % (msg, self._DisplayName)
        msg = '%s Username="%s"' % (msg, self._UserName)
        msg = '%s Password="%s"' % (msg, "".ljust(len(self._Password or ''), '*'))
        return msg 


    def ToXmlRequestBody(self, encoding:str='utf-8') -> str:
        """ 
        Overridden.
        Returns a POST request body for supplying music service account credentials.
        
        Returns:
            An xml string that can be used in a POST request to update the
            device configuration.
        """
        elm = self.ToElement()
        xml = tostring(elm, encoding='unicode')
        return xml
