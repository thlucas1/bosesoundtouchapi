# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export

@export
class ZoneMember:
    """
    SoundTouch device ZoneMember configuration object.
       
    This class contains the attributes and sub-items that represent a
    single multiroom zone member configuration of the device.
    """
    
    def __init__(self, ipAddress:str=None, deviceId:str=None, deviceRole:str=None, 
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            ipAddress (str):
                Zone member device IPV4 address.
            deviceId (str):
                Zone member device identifier.
            deviceRole (str):
                The role of the zone member device (optional).
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._DeviceId:str = None
        self._DeviceRole:str = None
        self._IpAddress:str = None

        if (root is None):
            
            self._IpAddress = ipAddress
            self._DeviceId = deviceId
            self._DeviceRole = deviceRole

        else:

            self._IpAddress = root.get('ipaddress')
            self._DeviceRole = root.get('role')
            self._DeviceId = root.text


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ 
        Zone member device identifier. 
        
        The master SoundTouch device cannot find zone members without their device id.
        """
        return self._DeviceId


    @property
    def DeviceRole(self) -> str:
        """ The role of the zone member device (optional). """
        return self._DeviceRole


    @property
    def IpAddress(self) -> str:
        """ Zone member device IPV4 address. """
        return self._IpAddress


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'device_id': self._DeviceId,
            'device_role': self._DeviceRole,
            'ip_address': self._IpAddress,
        }
        return result
        

    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('member')
        if self._IpAddress: elm.set('ipaddress', str(self._IpAddress))
        if self._DeviceRole: elm.set('role', str(self._DeviceRole))
        if self._DeviceId: elm.text = self._DeviceId
        return elm


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'ZoneMember:'
        if self._IpAddress and len(self._IpAddress) > 0: msg = '%s ipAddress="%s"' % (msg, str(self._IpAddress))
        if self._DeviceRole and len(self._DeviceRole) > 0: msg = '%s deviceRole="%s"' % (msg, str(self._DeviceRole))
        if self._DeviceId and len(self._DeviceId) > 0: msg = '%s deviceId="%s"' % (msg, str(self._DeviceId))
        return msg 


    def ToXmlString(self, encoding:str='utf-8') -> str:
        """ 
        Returns an xml string representation of the class. 
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.
        """
        if encoding is None:
            encoding = 'utf-8'
        elm = self.ToElement()
        xml = tostring(elm, encoding=encoding).decode(encoding)
        return xml
