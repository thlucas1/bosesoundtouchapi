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
        self._Actual:int = None
        self._Default:int = None
        self._DeviceId:str = None
        self._IsAvailable:bool = None
        self._Maximum:int = None
        self._Minimum:int = None
        self._Target:int = None

        if (root is None):

            self._Actual = int(actual) if actual else 0

        else:

            self._DeviceId = root.get('deviceID')
            self._Actual = int(_xmlFind(root, 'actualBalance', default=0))
            self._Default = int(_xmlFind(root, 'balanceDefault', default=0))
            self._IsAvailable = _xmlFind(root, 'balanceAvailable', default='false') == 'true'
            self._Maximum = int(_xmlFind(root, 'balanceMax', default=0))
            self._Minimum = int(_xmlFind(root, 'balanceMin', default=0))
            self._Target = int(_xmlFind(root, 'targetBalance', default=0))


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Actual(self) -> int:
        """ Actual value of the balance level. """
        return self._Actual


    @property
    def Default(self) -> int:
        """ Default value of the balance level. """
        return self._Default


    @property
    def DeviceId(self):
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId

    
    @property
    def IsAvailable(self) -> bool:
        """ True, if a balance confiiguration can be altered; otherwise, False. """
        return self._IsAvailable


    @property
    def Maximum(self) -> int:
        """ Maximum allowed value of the balance level. """
        return self._Maximum


    @property
    def Minimum(self) -> int:
        """ Minimum allowed value of the balance level. """
        return self._Minimum


    @property
    def Target(self) -> int:
        """ Targeted value of the balance level. """
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
        elm = Element('balance')
        if isRequestBody == True:
            
            elm.text = str(self.Actual)
            
        else:
            
            if self._DeviceId and len(self._DeviceId) > 0: elm.set('deviceID', str(self._DeviceId))
            
            if self._IsAvailable is not None:
                elmNode = Element('balanceAvailable')
                elmNode.text = str(self._IsAvailable)
                elm.append(elmNode)
                
            if self._Minimum is not None:
                elmNode = Element('balanceMin')
                elmNode.text = str(self._Minimum)
                elm.append(elmNode)
                
            if self._Maximum is not None:
                elmNode = Element('balanceMax')
                elmNode.text = str(self._Maximum)
                elm.append(elmNode)
                
            if self._Default is not None:
                elmNode = Element('balanceDefault')
                elmNode.text = str(self._Default)
                elm.append(elmNode)
                
            if self._Target is not None:
                elmNode = Element('targetBalance')
                elmNode.text = str(self._Target)
                elm.append(elmNode)
                
            if self._Actual is not None:
                elmNode = Element('actualBalance')
                elmNode.text = str(self._Actual)
                elm.append(elmNode)
                
        return elm

        
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
