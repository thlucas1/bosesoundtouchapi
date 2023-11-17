# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr

@export
class MediaServer:
    """
    SoundTouch device MediaServer configuration object.
       
    This class contains the attributes and sub-items that represent a
    single UPnP media server configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        # initialize storage.
        self._ServerId:str = None
        self._MacAddress:str = None
        self._IpAddress:str = None
        self._Manufacturer:str = None
        self._ModelName:str = None
        self._FriendlyName:str = None
        self._ModelDescription:str = None
        self._Location:str = None

        if (root is None):

            pass  # no other parms to process.

        else:

            # base fields.
            self._ServerId = root.get('id')
            self._MacAddress = root.get('mac')
            self._IpAddress = root.get('ip')
            self._Manufacturer = root.get('manufacturer')
            self._ModelName = root.get('model_name')
            self._FriendlyName = root.get('friendly_name')
            self._ModelDescription = root.get('model_description')
            self._Location = root.get('location')


    def __repr__(self) -> str:
        return self.ToString()


    # implement sorting support.
    def __eq__(self, other):
        try:
            return self.FriendlyName == other.FriendlyName
        except Exception as ex:
            if (isinstance(self, MediaServer )) and (isinstance(other, MediaServer )):
                return self.FriendlyName == other.FriendlyName
            return False

    def __lt__(self, other):
        try:
            # the following comparison will fail if the property value is None!  
            # use the following syntax when calling a sort method that uses lambda searches:
            # epColl.sort(FriendlyName=lambda x: x.FriendlyName or "", reverse=False)     <- GOOD syntax
            # epColl.sort(FriendlyName=lambda x: x.FriendlyName, reverse=False)           <- BAD syntax, as the "x.FriendlyName" property may be None, and will cause this to fail!
            return self.FriendlyName < other.FriendlyName
        except Exception as ex:
            if (isinstance(self, MediaServer )) and (isinstance(other, MediaServer )):
                return self.FriendlyName < other.FriendlyName
            return False


    @property
    def FriendlyName(self) -> str:
        """ The friendly name of the media server (e.g. "Home (Home Assistant)", "Hue Bridge", etc). """
        return self._FriendlyName


    @property
    def IpAddress(self) -> str:
        """ The IPV4 address assigned to the media server by the network. """
        return self._IpAddress


    @property
    def Location(self) -> str:
        """ The url location of the media server (e.g. "http://192.168.1.248:40000/device.xml", etc). """
        return self._Location


    @property
    def MacAddress(self) -> str:
        """ The MAC address (media access control address) assigned to the media server. """
        return self._MacAddress


    @property
    def Manufacturer(self) -> str:
        """ The manufacturer of the media server (e.g. "Home Assistant", "Signify", etc). """
        return self._Manufacturer


    @property
    def ModelDescription(self) -> str:
        """ The model description of the media server (e.g. "Philips hue Personal Wireless Lighting", etc). """
        return self._ModelDescription


    @property
    def ModelName(self) -> str:
        """ The model name of the media server (e.g. "Home Assistant OS", "Philipss Hue Bridge", etc). """
        return self._ModelName


    @property
    def ServerId(self) -> str:
        """ Globally unique identifier (guid) of the media server. """
        return self._ServerId


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'MediaServer:'
        if self._FriendlyName and len(self._FriendlyName) > 0: msg = '%s friendlyName="%s"' % (msg, str(self._FriendlyName))
        if self._ServerId and len(self._ServerId) > 0: msg = '%s id="%s"' % (msg, str(self._ServerId))
        if self._MacAddress and len(self._MacAddress) > 0: msg = '%s mac="%s"' % (msg, str(self._MacAddress))
        if self._IpAddress and len(self._IpAddress) > 0: msg = '%s ip="%s"' % (msg, str(self._IpAddress))
        if self._Manufacturer and len(self._Manufacturer) > 0: msg = '%s manufacturer="%s"' % (msg, str(self._Manufacturer))
        if self._ModelName and len(self._ModelName) > 0: msg = '%s modelName="%s"' % (msg, str(self._ModelName))
        if self._ModelDescription and len(self._ModelDescription) > 0: msg = '%s modelDescription="%s"' % (msg, str(self._ModelDescription))
        if self._Location and len(self._Location) > 0: msg = '%s location="%s"' % (msg, str(self._Location))
        return msg
