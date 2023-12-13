# external package imports.
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty
from zeroconf import Zeroconf, ServiceBrowser, ServiceInfo, ServiceStateChange, IPVersion

# our package imports.
from .bstutils import export
from .soundtouchdevice import SoundTouchDevice

# get smartinspect logger reference; create a new session for this module name.
from smartinspectpython.siauto import SIAuto, SILevel, SISession
import logging
_logsi:SISession = SIAuto.Si.GetSession(__name__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__name__, True)
_logsi.SystemLogger = logging.getLogger(__name__)


@export
class SoundTouchDiscovery:
    """
    This class contains methods used to dicover SoundTouch devices on a local
    network.  The ZeroConf (aka MDNS, etc) service is used to detect devices,
    and adds them to a device list as they are discovered.

    Click the **Sample Code** links in the individual methods for sample code examples.
    """

    def __init__(self, areDevicesVerified:bool=False, printToConsole:bool=False) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            areDevicesVerified (bool):
                True to create a `SoundTouchDevice` instance for discovered devices, which
                verifies that the device can be accessed by a `SoundTouchClient` instance
                and basic information obtained about its capabilities;
                otherwise, False to just identify the IPV4 Address, Port, and Device Name.  
                Default is False.
                
            printToConsole (bool):
                True to print discovered device information to the console as the devices
                are discovered; otherwise, False to not print anything to the console.
                Default is False.
                
        Specify False for the `areDevicesVerified` argument if you want to speed up
        device discovery, as it takes extra time to verify device connections as they 
        are discovered.
        """
        # initialize instance properties.
        self._AreDevicesVerified:bool = areDevicesVerified
        self._DiscoveredDeviceNames:dict = {}
        self._PrintToConsole:bool = printToConsole
        self._VerifiedDevices:dict = {}


    def __getitem__(self, key):
        if repr(key) in self._DiscoveredDeviceNames:
            return self._DiscoveredDeviceNames[repr(key)]


    def __iter__(self):
        return iter(self._DiscoveredDeviceNames)


    def __len__(self) -> int:
        return len(self._DiscoveredDeviceNames)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def AreDevicesVerified(self) -> bool:
        """
        Determines if a `SoundTouchDevice` object is created for devices that are
        discovered.  This property is set by what is passed to the class constructor.
        
        If False, then the `VerifiedDevices` property will be empty;
        
        If True, then the `VerifiedDevices` property will contain a `SoundTouchDevice`
        instance for each device that was detected as part of the discovery process.
        """
        return self._AreDevicesVerified
        

    @property
    def DiscoveredDeviceNames(self) -> dict:
        """
        A dictionary of discovered device names that were detected by the discovery process.
        
        Dictionary keys will be in the form of "address:port", where "address" is the device
        ipv4 address and the "port" is the ipv4 port number the SoundTouch web-services api
        is listening on.
        
        Dictionary values will be the device names (e.g. "SoundTouch 10", etc.).  This will
        match the name of the device as displayed in the SoundTouch App.
        """
        return self._DiscoveredDeviceNames


    @property
    def VerifiedDevices(self) -> dict:
        """
        A dictionary of discovered `SoundTouchDevice` instances that were detected
        on the network.
        
        This property is only populated if the `IsDeviceObjectCreated` property is True.
        
        Dictionary keys will be in the form of "address:port", where "address" is the device
        ipv4 address and the "port" is the ipv4 port number the SoundTouch web-services api
        is listening on.
        
        Dictionary values will be `SoundTouchDevice` instances that represent the discovered
        device.
        """
        return self._VerifiedDevices


    def _OnServiceStateChange(self,
                              zeroconf:Zeroconf, 
                              service_type:str, 
                              name:str, 
                              state_change:ServiceStateChange
                              ) -> None:
        """
        Called by the zeroconf ServiceBrowser when a service state has changed (e.g. added,
        removed, or updated).  In our case, we only care about devices that were added.
        
        IMPORTANT - This method is executed on a different thread, so be careful about 
        multi-threaded operations!
        """
        serviceType:str = service_type
        serviceName:str = name
        serviceStateChange:ServiceStateChange = state_change
        
        # process by the state change value.
        if (serviceStateChange is ServiceStateChange.Added):
            _logsi.LogVerbose("Discovered SoundTouch device service: '%s' (%s:%s)" % (serviceName, serviceType, serviceStateChange))
            
            deviceName:str = (serviceName.split(".")[0])
            serviceInfo:ServiceInfo = zeroconf.get_service_info(service_type, serviceName)
            if serviceInfo is None:
                return
            
            # get list of displayable (parsed) ipv4 addresses that were detected; if none, then we are done.
            ipAddressList = serviceInfo.parsed_addresses(IPVersion.V4Only)
            if (ipAddressList is None):
                return
            
            # create device instances for each ipv4 address found.
            for deviceIpAddress in ipAddressList:
                
                devicePort:int = serviceInfo.port
                deviceKey:str = '%s:%i' % (deviceIpAddress, devicePort)
                _logsi.LogVerbose("Discovered SoundTouch device: %s - %s" % (deviceKey, deviceName))
                if (self._PrintToConsole == True):
                    print("Discovered SoundTouch device: %s - %s" % (deviceKey, deviceName))
                _logsi.LogObject(SILevel.Verbose, "Discovered SoundTouch device ServiceInfo: %s - %s" % (deviceKey, deviceName), serviceInfo) 
                
                # # trace service info propertys if desired.
                # # note that the property keys and values must first be decoded to utf-8 encoding.
                # if _logsi.IsOn(SILevel.Verbose):
                #     if serviceInfo.properties is not None:
                #         dspProperties:dict = {}
                #         for key, value in serviceInfo.properties.items():
                #             dspProperties[key.decode('utf-8')] = value.decode('utf-8')
                #         _logsi.LogDictionary(SILevel.Verbose, "Discovered SoundTouch device ServiceInfo.Properties: '%s' (%s:%i)" % (deviceName, deviceIpAddress, devicePort), dspProperties) 

                # add the device name to the list (if not already added) using its 
                # ipv4 address and port number as the key.
                if deviceKey not in self._DiscoveredDeviceNames.keys():
                    self._DiscoveredDeviceNames[deviceKey] = deviceName

                # are we verifying devices connections?  if so, then create a SoundTouchDevice
                # object, which will verify the connection and gather basic capabilities of the device.
                # we will also add the SoundTouchDevice instance using the same key as the device name list.
                if self._AreDevicesVerified == True:
                    if deviceKey not in self._VerifiedDevices.keys():
                        device:SoundTouchDevice = SoundTouchDevice(host=deviceIpAddress, port=devicePort)
                        self._VerifiedDevices[deviceKey] = device

        elif (serviceStateChange is ServiceStateChange.Removed):
            _logsi.LogVerbose("Discovered SoundTouch device removal (ignored): '%s' (%s:%s)", serviceName, serviceType, serviceStateChange)
            pass

        elif (serviceStateChange is ServiceStateChange.Updated):
            _logsi.LogVerbose("Discovered SoundTouch device update (ignored): '%s' (%s:%s)", serviceName, serviceType, serviceStateChange)
            pass


    def DiscoverDevices(self, timeout:int=5) -> dict:
        """
        Discover SoundTouch devices on the local network via the 
        ZeroConf (aka MDNS) service.

        Args:
            timeout (int): 
                Maximum amount of time to wait (in seconds) for the 
                discovery to complete.  
                Default is 5 seconds.
                
        Returns:
            A dictionary of discovered `SoundTouchDevice` objects.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchDiscovery/DiscoverDevices.py
        ```
        </details>
        """
        # using Queue as a timer (timeout functionality).
        discoveryQueueTimer = Queue()

        # create the zeroconf service and our listener callback.
        zeroconf:Zeroconf = Zeroconf()
        
        # create the zeroconf service browser that will start device discovery.
        _logsi.LogVerbose("Discovery of SoundTouch devices via Zeroconf is starting ...")
        ServiceBrowser(zeroconf, "_soundtouch._tcp.local.", handlers=[self._OnServiceStateChange])
        
        try:
            # give the ServiceBrowser time to discover
            discoveryQueueTimer.get(timeout=timeout)
            
        except Empty:
            
            # this is not really an exception, but more of an indicator that
            # the timeout has been reached.
            _logsi.LogVerbose("Discovery of SoundTouch devices via Zeroconf has ended.")
        
        return self._DiscoveredDeviceNames


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'SoundTouchDiscovery:'
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            for key, deviceName in self._DiscoveredDeviceNames.items():
                msg = "%s\n- %s - %s" % (msg, key, deviceName)
            
        return msg
