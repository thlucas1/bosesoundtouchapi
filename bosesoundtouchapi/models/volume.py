# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindBool, _xmlFindInt
from ..soundtouchmodelrequest import SoundTouchModelRequest

@export
class Volume(SoundTouchModelRequest):
    """
    SoundTouch device Volume configuration object.
       
    This class contains the attributes and sub-items that represent the
    volume configuration of the device.
    """

    def __init__(self, actual:int=0, target:int=0, isMuted:bool=False,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            actual (int):
                The actual value of the volume level.
            target (int):
                The targeted value of the volume level.
            isMuted (bool):
                True if the device is muted; otherwise, False.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Actual:int = None
        self._DeviceId:str = None
        self._IsMuted:bool = None
        self._Target:int = None
        
        if (root is None):

            self._Actual = int(actual) if actual else 0
            self._IsMuted = isMuted
            self._Target = int(target) if target else 0

        else:

            self._DeviceId = root.get('deviceID')
            self._Actual = _xmlFindInt(root, 'actualvolume')
            self._IsMuted = _xmlFindBool(root, 'muteenabled')
            self._Target = _xmlFindInt(root, 'targetvolume')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Actual(self) -> int:
        """ Actual value of the volume level. """
        return self._Actual


    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId

    
    @property
    def IsMuted(self) -> bool:
        """ True if the device is muted; otherwise, False. """
        return self._IsMuted


    @property
    def Target(self) -> int:
        """ Targeted value of the volume level. """
        return self._Target


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('volume')
        if isRequestBody == True:
            
            elm.text = str(self.Target)
            
        else:

            if self._DeviceId and len(self._DeviceId) > 0: elm.set('deviceID', str(self._DeviceId))
                           
            if self._Target is not None:
                elmNode = Element('targetvolume')
                elmNode.text = str(self._Target)
                elm.append(elmNode)
                
            if self._Actual is not None:
                elmNode = Element('actualvolume')
                elmNode.text = str(self._Actual)
                elm.append(elmNode)
                
            if self._IsMuted is not None:
                elmNode = Element('muteenabled')
                elmNode.text = str(self._IsMuted).lower()
                elm.append(elmNode)
                
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Volume:'
        if self._Actual is not None:msg = '%s Actual=%d' % (msg, self._Actual)
        if self._Target is not None: msg = '%s Target=%d' % (msg, self._Target)
        if self._IsMuted is not None: msg = '%s IsMuted=%s' % (msg, str(self._IsMuted).lower())
        if self._DeviceId is not None: msg = '%s DeviceId="%s"' % (msg, self._DeviceId)
        return msg 
    