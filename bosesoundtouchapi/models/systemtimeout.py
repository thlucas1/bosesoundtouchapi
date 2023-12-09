# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindBool

@export
class SystemTimeout:
    """
    SoundTouch device SystemTimeout configuration object.
       
    This class contains the attributes and sub-items that represent the
    system timeout configuration of the device.
    """
    
    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._IsPowersavingEnabled:bool = None
        
        if (root is None):

            pass

        else:

            self._IsPowersavingEnabled = _xmlFindBool(root, 'powersaving_enabled')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def IsPowersavingEnabled(self) -> bool:
        """ True if power saving is enabled on the device; otherwise, False. """
        return self._IsPowersavingEnabled


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SystemTimeout:'
        if self._IsPowersavingEnabled is not None: msg = '%s PowersavingEnabled=%s' % (msg, str(self._IsPowersavingEnabled).lower())
        return msg 
