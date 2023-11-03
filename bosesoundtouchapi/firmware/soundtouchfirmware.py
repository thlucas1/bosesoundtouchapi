"""
The `firmware` namespace contains classes related to the Bose SoundTouch
Firmware update process.
"""
# external package imports.
import requests
import xml.etree.ElementTree as xmltree

# our package imports.
from .soundtouchfirmwarerelease import SoundTouchFirmwareRelease
from bosesoundtouchapi.bstutils import export
from bosesoundtouchapi.soundtoucherror import SoundTouchError

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SILevel, SISession
_logsi:SISession = SIAuto.Si.GetSession(__package__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__package__, True)
_logsi.SystemLogger = logging.getLogger(__package__)


BOSE_SOUNDTOUCH_UPDATE_INDEX_URL = 'https://worldwide.bose.com/updates/soundtouch'
"""
To fetch the Bose SoundTouch index.xml file this URL has to be visited.

The request is forwarded to another backend which contains a XML-Document 
named `index.xml`. This file contains information about the locations of 
all available SoundTouch firmware upgrades.
"""

@export
class SoundTouchFirmware:
    """
    A class that targets a specific Bose SoundTouch firmware upgrade.

    The specific information can be loaded from an XML-Element (ElementTree.Element).
    There is a static method that implements the parsing process to save the values
    stored in the XML-Element.

    <details>
        <summary>Sample Code</summary>
    ```python
    .. include:: ../../docs/include/samplecode/SoundTouchFirmware/_ClassInit.py
    ```
    </details>
    """
    
    def __init__(self, deviceId:int=0, productName:str=None, supportedOs:str=None,
                 hardwareRevision:str=None, hardwareRelease:SoundTouchFirmwareRelease=None,
                 protocolRevision:str=None, protocolImages:list=None
                 ) -> None:
        """
        Args:
            deviceId (str):
                A Bose-specific device id for this hardware object.
            productName (str):
                Product name for the linked firmware.
            supportedOs (str):
                Supported operating system for the linked firmware.
            hardwareRevision (str):
                The hardware revision number of the current release.
            hardwareRelease (SoundTouchFirmwareRelease):
                The hardware firmware release details.
            protocolRevision (str):
                If there are specific platform targets, a protocol revision number.
            protocolImages (list):
                If there are specific platform targets, some protocol images are added to the
                hardware object.
        """
        self._DeviceId:int = deviceId
        self._ProductName:str = productName
        self._SupportedOs:str = supportedOs
        self._ProtocolRevision:str = protocolRevision
        self._ProtocolImages:list = protocolImages if protocolImages else []
        self._HardwareRelease:SoundTouchFirmwareRelease = hardwareRelease
        self._HardwareRevision:str = hardwareRevision


    def __str__(self) -> str:
        return self.ToString()
    

    @property
    def DeviceId(self) -> int:
        """
        A Bose-specific device id for this hardware object.
        """
        return self._DeviceId


    @property
    def HardwareRevision(self) -> str:
        """
        The hardware revision number of the current release.
        """
        return self._HardwareRevision


    @property
    def HardwareRelease(self) -> SoundTouchFirmwareRelease:
        """
        The hardware firmware release details.
        """
        return self._HardwareRelease


    @property
    def ProductName(self) -> str:
        """
        Product name for the linked firmware.
        """
        return self._ProductName


    @property
    def ProtocolImages(self) -> list:
        """
        If there are specific platform targets, some protocols are added to the
        hardware object.
        """
        return self._ProtocolImages


    @property
    def ProtocolRevision(self) -> str:
        """
        If there are specific platform targets, a protocol revision number.
        """
        return self._ProtocolRevision


    @property
    def SupportedOs(self) -> str:
        """
        Supported operating system for the linked firmware.
        """
        return self._SupportedOs


    @staticmethod
    def GetIndex(url:str) -> xmltree.Element:
        """
        Downloads the product index.xml file from the given url and returns an
        Element object with the results.

        Args:
            url (str):
                Url to query for the index.xml file.
                
        Returns:
            An xml.etree.ElementTree.Element object of the index file contents if downloaded successfully;
            otherwise, False.
            
        Raises:
            SoundTouchError: 
                If the url argument is null.
                If the contents of the url could not be downloaded.
        """
        if (url is None) or (len(url) == 0):
            raise SoundTouchError('url argument not specified', logsi=_logsi)
        
        try:
            
            # download the file, and load it into an Element object.
            resp = requests.get(url, allow_redirects=True)
            root = xmltree.fromstring(resp.content.decode('utf-8'))
            
            # verify it's the index.
            if (root.tag == 'INDEX') and (root.get('REVISION', None) is not None):
                return root
            
            # if it's not a recognizable index, then raise an exception.
            raise SoundTouchError('Index url (%s) content was not recognized as a firmware index' % url, logsi=_logsi)
                
        except SoundTouchError: pass    # error already logged.
        except Exception as ex:
            
            raise SoundTouchError("Could not get firmware index: %s" % str(ex), logsi=_logsi)
   

    @staticmethod
    def LoadFromXmlElement(element:xmltree.Element) -> 'SoundTouchFirmware':
        """
        Creates a new `SoundTouchFirmware` instance from an xml element that
        contains firmware details.

        Args:
            element (xml.etree.ElementTree.Element):
                The root element
                
        Returns:
            A `SoundTouchFirmware` object that contains the parsed firmware details.
            
        Raises:
            SoundTouchError: 
                If the element argument is null.
        """
        if not element:
            raise SoundTouchError('Invalid XML-Element', logsi=_logsi)

        # process base element details.
        device = SoundTouchFirmware(
            int(element.get('ID', default='0'), 16),
            element.get('PRODUCTNAME'),
            element.get('SUPPORTEDOS')
        )
        
        # process HARDWARE element details.
        hardwareElm = element.find('HARDWARE')
        if hardwareElm is not None:
            device._HardwareRevision = hardwareElm.get('REVISION', None)
            device._HardwareRelease = SoundTouchFirmwareRelease.LoadFromXmlElement(hardwareElm.find('RELEASE'))

            # process PROTOCOL element details (if any).
            protocol = hardwareElm.find('PROTOCOL')
            if protocol is not None:
                device._ProtocolRevision = protocol.get('REVISION', None)
                for image in protocol.findall('IMAGE'):
                    device._ProtocolImages.append(image.attrib)

        _logsi.LogObject(SILevel.Verbose,"Firmware Device item: %s (%s, %s)" % (device.ProductName, device.HardwareRevision, device.HardwareRelease.Revision), device, excludeNonPublic=True)
        return device
   

    @staticmethod
    def LoadIndex(root:xmltree.Element) -> list:
        """
        Loads an XML-Element into a list of `SoundTouchFirmware` objects.

        This method can be called after fetching the index.xml file for a firmware
        release.

        Args:
            root (xml.etree.ElementTree.Element):
                The xml root-element for the index file.
            
        Returns:  
            A list of parsed firmware releases.
        """
        if not root:
            return []

        # process all DEVICE elements.
        items:list[SoundTouchFirmware] = []
        for dev in root.findall('DEVICE'):
            items.append(SoundTouchFirmware.LoadFromXmlElement(dev))
            
        _logsi.LogCollection(SILevel.Verbose,"Firmware Device Collection", items)
        return items


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchFirmware:'
        msg = "%s product='%s'" % (msg, self._ProductName)
        msg = "%s deviceId='%s'" % (msg, self._DeviceId)
        msg = "%s os='%s'" % (msg, self._SupportedOs)
        msg = "%s hardwareRevision='%s'" % (msg, self._HardwareRevision)
        return msg
