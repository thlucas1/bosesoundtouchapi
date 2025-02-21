# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindInt
from ..soundtouchmodelrequest import SoundTouchModelRequest

@export
class Bass(SoundTouchModelRequest):
    """
    SoundTouch device Bass configuration object.
       
    This class contains the attributes and sub-items that represent the 
    bass configuration of the device.      
    """

    def __init__(self, target:int=0,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            target (int):
                Target bass level to set.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Actual:int = None
        self._DeviceId:str = None
        self._Target:int = None

        if (root is None):
            
            self._Target = int(target) if target else 0

        else:

            self._DeviceId = root.get('deviceID')
            self._Actual = _xmlFindInt(root, 'actualbass')
            self._Target = _xmlFindInt(root, 'targetbass')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Actual(self) -> int:
        """ Actual value of the bass level. """
        return self._Actual


    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId

    
    @property
    def Target(self) -> int:
        """ Targeted value of the bass level. """
        return self._Target


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'device_id': self._DeviceId,
            'actual': self._Actual,
            'target': self._Target,
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
        elm = Element('bass')
        if isRequestBody == True:
            
            if self._Target is not None:
                elm.text = str(self._Target)
            
        else:
            
            if self._DeviceId and len(self._DeviceId) > 0: elm.set('deviceID', str(self._DeviceId))
                           
            if self._Target is not None:
                elmNode = Element('targetbass')
                elmNode.text = str(self._Target)
                elm.append(elmNode)
                
            if self._Actual is not None:
                elmNode = Element('actualbass')
                elmNode.text = str(self._Actual)
                elm.append(elmNode)
                
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Bass:'
        if self._DeviceId is not None and len(self._DeviceId) > 0: msg = '%s DeviceId="%s"' % (msg, str(self._DeviceId))
        if self._Actual is not None: msg = '%s Actual=%d' % (msg, self._Actual)
        if self._Target is not None: msg = '%s Target=%d' % (msg, self._Target)
        return msg 
    