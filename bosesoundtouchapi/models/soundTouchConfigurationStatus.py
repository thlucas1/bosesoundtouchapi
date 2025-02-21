# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export

@export
class SoundTouchConfigurationStatus:
    """
    SoundTouch device SoundTouchConfigurationStatus configuration object.
       
    This class contains the attributes and sub-items that represent the
    SoundTouch configuration status configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Status:str = None

        if (root is None):
            
            pass
        
        else:

            # base fields.
            self._Status = root.get('status')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Status(self) -> str:
        """ 
        Status of the SoundTouch configuration process ("SOUNDTOUCH_CONFIGURED", 
        "SOUNDTOUCH_NOT_CONFIGURED", "SOUNDTOUCH_CONFIGURING"). 
        """
        return self._Status


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'status': self._Status,
        }
        return result
        

    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchConfigurationStatus:'
        if self._Status and len(self._Status) > 0: msg = '%s status="%s"' % (msg, self._Status)
        return msg
