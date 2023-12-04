# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export

@export
class SoftwareUpdateCheckResponse:
    """
    SoundTouch device SoftwareUpdateCheckResponse configuration object.
       
    This class contains the attributes and sub-items that represent a
    software update check response.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._DeviceId:str = None
        self._IndexFileUrl:str = None
        self._ReleaseRevision:str = None

        if (root is None):

            pass

        else:

            self._DeviceId = root.get('deviceID')
            self._IndexFileUrl = root.get('indexFileUrl')
            
            elmRelease:Element = root.find('release')
            if elmRelease is not None:
                self._ReleaseRevision = elmRelease.get('revision')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId


    @property
    def IndexFileUrl(self) -> str:
        """ 
        Index file url to query for firmware update details (e.g. https://worldwide.bose.com/updates/soundtouch).
        """
        return self._IndexFileUrl


    @property
    def ReleaseRevision(self) -> str:
        """ 
        Latest release revision of available firmware update for the device.
        """
        return self._ReleaseRevision


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoftwareUpdateCheckResponse:'
        if self._DeviceId is not None and len(self._DeviceId) > 0: msg = '%s DeviceId="%s"' % (msg, self._DeviceId)
        if self._ReleaseRevision is not None and len(self._ReleaseRevision) > 0: msg = '%s ReleaseRevision="%s"' % (msg, self._ReleaseRevision)
        if self._IndexFileUrl is not None and len(self._IndexFileUrl) > 0: msg = '%s IndexFileUrl="%s"' % (msg, self._IndexFileUrl)
        return msg
