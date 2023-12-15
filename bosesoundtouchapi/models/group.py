# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from bosesoundtouchapi.bstutils import export, _xmlGetAttrInt, _xmlFind
from bosesoundtouchapi.soundtoucherror import SoundTouchError
from bosesoundtouchapi.soundtouchmodelrequest import SoundTouchModelRequest
from .grouprole import GroupRole
from .groupstatustypes import GroupStatusTypes

@export
class Group(SoundTouchModelRequest):
    """
    SoundTouch device Group configuration object.
       
    This class contains the attributes and sub-items that represent a
    group (stereo pair) configuration of the device.
    """

    def __init__(self, groupId:int=None, name:str=None, masterDeviceId:str=None, senderIpAddress:str=None, 
                 roles:list=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            groupId (int):
                Unique identifier of the group.
            name (str):
                User-friendly name of the Group.
            masterDeviceId (str):
                Unique identifier of the master device in the group.
            senderIPAddress (str):
                Sender device IPV4 address.
            roles (list):
                List of `GroupRole` objects that are under the control of this Group.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchWarning:
                If any Group member specified by the members argument is not a `GroupRole`
                object, or if a device id was not supplied for each member.
        """
        self._GroupId:int = None
        self._MasterDeviceId:str = None
        self._Name:str = None
        self._Roles:list[GroupRole] = []
        self._SenderIpAddress:str = None
        self._Status:str = None

        if (root is None):
            
            self._GroupId = int(groupId) if groupId else None
            self._MasterDeviceId = masterDeviceId
            self._Name = name
            self._SenderIpAddress = senderIpAddress
            self._Status = None
            
            if roles is not None:
                if isinstance(roles, list):
                    role:GroupRole    
                    for role in roles:
                        if isinstance(role, GroupRole):
                            self._Roles.append(GroupRole(root=role))

        else:
            
            self._GroupId = _xmlGetAttrInt(root, 'id')
            self._MasterDeviceId = _xmlFind(root, 'masterDeviceId')
            self._Name = _xmlFind(root, 'name')
            self._SenderIpAddress = _xmlFind(root, 'senderIPAddress')
            self._Status = _xmlFind(root, 'status')
            
            elmRoles:Element = root.find('roles')
            if elmRoles is not None:
                for elm in elmRoles.findall('groupRole'):
                    self._Roles.append(GroupRole(root=elm))


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def GroupId(self) -> int:
        """ Unique identifier of the group. """ 
        return self._GroupId


    @property
    def MasterDeviceId(self) -> str:
        """ Unique identifier of the master device in the group. """
        return self._MasterDeviceId


    @property
    def Name(self) -> str:
        """ User-friendly name of the Group. """
        return self._Name

    @Name.setter
    def Name(self, value:str):
        """ 
        Sets the Name property value.
        """
        if value is not None:
            self._Name = value
            self._SenderIpAddress = None
            self._Status = None


    @property
    def Roles(self) -> list[GroupRole]:
        """ The list of `GroupRole` objects that are (or will be) members of this Group. """
        return self._Roles


    @property
    def SenderIpAddress(self) -> str:
        """ Sender device IPV4 address. """
        return self._SenderIpAddress


    @property
    def Status(self) -> GroupStatusTypes:
        """ State of the stereo pair group (e.g. ""). """
        return self._Status


    def AddRole(self, role:GroupRole, logsi=None):
        """ 
        Add a new role to the list of roles for this Group.
        
        Args:
            role:
                The `GroupRole` object to append.
            logsi:
                A SmartInspect logging session, used to log exception messages.
                
        Raises:
            SoundTouchError:
                Role to be added is not a GroupRole object.
                Role to be added did not specify a DeviceId.
                Role DeviceId to be added or removed cannot be the master DeviceId.
                
        The master SoundTouch device cannot find roles without their device
        id.  This method will validate each role in the list to ensure that
        a device id was supplied.
        """
        if role is not None: 
            if not isinstance(role, GroupRole):
                raise SoundTouchError('Group member to be added is not a GroupRole object: %s' % str(role), logsi=logsi)
            if role.DeviceId is None:
                raise SoundTouchError('Group member to be added did not specify a DeviceId: %s' % role.ToString(), logsi=logsi)
            if role.IpAddress is None:
                raise SoundTouchError('Group member to be added did not specify a IpAddress: %s' % role.ToString(), logsi=logsi)
            self._Roles.append(role)


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('group')
        if self._GroupId is not None: 
            elm.set('id', str(self._GroupId))
            
        if self._Name is not None: 
            elmNode = Element('name')
            elmNode.text = self._Name
            elm.append(elmNode)

        if self._MasterDeviceId is not None: 
            elmNode = Element('masterDeviceId')
            elmNode.text = self._MasterDeviceId
            elm.append(elmNode)

        if self._SenderIpAddress is not None: 
            elmNode = Element('senderIPAddress')
            elmNode.text = self._SenderIpAddress
            elm.append(elmNode)

        if self._Status is not None: 
            elmNode = Element('status')
            elmNode.text = self._Status
            elm.append(elmNode)

        elmRoles = Element('roles')
        item:GroupRole
        for item in self._Roles:
            elmRoles.append(item.ToElement())
        elm.append(elmRoles)
            
        return elm


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'Group:'
        if self._GroupId is not None: msg = '%s GroupId="%s"' % (msg, str(self._GroupId))
        if self._Name is not None and len(self._Name) > 0: msg = '%s Name="%s"' % (msg, str(self._Name))
        if self._MasterDeviceId is not None and len(self._MasterDeviceId) > 0: msg = '%s MasterDeviceId="%s"' % (msg, str(self._MasterDeviceId))
        if self._SenderIpAddress is not None and len(self._SenderIpAddress) > 0: msg = '%s SenderIpAddress="%s"' % (msg, str(self._SenderIpAddress))
        if self._Status is not None and len(self._Status) > 0: msg = '%s Status="%s"' % (msg, str(self._Status))
        msg = "%s (%d items)" % (msg, len(self.Roles))
        
        if includeItems == True:
            item:GroupRole
            for item in self._Roles:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg


    def ToStringRoleSummary(self) -> str:
        """
        Returns a displayable string representation of the Roles list.
        """
        msg:str = "(%d items): " % (len(self._Roles))
        item:GroupRole
        for item in self._Roles:
            msg = "%s '%s (%s) %s'," % (msg, item.DeviceId, item.IpAddress, item.Role)
            
        return msg[0:len(msg)-1]
