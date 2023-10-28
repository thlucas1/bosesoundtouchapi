"""
The `firmware` namespace contains classes related to the Bose SoundTouch
Firmware update process.
"""
# external package imports.
import xml.etree.ElementTree as xmltree

# our package imports.
from .soundtouchfirmwarerelease import SoundTouchFirmwareRelease
from bosesoundtouchapi.soundtoucherror import SoundTouchError

# get smartinspect logger reference; create a new session for this module name.
from smartinspectpython.siauto import SIAuto, SILevel, SISession
import logging
_logsi:SISession = SIAuto.Si.GetSession(__name__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__name__, True)
_logsi.SystemLogger = logging.getLogger(__name__)


BOSE_ST_INDEX_URL = 'https://downloads.bose.com/updates/soundtouch'
"""
To fetch the Bose SoundTouch index.xml file this URL has to be visited.
"""


class SoundTouchFirmware:
    """
    A class that targets a specific Bose SoundTouch firmware upgrade.

    The specific information can be loaded from an XML-Element (ElementTree.Element).
    There is a static method that implements the parsing process to save the values
    stored in the XML-Element.
    """
    
    def __init__(self, deviceId:int=0, productName:str=None,
                 revision:str=None, release:SoundTouchFirmwareRelease=None,
                 protocols:list=None) -> None:
        """
        Args:
            deviceId (str):
                A Bose-specific device id for this hardware object.
            productName (str):
                Product name for the linked firmware.
            revision (str):
                The revision number of the current release.
            release (SoundTouchFirmwareRelease):
                The linked firmware release.
            protocols (list[str]):
                If there are specific platform targets, some protocols are added to the
                hardware object.
        """
        self._DeviceId:int = deviceId
        self._ProductName:str = productName
        self._Protocols:list = protocols if protocols else []
        self._Release:SoundTouchFirmwareRelease = release
        self._Revision:str = revision


    def __str__(self) -> str:
        return self.ToString()
    

    @property
    def DeviceId(self) -> int:
        """
        A Bose-specific device id for this hardware object.
        """
        return self._DeviceId


    @property
    def ProductName(self) -> str:
        """
        Product name for the linked firmware.
        """
        return self._ProductName


    @property
    def Protocols(self) -> list:
        """
        If there are specific platform targets, some protocols are added to the
        hardware object.
        """
        return self._Protocols


    @property
    def Release(self) -> SoundTouchFirmwareRelease:
        """
        The linked firmware release.
        """
        return self._Release


    @property
    def Revision(self) -> str:
        """
        The revision number of the current release.
        """
        return self._Revision


    @staticmethod
    def LoadFromXmlElement(element:xmltree.Element) -> 'SoundTouchFirmware':
        """
        Creates a new `SoundTouchFirmware` instance from an xml element that
        contains firmware details.

        Args:
            element (xmltree.Element):
                The root element
                
        Returns:
            A `SoundTouchFirmware` object that contains the parsed firmware details.
            
        Raises:
            SoundTouchError: 
                If the element argument is null.
        """
        if not element:
            raise SoundTouchError('Invalid XML-Element', logsi=_logsi)

        dev = SoundTouchFirmware(
            int(element.get('ID', default='0'), 16),
            element.get('PRODUCTNAME')
        )
        hardwareElm = element.find('HARDWARE')
        if hardwareElm is not None:
            dev._Revision = hardwareElm.get('REVISION', None)
            dev._Release = SoundTouchFirmwareRelease.LoadFromXmlElement(hardwareElm.find('RELEASE'))

        return dev
   

    @staticmethod
    def LoadIndex(root:xmltree.Element) -> list:
        """
        Loads an XML-Element into a list of `SoundTouchFirmware` objects.

        This method can be called after fetching the index.xml file for a firmware
        release.

        Args:
            root (xmltree.Element):
                The xml root-element for the index file.
            
        Returns:  
            A list of parsed firmware releases.
        """
        if not root:
            return []

        elements = []
        for dev in root.findall('DEVICE'):
            elements.append(SoundTouchFirmware.LoadFromXmlElement(dev))
        return elements


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchFirmware:'
        msg = "%s product='%s'" % (msg, self._ProductName)
        msg = "%s deviceId='%s'" % (msg, self._DeviceId)
        msg = "%s revision='%s'" % (msg, self._Revision)
        return msg
