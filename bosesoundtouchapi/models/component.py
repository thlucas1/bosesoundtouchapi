# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind

@export
class Component:
    """
    SoundTouch device Component configuration object.
       
    This class contains the attributes and sub-items that represents a
    component configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._ComponentCategory:str = None
        self._SoftwareVersion = None
        self._SerialNumber = None
        
        if (root is None):
            
            # nothing to do - always build it from a response.
            pass
        
        else:

            self._ComponentCategory = _xmlFind(root, 'componentCategory')
            self._SerialNumber = _xmlFind(root, 'serialNumber')
            self._SoftwareVersion = _xmlFind(root, 'softwareVersion')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ComponentCategory(self) -> str:
        """ The component category (e.g. "SCM", "SMSC", etc). """
        return self._ComponentCategory


    @property
    def SerialNumber(self) -> str:
        """ A unique manufacturer assigned serial number of the device. """
        return self._SerialNumber


    @property
    def SoftwareVersion(self) -> str:
        """ Current operating system software of the device. """
        return self._SoftwareVersion


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Component:'
        if self._ComponentCategory is not None and len(self._ComponentCategory) > 0: msg = '%s ComponentCategory="%s"' % (msg, self._ComponentCategory)
        if self._SerialNumber is not None and len(self._SerialNumber) > 0: msg = '%s SerialNumber="%s"' % (msg, self._SerialNumber)
        if self._SoftwareVersion is not None and len(self._SoftwareVersion) > 0: msg = '%s SoftwareVersion="%s"' % (msg, self._SoftwareVersion)
        return msg 
    