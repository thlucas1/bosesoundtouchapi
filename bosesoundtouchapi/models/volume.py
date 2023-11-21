# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind
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
        self._IsMuted:bool = None
        self._Target:int = None
        
        if (root is None):

            self._Actual = int(actual) if actual else 0
            self._IsMuted = isMuted == 'true' if isMuted else False
            self._Target = int(target) if target else 0

        else:

            self._Actual = int(_xmlFind(root, 'actualvolume', default='0'))
            self._IsMuted = bool(_xmlFind(root, 'muteenabled', default='false') == 'true')
            self._Target = int(_xmlFind(root, 'targetvolume', default='0'))


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Actual(self) -> int:
        """ The actual value of the volume level. """
        return self._Actual


    @property
    def IsMuted(self) -> bool:
        """ True if the device is muted; otherwise, False. """
        return self._IsMuted


    @property
    def Target(self) -> int:
        """ The targeted value of the volume level. """
        return self._Target


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Volume:'
        msg = '%s actual=%d' % (msg, self._Actual)
        msg = '%s target=%d' % (msg, self._Target)
        msg = '%s isMuted=%s' % (msg, str(self._IsMuted).lower())
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
        return '<volume>%d</volume>' % self._Actual
    