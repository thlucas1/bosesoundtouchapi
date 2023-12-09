# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindBool

@export
class Capabilities:
    """
    SoundTouch device Capabilities configuration object.
       
    This class contains the attributes and sub-items that represent the 
    capabilities configuration of the device.      

    This class contains important configuration values, such as `IsWebSocketApiProxyCapable`
    which indicates whether the WebSocket notification API can be used.

    Next, a capabilities object shows whether a clock display is available
    or if the device can run in dual Mode.  Each device comes with different
    additional features, which are also stored in this class with a dict-like
    implementation with the following mapping: `self[cap.name] = cap.url`.
    """
    
    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Capabilities:dict = {}
        self._DeviceId:str = None
        self._IsBcoResetCapable:bool = None
        self._IsClockDisplayCapable:bool = None
        self._IsDisablePowerSavingCapable:bool = None
        self._IsDualModeCapable:bool = None
        self._IsLightSwitchCapable:bool = None
        self._IsLrStereoCapable:bool = None
        self._IsWebSocketApiProxyCapable:bool = None
        
        if (root is None):
            
            pass

        else:

            self._DeviceId = root.get('deviceID')
            self._IsBcoResetCapable = _xmlFindBool(root, 'bcoresetCapable', default=False)
            self._IsClockDisplayCapable = _xmlFindBool(root, 'clockDisplay', default=False)
            self._IsDisablePowerSavingCapable = _xmlFindBool(root, 'disablePowerSaving', default=False)
            self._IsDualModeCapable = _xmlFindBool(root, './networkConfig/dualMode', default=False)
            self._IsLightSwitchCapable = _xmlFindBool(root, 'lightswitch', default=False)
            self._IsLrStereoCapable = _xmlFindBool(root, 'lrStereoCapable', default=False)
            self._IsWebSocketApiProxyCapable = _xmlFindBool(root, './networkConfig/wsapiproxy', default=False)

            self._Capabilities = {}
            for cap in root.findall('capability'):
                self[cap.get('name')] = cap.get('url')


    def __getitem__(self, key):
        return self._Capabilities[key]


    def __setitem__(self, key, value):
        self._Capabilities[key] = value


    def __iter__(self) -> Iterator:
        return iter(self._Capabilities)


    def __len__(self) -> int:
        return len(self._Capabilities)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId
    

    @property
    def IsAudioDspControlsCapable(self) -> bool:
        """ Returns whether the device supports audiodspcontrols functionality. """
        return 'audiodspcontrols' in self._Capabilities


    @property
    def IsAudioProductLevelControlsCapable(self) -> bool:
        """ Returns whether the device supports audioproductlevelcontrols functionality. """
        return 'audioproductlevelcontrols' in self._Capabilities


    @property
    def IsAudioProductToneControlsCapable(self) -> bool:
        """ Returns whether the device supports audioproducttonecontrols functionality. """
        return 'audioproducttonecontrols' in self._Capabilities


    @property
    def IsAudioSpeakerAttributeAndSettingCapable(self) -> bool:
        """ Returns whether the device supports audiospeakerattributeandsetting functionality. """
        return 'audiospeakerattributeandsetting' in self._Capabilities


    @property
    def IsBcoResetCapable(self) -> bool:
        """ Returns whether the device contains a Bose coreset. """
        return self._IsBcoResetCapable


    @property
    def IsClockDisplayCapable(self) -> bool:
        """ Returns whether the clock display is available. """
        return self._IsClockDisplayCapable


    @property
    def IsDisablePowerSavingCapable(self) -> bool:
        """ Returns whether the power saving mode can be disabled. """
        return self._IsDisablePowerSavingCapable


    @property
    def IsDualModeCapable(self) -> bool:
        """ Returns whether the device can run in dual mode. """
        return self._IsDualModeCapable


    @property
    def IsLightSwitchCapable(self) -> bool:
        """ Returns whether the light switch can be used. """
        return self._IsLightSwitchCapable


    @property
    def IsLrStereoCapable(self) -> bool:
        """ Returns whether the device is left-right stereo capable. """
        return self._IsLrStereoCapable


    @property
    def IsProductCecHdmiControlCapable(self) -> bool:
        """ Returns whether the device supports productcechdmicontrol functionality. """
        return 'productcechdmicontrol' in self._Capabilities


    @property
    def IsProductHdmiAssignmentControlsCapable(self) -> bool:
        """ Returns whether the device supports producthdmiassignmentcontrols functionality. """
        return 'producthdmiassignmentcontrols' in self._Capabilities


    @property
    def IsReBroadcastLatencyModeCapable(self) -> bool:
        """ Returns whether the device supports rebroadcastlatencymode functionality. """
        return 'rebroadcastlatencymode' in self._Capabilities


    @property
    def IsSystemTimeoutCapable(self) -> bool:
        """ Returns whether the device supports systemtimeout functionality. """
        return 'systemtimeout' in self._Capabilities


    @property
    def IsSystemTimeoutControlCapable(self) -> bool:
        """ Returns whether the device supports systemtimeoutcontrol functionality. """
        return 'systemtimeoutcontrol' in self._Capabilities


    @property
    def IsWebSocketApiProxyCapable(self) -> bool:
        """ Returns whether the WebSocket API can be used on port 8080. """
        return self._IsWebSocketApiProxyCapable


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'Capabilities:'
        msg = '%s wsApiProxy=%s' % (msg, str(self._IsWebSocketApiProxyCapable).lower())
        msg = '%s lightswitch=%s' % (msg, str(self._IsLightSwitchCapable).lower())
        msg = '%s clockDisplay=%s' % (msg, str(self._IsClockDisplayCapable).lower())
        msg = '%s lrStereoCapable=%s' % (msg, str(self._IsLrStereoCapable).lower())
        msg = '%s bcoResetCapable=%s' % (msg, str(self._IsBcoResetCapable).lower())
        msg = '%s disablePowerSaving=%s' % (msg, str(self._IsDisablePowerSavingCapable).lower())
        msg = '%s dualMode=%s' % (msg, str(self._IsDualModeCapable).lower())
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            for item in self:
                msg = "%s\n- '%s' = '%s'" % (msg, str(item), str(self[item]))

        return msg 
