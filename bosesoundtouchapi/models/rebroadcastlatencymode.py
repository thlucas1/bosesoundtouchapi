# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export

@export
class RebroadcastLatencyMode:
    """
    SoundTouch device RebroadcastLatencyMode configuration object.
       
    This class contains the attributes and sub-items that represent the 
    Rebroadcast Latency Mode configuration of the device.      
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        # initialize storage.
        self._Controllable:bool = None
        self._Mode:str = None

        if (root is None):

            pass

        elif root.tag == 'rebroadcastlatencymode':

            # base fields.
            self._Mode = root.get('mode', default=None)
            self._Controllable = bool(root.get('controllable', default='false') == 'true')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Controllable(self) -> bool:
        """ True if the latency mode is controllable; otherwise, False. """
        return self._Controllable


    @property
    def Mode(self) -> str:
        """ The mode value (e.g. "SYNC_TO_ZONE", "SYNC_TO_ROOM", etc). """
        return self._Mode


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'RebroadcastLatencyMode:'
        msg = '%s mode="%s"' % (msg, str(self._Mode))
        msg = '%s controllable=%s' % (msg, str(self._Controllable).lower())
        return msg 
