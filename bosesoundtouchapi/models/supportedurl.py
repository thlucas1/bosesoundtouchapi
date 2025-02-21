# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlGetAttrBool

@export
class SupportedUrl:
    """
    SoundTouch device SupportedUrl configuration object.
       
    This class contains the attributes and sub-items that represent a
    single supportedurl item configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Location:str = None

        if (root is None):
            
            pass
        
        else:

            self._Location = root.get('location')

        
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    # implement sorting support.
    def __eq__(self, other):
        try:
            return self.Location == other.Location
        except Exception as ex:
            if (isinstance(self, SupportedUrl )) and (isinstance(other, SupportedUrl )):
                return self.Location == other.Location
            return False

    def __lt__(self, other):
        try:
            return self.Location < other.Location
        except Exception as ex:
            if (isinstance(self, SupportedUrl )) and (isinstance(other, SupportedUrl )):
                return self.Location < other.Location
            return False


    @property
    def Location(self) -> str:
        """ Url location. """
        return self._Location


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'location': self._Location,
        }
        return result
        

    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'URL:'
        if self._Location is not None and len(self._Location) > 0: msg = '%s Location="%s"' % (msg, str(self._Location))
        return msg 
