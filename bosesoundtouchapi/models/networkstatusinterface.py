# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindBool

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
        self._Bindings:list[str] = []
        self._FrequencyKhz:str = None
        self._Kind:str = None
        self._MacAddress:str = None
        self._Name:str = None
        self._Rssi:str = None
        self._IsRunning:bool = None
        self._Ssid:str = None

        if (root is None):

            pass

        else:

            self._FrequencyKhz = _xmlFind(root, 'frequencyKHz')
            self._Kind = _xmlFind(root, 'kind')
            self._MacAddress = _xmlFind(root, 'mac-addr')
            self._Name = _xmlFind(root, 'name')
            self._Rssi = _xmlFind(root, 'rssi')
            self._IsRunning = _xmlFindBool(root, 'running')
            self._Ssid = _xmlFind(root, 'ssid')

            for binding in root.find('bindings'):
                self._Bindings.append(_xmlFind(binding, 'ipv4address'))


    def __getitem__(self, key) -> str:
        return self._Bindings[key]


    def __setitem__(self, key, value):
        self._Bindings[key] = value


    def __iter__(self):
        return iter(self._Bindings)


    def __len__(self) -> int:
        return len(self._Bindings)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
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


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'frequency_khz': self._FrequencyKhz,
            'kind': self._Kind,
            'mac_address': self._MacAddress,
            'name': self._Name,
            'rssi': self._Rssi,
            'is_running': self._IsRunning,
            'ssid': self._Ssid,
            'bindings': [ item for item in self._Bindings ],
        }
        return result
        

    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'NetworkStatusInterface:'
        if self._Name is not None and len(self._Name) > 0: msg = '%s name="%s"' % (msg, str(self._Name))
        if self._MacAddress is not None and len(self._MacAddress) > 0: msg = '%s macAddress="%s"' % (msg, str(self._MacAddress))
        if self._IsRunning is not None: msg = '%s running="%s"' % (msg, str(self._IsRunning).lower())
        if self._Kind is not None and len(self._Kind) > 0: msg = '%s kind="%s"' % (msg, str(self._Kind))
        if self._Ssid is not None and len(self._Ssid) > 0: msg = '%s ssid="%s"' % (msg, str(self._Ssid))
        if self._Rssi is not None and len(self._Rssi) > 0: msg = '%s rssi="%s"' % (msg, str(self._Rssi))
        if self._FrequencyKhz is not None and len(self._FrequencyKhz) > 0: msg = '%s frequencyKHz="%s"' % (msg, str(self._FrequencyKhz))
        return msg
