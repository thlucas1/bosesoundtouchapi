# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind
from .infonetworkinfo import InformationNetworkInfo
from .component import Component


@export
class Information:
    """
    SoundTouch device Information configuration object.
       
    This class contains the attributes and sub-items that represent a
    Information configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Components:list[Component] = []
        self._CountryCode:str = None
        self._DeviceId:str = None
        self._DeviceName:str = None
        self._DeviceType:str = None
        self._MacAddress:str = None
        self._ModuleType:str = None
        self._NetworkInfo:list[InformationNetworkInfo] = []
        self._RegionCode:str = None
        self._StreamingAccountUUID:str = None
        self._StreamingUrl:str = None
        self._Variant:str = None
        self._VariantMode:str = None

        if (root is None):

            # nothing to do - always build it from a response.
            pass
        
        else:

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
            elmNode:Element = root.find('components')
            if elmNode is not None:
                for component in elmNode.findall('component'):
                    self._Components.append(Component(root=component))

            # load device details - network info list.
            for info in root.findall('networkInfo'):
                self._NetworkInfo.append(InformationNetworkInfo(info))


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()

        
    @property
    def Components(self) -> list[Component]:
        """
        List of `Component` objects containing various information about the 
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
    def NetworkInfo(self) -> list[InformationNetworkInfo]:
        """
        List of `SoundTouchNetworkConfig` objects containing the current network configuration 
        of the device.
        """
        return self._NetworkInfo


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


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'Info:'
        if self._DeviceId is not None and len(self._DeviceId) > 0: msg = '%s\nDeviceId="%s"' % (msg, str(self._DeviceId))
        if self._DeviceName is not None and len(self._DeviceName) > 0: msg = '%s\nDeviceName="%s"' % (msg, str(self._DeviceName))
        if self._DeviceType is not None and len(self._DeviceType) > 0: msg = '%s\nDeviceType="%s"' % (msg, str(self._DeviceType))
        if self._MacAddress is not None and len(self._MacAddress) > 0: msg = '%s\nMacAddress="%s"' % (msg, str(self._MacAddress))
        if self._CountryCode is not None and len(self._CountryCode) > 0: msg = '%s\nCountryCode="%s"' % (msg, str(self._CountryCode))
        if self._RegionCode is not None and len(self._RegionCode) > 0: msg = '%s\nRegionCode="%s"' % (msg, str(self._RegionCode))
        if self._ModuleType is not None and len(self._ModuleType) > 0: msg = '%s\nModuleType="%s"' % (msg, str(self._ModuleType))
        if self._VariantMode is not None and len(self._VariantMode) > 0: msg = '%s\nVariantMode="%s"' % (msg, str(self._VariantMode))
        if self._Variant is not None and len(self._Variant) > 0: msg = '%s\nVariant="%s"' % (msg, str(self._Variant))
        if self._StreamingUrl is not None and len(self._StreamingUrl) > 0: msg = '%s\nStreamingUrl="%s"' % (msg, str(self._StreamingUrl))
        if self._StreamingAccountUUID is not None and len(self._StreamingAccountUUID) > 0: msg = '%s\nStreamingAccountUUID="%s"' % (msg, str(self._StreamingAccountUUID))
        
        if includeItems == True:
            
            msg = "%s\n\nDevice NetworkInfos: (%d items)" % (msg, len(self._NetworkInfo))
            item:InformationNetworkInfo
            for item in self._NetworkInfo:
                msg = "%s\n- %s" % (msg, item.ToString())

            msg = "%s\n\nDevice Components: (%d items)" % (msg, len(self._Components))
            item:Component
            for item in self._Components:
                msg = "%s\n- %s" % (msg, item.ToString())
                
        else:
            
            msg = "%s\nNetworkInfo: (%d items)" % (msg, len(self._NetworkInfo))
            msg = "%s\nComponents: (%d items)" % (msg, len(self._Components))
            
        return msg 
    