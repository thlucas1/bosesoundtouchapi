# external package imports.
import xml.etree.ElementTree as xmltree

# our package imports.
from bosesoundtouchapi.bstutils import export
from bosesoundtouchapi.soundtoucherror import SoundTouchError

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SILevel, SISession
_logsi:SISession = SIAuto.Si.GetSession(__package__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__package__, True)
_logsi.SystemLogger = logging.getLogger(__package__)


@export
class SoundTouchFirmwareRelease:
    """
    A Bose SoundTouch release targets a specific firmware upgrade.

    The specific information can be loaded from an XML-Element (ElementTree.Element).
    There is a static method that implements the parsing process to save the values
    stored in the XML-Element.
    """
    
    def __init__(self, revision:str=None, httpHost:str=None, urlPath:str=None, 
                 usbPath:str=None, image:dict=None, notesUrl:str=None, 
                 features:list=None
                 ) -> None:
        """
        Args:
            revision (str):
                The revision number of the current release.
            httpHost (str):
                The http hostname of the update provider.
            urlPath (str):
                The uri part of the full url linked to the downloadable update file.
            usbPath (str):
                The uri part of the full url linked to the downloadable USB device update file.
            image (dict[str, str]):
                The main property storing data related to the firmware image.
            notesUrl (str):
                If the update file contains some release notes, the url is given within this property.
            features (list[dict[str, str]]):
                If there are some features within the release, they are added to this list as a dict.
        """
        self._Features:list = features if features else []
        self._HttpHost:str = httpHost
        self._Image:dict = image if image else {}
        self._NotesUrl:str = notesUrl
        self._Revision:str = revision
        self._UrlPath:str = urlPath
        self._UsbPath:str = usbPath


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Features(self) -> list:
        """
        If there are some features within the release, they are added to this list as a dict.
        """
        return self._Features


    @property
    def HttpHost(self) -> str:
        """
        HTTP Hostname of the update provider.
        """
        return self._HttpHost


    @property
    def Image(self) -> dict:
        """
        Main property storing data related to the firmware image.
        """
        return self._Image


    @property
    def NotesUrl(self) -> str:
        """
        If the update file contains some release notes, the URL is given within this property.
        """
        return self._NotesUrl


    @property
    def Revision(self) -> str:
        """
        Revision number of the current release.
        """
        return self._Revision


    @property
    def UrlPath(self) -> str:
        """
        URI part of the full URL linked to the downloadable update file.
        """
        return self._UrlPath


    @property
    def UsbPath(self) -> str:
        """
        The uri part of the full url linked to the downloadable USB device update file.
        """
        return self._UsbPath


    @staticmethod
    def LoadFromXmlElement(element:xmltree.Element) -> 'SoundTouchFirmwareRelease':
        """
        Creates a new `SoundTouchFirmwareRelease` instance from an xml element that
        contains firmware details.

        Args:
            element (xmltree.Element):
                The root element with the tag "RELEASE".
                
        Returns:
            A `SoundTouchFirmwareRelease` object that contains the parsed firmware
            release details.
            
        Raises:
            SoundTouchError: 
                If the element argument is null.
        """
        if not element:
            raise SoundTouchError('Expected non null input', logsi=_logsi)

        # process base element details.
        release = SoundTouchFirmwareRelease(
            element.get('REVISION', None),
            element.get('HTTPHOST', None),
            element.get('URLPATH', None),
            element.get('USBPATH', None)
        )

        # process IMAGE element details (if any).
        image = element.find('IMAGE')
        if image is not None:
            release._Image = image.attrib

        # process NOTES element details (if any).
        notes = element.find('NOTES')
        if notes is not None:
            release._NotesUrl = notes.get('URL', None)

        # process FEATURE element details (if any).
        for feature in element.findall('FEATURE'):
            release._Features.append(feature.attrib)
            
        return release


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchFirmwareRelease:'
        msg = "%s  revision='%s'" % (msg, self._Revision)
        msg = "%s, host='%s'" % (msg, self._HttpHost)
        msg = "%s, urlPath='%s'" % (msg, self._UrlPath)
        msg = "%s, usbPath='%s'" % (msg, self._UsbPath)
        msg = "%s, notes='%s'" % (msg, self._NotesUrl)
        return msg
