# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind
from ..soundtouchmodelrequest import SoundTouchModelRequest

@export
class Balance(SoundTouchModelRequest):
    """
    SoundTouch device Balance configuration object.
       
    This class contains the attributes and sub-items that represent the 
    balance configuration of the device.      
    """

    def __init__(self, actual:int=0,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            actual (int):
                The actual value of the balance level.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        if (root is None):

            self._Actual = int(actual) if actual else 0

        else:

            self._Actual = int(_xmlFind(root, 'actualBalance', default=0))
            self._Default = int(_xmlFind(root, 'balanceDefault', default=0))
            self._DeviceId = root.get('deviceID')
            self._IsAvailable = _xmlFind(root, 'balanceAvailable', default='false') == 'true'
            self._Maximum = int(_xmlFind(root, 'balanceMax', default=0))
            self._Minimum = int(_xmlFind(root, 'balanceMin', default=0))
            self._Target = int(_xmlFind(root, 'targetBalance', default=0))


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def Actual(self) -> int:
        """ The actual value of the balance level. """
        return self._Actual


    @property
    def Default(self) -> int:
        """ The default value of the balance level. """
        return self._Default


    @property
    def DeviceId(self):
        """ The Device identifier. """
        return self._DeviceId

    
    @property
    def IsAvailable(self) -> bool:
        """ True, if a balance confiiguration can be altered; otherwise, False. """
        return self._IsAvailable


    @property
    def Maximum(self) -> int:
        """ The maximum allowed value of the balance level. """
        return self._Maximum


    @property
    def Minimum(self) -> int:
        """ The minimum allowed value of the balance level. """
        return self._Minimum


    @property
    def Target(self) -> int:
        """ The targeted value of the balance level. """
        return self._Target


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Balance:'
        msg = '%s available=%s' % (msg, str(self._IsAvailable).lower())
        msg = '%s actual=%d' % (msg, self._Actual)
        msg = '%s target=%d' % (msg, self._Target)
        msg = '%s default=%d' % (msg, self._Default)
        msg = '%s min=%d' % (msg, self._Minimum)
        msg = '%s max=%d' % (msg, self._Maximum)
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
        return '<balance>%d</balance>' % self._Actual
