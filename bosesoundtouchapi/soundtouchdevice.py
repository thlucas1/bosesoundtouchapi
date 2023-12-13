# external package imports.
import re
from urllib3 import PoolManager, ProxyManager, Timeout, HTTPResponse
from xml.etree.ElementTree import Element, fromstring

# our package imports.
from .bstappmessages import BSTAppMessages
from .bstutils import export, _xmlFind
from .soundtouchdevicecomponent import SoundTouchDeviceComponent
from .soundtoucherror import SoundTouchError
from .models import InfoNetworkConfig
from .uri.soundtouchnodes import SoundTouchNodes
from .uri.soundtouchuri import SoundTouchUri

# get smartinspect logger reference; create a new session for this module name.
from smartinspectpython.siauto import SIAuto, SILevel, SISession
import logging
_logsi:SISession = SIAuto.Si.GetSession(__name__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__name__, True)
_logsi.SystemLogger = logging.getLogger(__name__)

RE_IPV4_ADDRESS = r"\d{1,3}([.]\d{1,3}){3}"

@export
class SoundTouchDevice:
    """
    This class contains device-related information, such as: host ip address,
    device name/type/id, a list of the device's components, a list of supported
    URLs and the current network configuration.

    The supported URLs are used by the SoundTouchClient to verify the requested
    URL is supported by the device.
    
    In order to load all properties and attributes of the SoundTouchDevice object, some
    special URLs will be queried:
        - http://host:8090/info (contains basic device information)
        - http://host:8090/supportedURLs (contains URL's supported by the device)
        
    Click the **Sample Code** links in the individual methods for sample code examples.
    """

    def __init__(self, host:str, connectTimeout:int=30, proxyManager:ProxyManager=None, port:int=8090) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            host (str):
                An Ipv4 address of the device; it must the following regular expression
                pattern for a IP V4 network address: r"\d{1,3}([.]\d{1,3}){3}".
            connectTimeout (int):
                Controls how long (in seconds) a connection request is allowed to run 
                before being aborted.  
                Only used if the proxy argument is null (e.g. default proxy manager is used).  
                Default is 30 seconds.
            proxyManager (Optional[urllib3.ProxyManager]):
                If a custom proxy should be used, it can be specified here;
                otherwise, a default urllib3.PoolManager is used for http requests / responses.
            port (int):
                IPV4 port number the Bose WebAPI is listening on for incoming requests on the device.
                Default is 8090, the standard WebAPI port number.
                
        Raises:
            SoundTouchError:
                SoundTouch host address is not recognized as a valid IPV4 network address.  
                Could not retrieve SoundTouch device information.  
                Could not retrieve SoundTouch device supported urls.  
                If the method fails for any other reason.
                
        This method loads all components and device properties allocated at the given 
        SoundTouch host.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchDevice/_ClassInit.py
        ```
        </details>
        """
        self._Components:list[SoundTouchDeviceComponent] = []
        self._CountryCode:str = None
        self._DeviceId:str = None
        self._DeviceName:str = None
        self._DeviceType:str = None
        self._Host:str = host
        self._MacAddress:str = None
        self._ModuleType:str = None
        self._NetworkInfo:list[InfoNetworkConfig] = []
        self._Port:int = int(port)
        self._RegionCode:str = None
        self._StreamingAccountUUID:str = None
        self._StreamingUrl:str = None
        self._SupportedUris:list[SoundTouchUri] = []
        self._Variant:str = None
        self._VariantMode:str = None

        try:

            _logsi.LogVerbose("Initializing SoundTouch device.")
            
            # validations.
            if (host is None) or (not re.match(RE_IPV4_ADDRESS, host)):
                raise SoundTouchError(BSTAppMessages.BST_HOST_ADDRESS_INVALID % (host), None, _logsi)

            # assign the proxy manager used for http requests and responses.
            manager = proxyManager 
            if proxyManager is None:
        
                # create new pool manager with specified timeouts.
                timeout = Timeout(connect=float(connectTimeout), read=None)
                manager = PoolManager(headers={'User-Agent': 'BoseSoundTouchApi/1.0.0'},
                                              timeout=timeout
                                              )
        
            # get SoundTouch device information; if it fails then we are done.
            _logsi.LogVerbose("Retrieving SoundTouch device information.")
            reqUrl:str = f'http://{host}:{port}/info'
            response:HTTPResponse = manager.request('GET', reqUrl)
            if response.status != 200:
                raise SoundTouchError("Could not retrieve SoundTouch device info: (%s) - '%s'" % (response.status, reqUrl), None, _logsi)

            # convert xml string response to xmltree Element object for parsing.
            root = fromstring(response.data)

            # load device details - base info.
            self._CountryCode = _xmlFind(root, 'countryCode')
            self._DeviceId = root.get('deviceID')
            self._DeviceName = _xmlFind(root, 'name')
            self._DeviceType = _xmlFind(root, 'type')
            self._ModuleType = _xmlFind(root, 'moduleType')
            self._RegionCode = _xmlFind(root, 'regionCode')
            self._StreamingAccountUUID = _xmlFind(root, 'margeAccountUUID')
            self._StreamingUrl = _xmlFind(root, 'margeURL')
            self._Variant = _xmlFind(root, 'variant')
            self._VariantMode = _xmlFind(root, 'variantMode')

            # default MAC address to the device id.
            self._MacAddress = self._DeviceId
         
            # load device details - components list.
            component:Element
            for component in root.find('components'):

                componentCategory:str = None
                elm:Element = component.find('componentCategory')
                if elm is not None: componentCategory = elm.text

                softwareVersion:str = None
                elm:Element = component.find('softwareVersion')
                if elm is not None: softwareVersion = elm.text

                serialNumber:str = None
                elm:Element = component.find('serialNumber')
                if elm is not None: serialNumber = elm.text

                obj = SoundTouchDeviceComponent(componentCategory, softwareVersion, serialNumber)
                self._Components.append(obj)

            # load device details - network info list.
            for info in root.findall('networkInfo'):
                self._NetworkInfo.append(InfoNetworkConfig(info))
        
            response.close()
        
            # get SoundTouch supported url information; if it fails then we are done.
            _logsi.LogVerbose("Retrieving SoundTouch device supported URI list.")
            reqUrl:str = f'http://{host}:{port}/supportedURLs'
            response:HTTPResponse = manager.request('GET', reqUrl)
            if response.status != 200:
                raise SoundTouchError("Could not retrieve SoundTouch device supported urls: (%s) - '%s'" % (response.status, reqUrl), None, _logsi)

            # get list of ALL supported SoundTouch uri's.
            allUris:dict = SoundTouchNodes._AllUris
        
            # load the list of SoundTouch uri's that THIS device supports.
            # it could be everything in the ALL supported uri's list, but probably not as
            # SoundTouch devices can support different features.
            for url_element in fromstring(response.data).findall('URL'):
                name:str = url_element.get('location', default='/')[1:]  # drop the forward slash prefix.
                if name is not None and name in allUris:
                    self._SupportedUris.append(allUris[name])

            response.close()
            
            if _logsi.IsOn(SILevel.Verbose):
                _logsi.LogObject(SILevel.Verbose, "SoundTouch Device object: '%s' (%s)" % (self.DeviceName, self.Host), self)
                
        except SoundTouchError: raise  # pass handled exceptions on thru
        except Exception as ex:
        
            # format unhandled exception.
            raise SoundTouchError(BSTAppMessages.UNHANDLED_EXCEPTION.format("__init__", str(ex)), logsi=_logsi)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    def __iter__(self):
        return iter(self.Components)


    @property
    def Components(self) -> list[SoundTouchDeviceComponent]:
        """
        List of `SoundTouchDeviceComponent` objects containing various information about the 
        device's components (e.g. SCM, LPM, BASS, etc).
        """
        return self._Components


    @property
    def CountryCode(self) -> str:
        """
        Country code of the device as assigned by the manufacturer (e.g. 'US', etc). 
        """
        return self._CountryCode


    @property
    def DeviceId(self) -> str:
        """
        Unique device identifier as assigned by the manufacturer (e.g. '9070658C9D4A', etc).
        """
        return self._DeviceId

    @property
    def DeviceName(self) -> str:
        """ 
        Friendly name assigned to the SoundTouch device (e.g. 'Home Theater SoundBar', etc). 
        """
        return self._DeviceName

    @property
    def DeviceType(self) -> str:
        """ 
        Type of device as assigned by the manufacturer (e.g. 'SoundTouch 10', 'SoundTouch 300', etc). 
        """
        return self._DeviceType


    @property
    def Host(self) -> str:
        """ 
        Ipv4 address of the SoundTouch device. 
        This property is read-only, and supplied by the class constructor.
        """
        return self._Host


    @property
    def LogReadUrl(self) -> str:
        """
        URL to download a logread file from this device.

        The format of the returned url is:  
        `http://{Host}:8091/logread.dat`

        Example with Host = '192.168.1.131':  
        `http://192.168.1.131/logread.dat`
        """
        return f'http://{self.Host}/logread.dat'


    @property
    def MacAddress(self) -> str:
        """ MAC address (media access control address) assigned to the device. """
        return self._MacAddress


    @property
    def ModuleType(self) -> str:
        """ 
        Radio module type used in the device, as assigned by the manufacturer (e.g. 'SM2', etc). 
        """
        return self._ModuleType


    @property
    def NetworkInfo(self) -> list[InfoNetworkConfig]:
        """
        List of `SoundTouchNetworkConfig` objects containing the current network configuration 
        of the device.
        """
        return self._NetworkInfo


    @property
    def Port(self) -> str:
        """ 
        Ipv4 address of the SoundTouch device. 
        This property is read-only, and supplied by the class constructor.
        """
        return self._Port


    @property
    def RegionCode(self) -> str:
        """ 
        Region code of the device as assigned by the manufacturer (e.g. 'US', etc). 
        """
        return self._RegionCode


    @property
    def StreamingAccountUUID(self) -> str:
        """ 
        Bose Streaming account UUID, as assigned by the manufacturer (e.g. '6146078', etc). 
        """
        return self._StreamingAccountUUID


    @property
    def StreamingUrl(self) -> str:
        """ 
        Bose Streaming URL, as assigned by the manufacturer (e.g. 'https://streaming.bose.com', etc). 
        """
        return self._StreamingUrl


    @property
    def SupportedUris(self) -> list[SoundTouchUri]:
        """
        List of `SoundTouchUri` objects that the device supports.
        
        These URI's are used by the SoundTouchClient class to obtain information from the 
        device (e.g. info, nowPlaying, etc).
        """
        return self._SupportedUris


    @property
    def PtsUrl(self) -> str: # str | None
        """
        URL to download a logread file.

        The format of the returned url is:  
        http://{Host}:8091/pts.dat

        Example with Host = '192.168.1.131':  
        `http://192.168.1.131/pts.dat`
        """
        return f'http://{self.Host}/pts.dat'


    @property
    def UpnpUrl(self) -> str:
        """ 
        Universal Plug and Play (UPnP) root URL for this device.

        The document located at the returned URL contains additional information about
        methods and properties that can be used with UPnP.
        
        The format of the returned url is:  
        `http://{Host}:8091/XD/BO5EBO5E-F00D-F00D-FEED-{DeviceId}.xml`

        Example with Host = '192.168.1.131', DeviceId = 'E8EB11B9B723':  
        'http://192.168.1.130:8091/XD/BO5EBO5E-F00D-F00D-FEED-E8EB11B9B723.xml'
        """
        return f'http://{self.Host}:8091/XD/BO5EBO5E-F00D-F00D-FEED-{self.DeviceId}.xml'


    @property
    def Variant(self) -> str:
        """ 
        Variant value (e.g. 'ginger', etc). 
        """
        return self._Variant


    @property
    def VariantMode(self) -> str:
        """ 
        Variant mode value (e.g. 'noap', etc). 
        """
        return self._VariantMode


    def GetComponents(self, componentCategory:str) -> SoundTouchDeviceComponent:
        """
        Iterates over all components discovered at class initialization that match 
        the given category.
        
        Args:
            componentCategory (str):
                The  component's category
                
        Returns:
            An iterator over the filtered `SoundTouchDeviceComponent` components.
            
        This yields a device component for the given category.
        """
        if not componentCategory:
            return None

        for component in filter(lambda x: x and x.Category == componentCategory, self.Components):
            yield component


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'SoundTouchDevice:'
        msg = "%s Host='%s'" % (msg, self._Host)
        msg = "%s DeviceName='%s'" % (msg, self._DeviceName)
        msg = "%s DeviceId='%s'" % (msg, self._DeviceId)
        msg = "%s (%d components)" % (msg, len(self._Components))
        
        if includeItems == True:
            item:SoundTouchDeviceComponent
            for item in self._Components:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
