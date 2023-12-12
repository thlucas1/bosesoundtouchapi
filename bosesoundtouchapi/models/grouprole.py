# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind
from .grouproletypes import GroupRoleTypes

@export
class GroupRole:
    """
    SoundTouch device GroupRole configuration object.
       
    This class contains the attributes and sub-items that represent a
    single multiroom zone member configuration of the device.
    """
    
    def __init__(self, ipAddress:str=None, deviceId:str=None, role:GroupRoleTypes=None, 
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            deviceId (str):
                Unique identifier of the device.
            ipAddress (str):
                IPV4 address of the device.
            role (GroupRoleTypes|str):
                Role (or location) of the device ("LEFT", "RIGHT").
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._DeviceId:str = None
        self._IpAddress:str = None
        self._Role:str = None

        if (root is None):
            
            if isinstance(role, GroupRoleTypes):
                role = role.value
            
            self._DeviceId = deviceId
            self._IpAddress = ipAddress
            self._Role = role

        else:

            self._DeviceId = _xmlFind(root, "deviceId")
            self._IpAddress = _xmlFind(root, "ipAddress")
            self._Role = _xmlFind(root, "role")


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ Unique identifier of the device. """
        return self._DeviceId


    @property
    def IpAddress(self) -> str:
        """ IPV4 address of the device. """
        return self._IpAddress


    @property
    def Role(self) -> str:
        """ Role (or location) of the device ("LEFT", "RIGHT", "NORMAL"). """
        return self._Role


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('groupRole')
        
        if self._DeviceId is not None: 
            elmNode = Element('deviceId')
            elmNode.text = self._DeviceId
            elm.append(elmNode)

        if self._Role is not None: 
            elmNode = Element('role')
            elmNode.text = self._Role
            elm.append(elmNode)

        if self._IpAddress is not None: 
            elmNode = Element('ipAddress')
            elmNode.text = self._IpAddress
            elm.append(elmNode)

        return elm


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'GroupRole:'
        if self._DeviceId and len(self._DeviceId) > 0: msg = '%s DeviceId="%s"' % (msg, str(self._DeviceId))
        if self._IpAddress and len(self._IpAddress) > 0: msg = '%s IpAddress="%s"' % (msg, str(self._IpAddress))
        if self._Role and len(self._Role) > 0: msg = '%s Role="%s"' % (msg, str(self._Role))
        return msg 
