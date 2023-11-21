# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind
from ..soundtouchmodelrequest import SoundTouchModelRequest

@export
class Bass(SoundTouchModelRequest):
    """
    SoundTouch device Bass configuration object.
       
    This class contains the attributes and sub-items that represent the 
    bass configuration of the device.      
    """

    def __init__(self, actual:int=0,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            actual (int):
                The actual value of the bass level.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Actual:int = None
        self._Target:int = None

        if (root is None):
            
            self._Actual = int(actual) if actual else 0

        else:

            self._Actual = int(_xmlFind(root, 'actualbass', default=0))
            self._Target = int(_xmlFind(root, 'targetbass', default=0))


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Actual(self) -> int:
        """ Actual value of the bass level. """
        return self._Actual


    @property
    def Target(self) -> int:
        """ Targeted value of the bass level. """
        return self._Target


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Bass:'
        msg = '%s actual=%d' % (msg, self._Actual)
        msg = '%s target=%d' % (msg, self._Target)
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
        return '<bass>%s</bass>' % self._Actual
