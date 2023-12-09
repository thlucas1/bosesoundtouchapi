# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind
from .networkstatusinterface import NetworkStatusInterface

@export
class NetworkStatus:
    """
    SoundTouch device NetworkStatus configuration object.
       
    This class contains the attributes and sub-items that represent the
    network status configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._DeviceId = None
        self._Interfaces:list[NetworkStatusInterface] = []
        self._SerialNumber = None
        
        if (root is None):

            pass

        else:

            root_devices:Element = root.find('devices')
            root_device:Element = root_devices.find('device')
            self._DeviceId = root_device.get('deviceID')
            self._SerialNumber = _xmlFind(root_device, 'deviceSerialNumber')
        
            for interface in root_device.find('interfaces'):
                self._Interfaces.append(NetworkStatusInterface(interface))
            

    def __getitem__(self, key) -> NetworkStatusInterface:
        return self._Interfaces[key]


    def __iter__(self) -> Iterator:
        return iter(self._Interfaces)


    def __len__(self) -> int:
        return len(self._Interfaces)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ The device identifier, as assigned by the manufacturer. """
        return self._DeviceId


    @property
    def InterfaceCount(self) -> int:
        """ 
        The total number of network interfaces defined, including both
        wired and wireless. 
        """
        return len(self._Interfaces)


    @property
    def SerialNumber(self) -> str:
        """ The device serial number, as assigned by the manufacturer. """
        return self._SerialNumber


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'NetworkStatus:'
        if self._DeviceId and len(self._DeviceId) > 0: msg = '%s deviceId="%s"' % (msg, str(self._DeviceId))
        if self._SerialNumber and len(self._SerialNumber) > 0: msg = '%s serial="%s"' % (msg, str(self._SerialNumber))
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            item:NetworkStatusInterface
            for item in self:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
