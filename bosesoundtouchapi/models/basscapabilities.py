# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindInt, _xmlFindBool

@export
class BassCapabilities:
    """
    SoundTouch device BassCapabilities configuration object.
       
    This class contains the attributes and sub-items that represent the 
    bass capabilities configuration of the device.      
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Default:int = None
        self._DeviceId:str = None
        self._IsAvailable:bool = None
        self._Maximum:int = None
        self._Minimum:int = None

        if (root is None):
            
            pass
        
        else:

            self._Default = _xmlFindInt(root, 'bassDefault')
            self._DeviceId = root.get('deviceID')
            self._IsAvailable = _xmlFindBool(root, 'bassAvailable')
            self._Maximum = _xmlFindInt(root, 'bassMax')
            self._Minimum = _xmlFindInt(root, 'bassMin')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Default(self) -> int:
        """ The default value of the bass level. """
        return self._Default


    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId

    
    @property
    def IsAvailable(self) -> bool:
        """ Returns True if the bass level of the device is adjustable; otherwise, False. """
        return self._IsAvailable


    @property
    def Maximum(self) -> int:
        """ The maximum allowed value of the bass level. """
        return self._Maximum


    @property
    def Minimum(self) -> int:
        """ The minimum allowed value of the bass level. """
        return self._Minimum


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'device_id': self._DeviceId,
            'default': self._Default,
            'is_available': self._IsAvailable,
            'maximum': self._Maximum,
            'minimum': self._Minimum,
        }
        return result
        

    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'BassCapabilities:'
        if self._DeviceId is not None and len(self._DeviceId) > 0: msg = '%s DeviceId="%s"' % (msg, str(self._DeviceId))
        if self._IsAvailable is not None: msg = '%s Available=%s' % (msg, str(self._IsAvailable).lower())
        if self._Minimum is not None: msg = '%s Min=%d' % (msg, self._Minimum)
        if self._Maximum is not None: msg = '%s Max=%d' % (msg, self._Maximum)
        if self._Default is not None: msg = '%s Default=%d' % (msg, self._Default)
        return msg 
