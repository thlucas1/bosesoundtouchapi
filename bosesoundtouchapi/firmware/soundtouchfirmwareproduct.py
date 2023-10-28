# external package imports.
import xml.etree.ElementTree as xmltree

# our package imports.
from bosesoundtouchapi.soundtoucherror import SoundTouchError

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SILevel, SISession, SIColors
_logsi:SISession = SIAuto.Si.GetSession(__name__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__name__, True)
_logsi.SystemLogger = logging.getLogger(__name__)


class SoundTouchFirmwareProduct:
    """
    A class storing the product id and the linked URL where the firmware
    can be downloaded.
    """
    
    def __init__(self, productId:int=0x00, indexUrl:str=None, deviceClass:str=None) -> None:
        """
        Args:
            productId (int):
                The product id given by Bose.
            indexUrl (str):
                Specifies where the index.xml file is located.  
                Use the XML-Document stored at this link as the parameter in `LoadIndex` method.
            deviceClass (str):
                Some products have a special device class added to their entry. (Usage unknown)
        """
        self._DeviceClass:str = deviceClass
        self._IndexUrl:str = indexUrl
        self._ProductId:int = productId


    def __str__(self) -> str:
        return self.ToString()
    

    @property
    def DeviceClass(self) -> str:
        """
        Some products have a special device class added to their entry. (Usage unknown)
        """
        return self._DeviceClass


    @property
    def HasDeviceClass(self) -> bool:
        """
        Returns whether this product stores a device class (True) or not (False).
        """
        return (self._DeviceClass is not None)


    @property
    def IndexUrl(self) -> str:
        """
        Specifies where the index.xml file is located.  
        
        Use the XML-Document stored at this link as the parameter in `LoadIndex` method.
        """
        return self._IndexUrl


    @property
    def ProductId(self) -> int:
        """
        The product id given by Bose.
        """
        return self._ProductId


    @staticmethod
    def LoadFromXmlElement(element:xmltree.Element) -> 'SoundTouchFirmwareProduct':
        """
        Creates a new `SoundTouchFirmwareProduct` instance from an xml element that
        contains firmware product details.

        Args:
            element (xmltree.Element):
                The root element
                
        Returns:
            A `SoundTouchFirmwareProduct` object that contains the parsed firmware 
            product details.
            
        Raises:
            SoundTouchError: 
                If the element argument is null.
        """
        if not element:
            raise SoundTouchError('Invalid XML-Element (nullptr)', logsi=_logsi)

        return SoundTouchFirmwareProduct(
            int(element.get('PID', default='0'), 16),
            element.get('URL'),
            element.get('DEVICE_CLASS', None)
        )


    @staticmethod
    def LoadLookupXml(root:xmltree.Element) -> list:
        """
        Loads a XML-Element into a list of `SoundTouchFirmwareProduct` objects.

        This method can be called after fetching the lookup.xml file.

        Args:
            root (xmltree.Element):
                The xml root-element for the lookup file.
    
        Returns:  
            A list of parsed products.
        """
        if not root:
            return []

        data = []
        for prod in root.findall('PRODUCT'):
            data.append(SoundTouchFirmwareProduct.LoadFromXmlElement(prod))

        for prod in root.findall('PRA-PRODUCT'):
            data.append(SoundTouchFirmwareProduct.LoadFromXmlElement(prod))
            
        return data


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchFirmwareProduct:'
        msg = "%s id='%s'" % (msg, self._ProductId)
        msg = "%s indexUrl='%s'" % (msg, self._IndexUrl)
        return msg
