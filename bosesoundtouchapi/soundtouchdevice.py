# external package imports.
import re
import telnetlib 
from urllib3 import PoolManager, ProxyManager, Timeout, HTTPResponse
from xml.etree.ElementTree import Element, fromstring

# our package imports.
from .bstappmessages import BSTAppMessages
from .bstutils import export
from .soundtoucherror import SoundTouchError
from .models import Component, Information, InformationNetworkInfo, SupportedUrls, SupportedUrl
from .uri.soundtouchnodes import SoundTouchNodes
from .uri.soundtouchuri import SoundTouchUri, SoundTouchUriTypes
from .bstconst import (
    MSG_TRACE_DEVICE_COMMAND_WITH_PARM
)


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
                pattern for a IP V4 network address: r"\\d{1,3}([.]\\d{1,3}){3}".
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
        self._ConnectTimeout:int = connectTimeout
        self._Information:Information = Information()
        self._Host:str = host
        self._Port:int = int(port)
        self._SupportedUris:list[SoundTouchUri] = []
        self._SupportedUrls:SupportedUrls = None
        self._UnknownUrlNames:list[str] = []
        self._UnSupportedUrlNames:list[str] = []

        try:

            _logsi.LogVerbose("Initializing SoundTouch device.")
            
            # validations.
            if (host is None) or (not re.match(RE_IPV4_ADDRESS, host)):
                raise SoundTouchError(BSTAppMessages.BST_HOST_ADDRESS_INVALID % (host), None, _logsi)

            # assign the proxy manager used for http requests and responses.
            manager = proxyManager 
            if proxyManager is None:
        
                # create new pool manager with specified timeouts and limits.
                # note that we do not need many connections for the device class, as client will
                # be the heavy lifter and consuming the most connections.
                timeout = Timeout(connect=float(connectTimeout), read=None)
                manager = PoolManager(headers={'User-Agent': 'BoseSoundTouchApi/1.0.0'},
                                      timeout=timeout,
                                      num_pools=10,   # number of connection pools to allocate.
                                      maxsize=5,      # maximum number of connections to keep in the pool.
                                      block=True      # limit number of connections to the device.
                                     )
        
            # get SoundTouch device information; if it fails then we are done.
            _logsi.LogVerbose("Retrieving SoundTouch device information.")
            reqUrl:str = f'http://{host}:{port}/info'
            response:HTTPResponse = manager.request('GET', reqUrl)
            if response.status != 200:
                raise SoundTouchError("Could not retrieve SoundTouch device info: (%s) - '%s'" % (response.status, reqUrl), None, _logsi)

            # convert xml string response to xmltree Element and create information object.
            info:Element = fromstring(response.data)
            self._Information:Information = Information(root=info)
            response.close()
        
            # get SoundTouch supported url information; if it fails then we are done.
            _logsi.LogVerbose("Retrieving SoundTouch device supported URI list.")
            reqUrl:str = f'http://{host}:{port}/supportedURLs'
            response:HTTPResponse = manager.request('GET', reqUrl)
            if response.status != 200:
                raise SoundTouchError("Could not retrieve SoundTouch device supported urls: (%s) - '%s'" % (response.status, reqUrl), None, _logsi)
            
            # load supported url's list.
            elmNode:Element = fromstring(response.data)
            self._SupportedUrls = SupportedUrls(root=elmNode)

            # get list of ALL supported SoundTouch uri's that are possible regardless of device type.
            # we will add all of the 'request' type names to the UnSupportedUrlNames list, then 
            # filter them out below based upon what is returned by the device '/supportedUrls' call.  
            # this will leave a list of 'request' type names that are NOT supported by the device.
            allUris:dict = SoundTouchNodes._AllUris
            EVENT_TYPE:str = SoundTouchUriTypes.OP_TYPE_EVENT.name
            for name in allUris.keys():
                uri:SoundTouchUri = allUris[name]
                if uri.UriType != EVENT_TYPE:
                    self._UnSupportedUrlNames.append(name)
        
            # load the list of SoundTouch uri's that THIS device supports.
            # it could be everything in the ALL supported uri's list, but probably not as
            # SoundTouch devices can support different features.
            url:SupportedUrl
            for url in self._SupportedUrls.Urls:
                name:str = url.Location[1:]               # drop the forward slash prefix.
                if name in allUris:
                    if name in self._UnSupportedUrlNames: # in case the name is listed multiple times.
                        self._UnSupportedUrlNames.remove(name)
                        self._SupportedUris.append(allUris[name])
                else:
                    if name not in self._UnknownUrlNames: # in case the name is listed multiple times.
                        self._UnknownUrlNames.append(name)

            response.close()
            
            if _logsi.IsOn(SILevel.Verbose):
                _logsi.LogObject(SILevel.Verbose, "SoundTouch Device object: '%s' (%s)" % (self.DeviceName, self.Host), self)
                
        except SoundTouchError: raise  # pass handled exceptions on thru
        except Exception as ex:
        
            # format unhandled exception.
            raise SoundTouchError(BSTAppMessages.UNHANDLED_EXCEPTION.format("SoundTouchDevice.__init__", str(ex)), logsi=_logsi)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    def __iter__(self):
        return iter(self.Components)


    @property
    def Components(self) -> list[Component]:
        """
        List of `Component` objects containing various information about the 
        device's components (e.g. SCM, LPM, BASS, etc).
        """
        return self._Information._Components


    @property
    def ConnectTimeout(self) -> int:
        """ 
        Controls how long (in seconds) a connection request is allowed to run before being aborted.  
        Only valid if the proxy argument is null (e.g. default proxy manager is used) on the class
        constructor.
        """
        return self._ConnectTimeout


    @property
    def CountryCode(self) -> str:
        """
        Country code of the device as assigned by the manufacturer (e.g. 'US', etc). 
        """
        return self._Information._CountryCode


    @property
    def DeviceId(self) -> str:
        """
        Unique device identifier as assigned by the manufacturer (e.g. '9070658C9D4A', etc).
        """
        return self._Information._DeviceId

    @property
    def DeviceName(self) -> str:
        """ 
        Friendly name assigned to the SoundTouch device (e.g. 'Home Theater SoundBar', etc). 
        """
        return self._Information._DeviceName

    @property
    def DeviceType(self) -> str:
        """ 
        Type of device as assigned by the manufacturer (e.g. 'SoundTouch 10', 'SoundTouch 300', etc). 
        """
        return self._Information._DeviceType


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

        Example with Host = '192.168.1.81':  
        `http://192.168.1.81/logread.dat`
        """
        return f'http://{self.Host}/logread.dat'


    @property
    def MacAddress(self) -> str:
        """ MAC address (media access control address) assigned to the device. """
        return self._Information._MacAddress


    @property
    def ModuleType(self) -> str:
        """ 
        Radio module type used in the device, as assigned by the manufacturer (e.g. 'SM2', etc). 
        """
        return self._Information._ModuleType


    @property
    def NetworkInfo(self) -> list[InformationNetworkInfo]:
        """
        List of `InformationNetworkInfo` objects containing the current network configuration 
        of the device.
        """
        return self._Information._NetworkInfo


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
        return self._Information._RegionCode


    @property
    def StreamingAccountUUID(self) -> str:
        """ 
        Bose Streaming account UUID, as assigned by the manufacturer (e.g. '1234567', etc). 
        """
        return self._Information._StreamingAccountUUID


    @property
    def StreamingUrl(self) -> str:
        """ 
        Bose Streaming URL, as assigned by the manufacturer (e.g. 'https://streaming.bose.com', etc). 
        """
        return self._Information._StreamingUrl


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

        Example with Host = '192.168.1.81':  
        `http://192.168.1.81/pts.dat`
        """
        return f'http://{self.Host}/pts.dat'


    @property
    def UnknownUrlNames(self) -> list[str]:
        """
        List of url names that the device support, but are NOT recognized by the SoundTouch
        API.
        """
        return self._UnknownUrlNames


    @property
    def UnSupportedUrlNames(self) -> list[str]:
        """
        List of url names that are NOT supported by the device.
        """
        return self._UnSupportedUrlNames


    @property
    def UpnpUrl(self) -> str:
        """ 
        Universal Plug and Play (UPnP) root URL for this device.

        The document located at the returned URL contains additional information about
        methods and properties that can be used with UPnP.
        
        The format of the returned url is:  
        `http://{Host}:8091/XD/BO5EBO5E-F00D-F00D-FEED-{DeviceId}.xml`

        Example with Host = '192.168.1.81', DeviceId = 'E8EB11B9B723':  
        'http://192.168.1.80:8091/XD/BO5EBO5E-F00D-F00D-FEED-E8EB11B9B723.xml'
        """
        return f'http://{self.Host}:8091/XD/BO5EBO5E-F00D-F00D-FEED-{self.DeviceId}.xml'


    @property
    def Variant(self) -> str:
        """ 
        Variant value (e.g. 'ginger', etc). 
        """
        return self._Information._Variant


    @property
    def VariantMode(self) -> str:
        """ 
        Variant mode value (e.g. 'noap', etc). 
        """
        return self._Information._VariantMode


    def GetComponents(self, componentCategory:str) -> Component:
        """
        Iterates over all components discovered at class initialization that match 
        the given category.
        
        Args:
            componentCategory (str):
                The  component's category
                
        Returns:
            An iterator over the filtered `Component` components.
            
        This yields a device component for the given category.
        """
        if not componentCategory:
            return None

        for component in filter(lambda x: x and x.Category == componentCategory, self.Components):
            yield component


    def RebootDevice(self, sshPort:int=17000) -> str:
        """        
        Reboots the operating system of the SoundTouch device.
        
        Args:
            sshPort (int):
                SSH port to connect to; default is 17000.
                
        Returns:
            The SSH server response, in string format.
                
        This method will open a telnet connection to the SoundTouch SSH server
        running on the device (port 17000).  It will then issue a `sys reboot`
        command to reboot the device.  The telnet session will fail if any other
        process has a telnet session open to the device; this is a SoundTouch
        device limitation, as only one SSH session is allowed per device.
        
        If successful, all communication with the device will be lost while the 
        device is rebooting. SoundTouch web-services API connectivity should be 
        restored within 45 - 60 seconds if the reboot is successful.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchDevice/RebootDevice.py
        ```
        </details>
        """
        response:str = None
        conn = None
        
        try:
            
            _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("RebootDevice", self.Host, self.DeviceName))
            
            # open a connection to the ssh server running on the device (port 17000 default).
            conn = telnetlib.Telnet(self.Host, sshPort) 

            # send reboot system command.
            conn.write(b"sys reboot\n")
        
            # receive response; decode if bytes received (expected).
            response = conn.read_all()
            if isinstance(response, bytes):
                response = response.decode(encoding='utf-8')
            _logsi.LogVerbose("SSH Server response:\n%s" % response)
            
        except Exception as ex:
            
            # format unhandled exception.
            raise SoundTouchError(BSTAppMessages.UNHANDLED_EXCEPTION.format("SoundTouchDevice.RebootDevice", str(ex)), logsi=_logsi)

        finally:
            
            if conn is not None:
                conn.close()
            conn = None
        
        return response
        
        
    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'SoundTouchDevice:'
        msg = '%s Host="%s"' % (msg, self._Host)
        msg = '%s DeviceName="%s"' % (msg, self.DeviceName)
        msg = '%s DeviceId="%s"' % (msg, self.DeviceId)
        msg = '%s SupportedUrisCount=%d' % (msg, len(self.SupportedUris))
        if len(self.UnSupportedUrlNames) > 0:
            msg = "%s UnSupportedUrlNamesCount=%d" % (msg, len(self.UnSupportedUrlNames))
        if len(self.UnknownUrlNames) > 0:
            msg = "%s UnknownUrlNames=%d" % (msg, len(self.UnknownUrlNames))
        
        if includeItems == True:
            
            msg = "%s\n\nDevice %s" % (msg, self._Information.ToString(True))
            
            msg = "%s\n\nDevice UnSupportedUrlNames (%d items)" % (msg, len(self.UnSupportedUrlNames))
            item:str
            for item in self.UnSupportedUrlNames:
                msg = "%s\n- %s" % (msg, item)
            
            msg = "%s\n\nDevice UnknownUrlNames (%d items)" % (msg, len(self.UnknownUrlNames))
            item:str
            for item in self.UnknownUrlNames:
                msg = "%s\n- %s" % (msg, item)
            
            msg = "%s\n\nDevice SupportedUrlNames (%d items)" % (msg, len(self.SupportedUris))
            item:SoundTouchUri
            for item in self.SupportedUris:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
