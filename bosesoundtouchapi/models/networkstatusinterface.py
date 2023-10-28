# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind

@export
class NetworkStatusInterface:
    """
    SoundTouch device NetworkStatusInterface configuration object.
       
    This class contains the attributes and sub-items that represent a
    single network interface configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._bindings = []

        if (root is None):
            pass  # no other parms to process.
        else:

            # base fields.
            self._FrequencyKhz:str = _xmlFind(root, 'frequencyKHz')
            self._Kind:str = _xmlFind(root, 'kind')
            self._MacAddress:str = _xmlFind(root, 'mac-addr')
            self._Name:str = _xmlFind(root, 'name')
            self._Rssi:str = _xmlFind(root, 'rssi')
            self._IsRunning:bool = bool(_xmlFind(root, 'running', default='false') == 'true')
            self._Ssid:str = _xmlFind(root, 'ssid')

            for binding in root.find('bindings'):
                self._bindings.append(_xmlFind(binding, 'ipv4address'))


    def __getitem__(self, key) -> str:
        return self._bindings[key]


    def __setitem__(self, key, value):
        self._bindings[key] = value


    def __iter__(self):
        return iter(self._bindings)


    def __len__(self) -> int:
        return len(self._bindings)


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def FrequencyKhz(self) -> str:
        """ 
        The frequency (in KiloHertz) the network uses to communicate with a 
        wireless router (e.g. 2452000 = 2.4GHz, etc). 
        """
        return self._FrequencyKhz


    @property
    def IsRunning(self) -> bool:
        """ True if the network connection is active; otherwise, False. """
        return self._IsRunning


    @property
    def Kind(self) -> str:
        """ The kind of network connection that is established (e.g. "Wired", "Wireless", etc). """
        return self._Kind 


    @property
    def MacAddress(self) -> str:
        """ The MAC address (media access control address) assigned to the device. """
        return self._MacAddress


    @property
    def Name(self) -> str:
        """ Network interface name (e.g. "etho0", etc). """
        return self._Name


    @property
    def Rssi(self) -> str:
        """ 
        Received Signal Strength Indicator status of the network connection (e.g. "good", etc).   
        This is a measurement of how well your device can receive a wireless
        network signal, and determines how good the wireless connection is.
        """
        return self._Rssi


    @property
    def Ssid(self) -> str:
        """ The network service set identifier (SSID) the device is connected to. """
        return self._Ssid


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'NetworkStatusInterface:'
        if self._Name and len(self._Name) > 0: msg = '%s name="%s"' % (msg, str(self._Name))
        if self._MacAddress and len(self._MacAddress) > 0: msg = '%s macAddress="%s"' % (msg, str(self._MacAddress))
        if self._IsRunning: msg = '%s running="%s"' % (msg, str(self._IsRunning).lower())
        if self._Kind and len(self._Kind) > 0: msg = '%s kind="%s"' % (msg, str(self._Kind))
        if self._Ssid and len(self._Ssid) > 0: msg = '%s ssid="%s"' % (msg, str(self._Ssid))
        if self._Rssi and len(self._Rssi) > 0: msg = '%s rssi="%s"' % (msg, str(self._Rssi))
        if self._FrequencyKhz and len(self._FrequencyKhz) > 0: msg = '%s frequencyKHz="%s"' % (msg, str(self._FrequencyKhz))
        return msg
