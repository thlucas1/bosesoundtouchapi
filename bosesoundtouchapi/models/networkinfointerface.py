# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export

@export
class NetworkInfoInterface:
    """
    SoundTouch device NetworkInfoInterface configuration object.
       
    This class contains the attributes and sub-items that represent a
    single network information interface configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        if (root is None):
            pass  # no other parms to process.
        else:

            # base fields.
            self._FrequencyKhz = root.get('frequencyKHz')
            self._InterfaceType = root.get('type')
            self._IpAddress = root.get('ipAddress')
            self._MacAddress = root.get('macAddress')
            self._Mode = root.get('mode')
            self._Name = root.get('name')
            self._Signal = root.get('signal')
            self._Ssid = root.get('ssid')
            self._State = root.get('state')


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def FrequencyKhz(self):
        """ 
        The frequency (in KiloHertz) the network uses to communicate with a 
        wireless router (e.g. 2452000 = 2.4GHz, etc). 
        """
        return self._FrequencyKhz


    @property
    def InterfaceType(self):
        """ The type of interface (e.g. "WIFI_INTERFACE", "ETHERNET_INTERFACE", etc). """
        return self._InterfaceType


    @property
    def IpAddress(self):
        """ The IPV4 address assigned to the device by the network. """
        return self._IpAddress


    @property
    def MacAddress(self):
        """ The MAC address (media access control address) assigned to the device. """
        return self._MacAddress


    @property
    def Mode(self):
        """ ? - TODO define this property. """
        return self._Mode


    @property
    def Name(self):
        """ The network interface name (e.g. "wlan0", "eth0", etc). """
        return self._Name


    @property
    def Signal(self):
        """ The network signal status indicator (e.g. "EXCELLENT_SIGNAL", "POOR_SIGNAL", etc). """
        return self._Signal


    @property
    def Ssid(self):
        """ The network service set identifier (SSID) the device is connected to. """
        return self._Ssid


    @property
    def State(self):
        """ 
        The state of the network connection (e.g. "NETWORK_WIFI_CONNECTED", 
        "NETWORK_WIFI_DISCONNECTED", "NETWORK_ETHERNET_DISCONNECTED", etc). 
        """
        return self._State


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'NetworkInfoInterface:'
        if self._Name and len(self._Name) > 0: msg = '%s name="%s"' % (msg, str(self._Name))
        if self._InterfaceType and len(self._InterfaceType) > 0: msg = '%s type="%s"' % (msg, str(self._InterfaceType))
        if self._IpAddress and len(self._IpAddress) > 0: msg = '%s ipAddress="%s"' % (msg, str(self._IpAddress))
        if self._MacAddress and len(self._MacAddress) > 0: msg = '%s macAddress="%s"' % (msg, str(self._MacAddress))
        if self._Ssid and len(self._Ssid) > 0: msg = '%s ssid="%s"' % (msg, str(self._Ssid))
        if self._State and len(self._State) > 0: msg = '%s state="%s"' % (msg, str(self._State))
        return msg 
