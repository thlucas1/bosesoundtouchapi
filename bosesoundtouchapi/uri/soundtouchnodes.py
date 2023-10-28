# external package imports.
import sys

# our package imports.
from .soundtouchuri import SoundTouchUri
from .soundtouchuriscopes import SoundTouchUriScopes
from .soundtouchuritypes import SoundTouchUriTypes

# our package imports.
from .soundtouchuriscopes import SoundTouchUriScopes
from .soundtouchuritypes import SoundTouchUriTypes
from bosesoundtouchapi.bstutils import static_init



@static_init    # indicate we have a static init method.
class SoundTouchNodes:
    """
    This class contains all SoundTouch URI's that COULD be implemented by a Bose device. 
    """
    # The URI list was derived from the following files:
    # rootfs/opt/Bose/etc/HandCraftedWebServer-SoundTouch.xml
    # rootfs/opt/Bose/etc/WebServer-SoundTouch.xml
    
    # static properties.
    _AllUris:dict = {}
    """ 
    A dictionary of all possible SoundTouch uri's, mapped to their name, that
    could be used when accessing or updating a Bose SoundTouch device.
    """

    # URI node definitions (in alphabetical order).
    AbortSoftwareUpdate              = SoundTouchUri("AbortSoftwareUpdate")
    addGroup                         = SoundTouchUri("addGroup")
    addStation                       = SoundTouchUri("addStation")
    addStereoPair                    = SoundTouchUri("addStereoPair")
    addWirelessProfile               = SoundTouchUri("addWirelessProfile")
    addZoneSlave                     = SoundTouchUri("addZoneSlave")
    art                              = SoundTouchUri("art")
    audiodspcontrols                 = SoundTouchUri("audiodspcontrols")
    audioproductlevelcontrols        = SoundTouchUri("audioproductlevelcontrols")
    audioproducttonecontrols         = SoundTouchUri("audioproducttonecontrols")
    audiospeakerattributeandsetting  = SoundTouchUri("audiospeakerattributeandsetting")
    balance                          = SoundTouchUri("balance")
    bass                             = SoundTouchUri("bass")
    bassCapabilities                 = SoundTouchUri("bassCapabilities")
    bluetoothInfo                    = SoundTouchUri("bluetoothInfo")
    bookmark                         = SoundTouchUri("bookmark")
    cancelPairLightswitch            = SoundTouchUri("cancelPairLightswitch")
    capabilities                     = SoundTouchUri("capabilities")
    clearBluetoothPaired             = SoundTouchUri("clearBluetoothPaired")
    clearPairedList                  = SoundTouchUri("clearPairedList")
    clockDisplay                     = SoundTouchUri("clockDisplay")
    clockTime                        = SoundTouchUri("clockTime")
    criticalError                    = SoundTouchUri("criticalError", SoundTouchUriScopes.OP_SCOPE_PRIVATE)
    criticalErrorUpdate              = SoundTouchUri("criticalErrorUpdate", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    DSPMonoStereo                    = SoundTouchUri("DSPMonoStereo")
    enterBluetoothPairing            = SoundTouchUri("enterBluetoothPairing")
    enterPairingMode                 = SoundTouchUri("enterPairingMode")
    errorNotification                = SoundTouchUri("errorNotification", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    factoryDefault                   = SoundTouchUri("factoryDefault", SoundTouchUriScopes.OP_SCOPE_PRIVATE)
    genreStations                    = SoundTouchUri("genreStations")
    getActiveWirelessProfile         = SoundTouchUri("getActiveWirelessProfile")
    getBCOReset                      = SoundTouchUri("getBCOReset")
    getGroup                         = SoundTouchUri("getGroup")
    getZone                          = SoundTouchUri("getZone")
    groupUpdated                     = SoundTouchUri("groupUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    info                             = SoundTouchUri("info")
    introspect                       = SoundTouchUri("introspect")
    key                              = SoundTouchUri("key")
    language                         = SoundTouchUri("language")
    languageUpdated                  = SoundTouchUri("languageUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    listMediaServers                 = SoundTouchUri("listMediaServers")
    lowPowerStandby                  = SoundTouchUri("lowPowerStandby")
    LowPowerStandbyUpdate            = SoundTouchUri("LowPowerStandbyUpdate", SoundTouchUriScopes.OP_SCOPE_PRIVATE, SoundTouchUriTypes.OP_TYPE_EVENT)
    marge                            = SoundTouchUri("marge")
    masterMsg                        = SoundTouchUri("masterMsg")
    name                             = SoundTouchUri("name")
    nameSource                       = SoundTouchUri("nameSource")
    nameUpdated                      = SoundTouchUri("nameUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    navigate                         = SoundTouchUri("navigate")
    netStats                         = SoundTouchUri("netStats")
    networkInfo                      = SoundTouchUri("networkInfo")
    notification                     = SoundTouchUri("notification")
    nowPlaying                       = SoundTouchUri("nowPlaying")
    nowPlayingUpdated                = SoundTouchUri("nowPlayingUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    nowSelection                     = SoundTouchUri("nowSelection")
    nowSelectionUpdated              = SoundTouchUri("nowSelectionUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    pairLightswitch                  = SoundTouchUri("pairLightswitch")
    pdo                              = SoundTouchUri("pdo")
    performWirelessSiteSurvey        = SoundTouchUri("performWirelessSiteSurvey")
    playbackRequest                  = SoundTouchUri("playbackRequest")
    playNotification                 = SoundTouchUri("playNotification", SoundTouchUriScopes.OP_SCOPE_PRIVATE)
    powerManagement                  = SoundTouchUri("powerManagement")
    powersaving                      = SoundTouchUri("powersaving")
    presets                          = SoundTouchUri("presets")
    presetsUpdated                   = SoundTouchUri("presetsUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    productcechdmicontrol            = SoundTouchUri("productcechdmicontrol")
    producthdmiassignmentcontrols    = SoundTouchUri("producthdmiassignmentcontrols")
    pushCustomerSupportInfoToMarge   = SoundTouchUri("pushCustomerSupportInfoToMarge")
    rebroadcastlatencymode           = SoundTouchUri("rebroadcastlatencymode")
    recents                          = SoundTouchUri("recents")
    recentsUpdated                   = SoundTouchUri("recentsUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    removeGroup                      = SoundTouchUri("removeGroup")
    removeMusicServiceAccount        = SoundTouchUri("removeMusicServiceAccount")
    removePreset                     = SoundTouchUri("removePreset")
    removeStation                    = SoundTouchUri("removeStation")
    removeStereoPair                 = SoundTouchUri("removeStereoPair")
    removeZoneSlave                  = SoundTouchUri("removeZoneSlave")
    requestToken                     = SoundTouchUri("requestToken")
    search                           = SoundTouchUri("search")
    searchStation                    = SoundTouchUri("searchStation")
    select                           = SoundTouchUri("select")
    selectLastSoundTouchSource       = SoundTouchUri("selectLastSoundTouchSource")
    selectLastSource                 = SoundTouchUri("selectLastSource")
    selectLastWiFiSource             = SoundTouchUri("selectLastWiFiSource")
    selectLocalSource                = SoundTouchUri("selectLocalSource")
    selectPreset                     = SoundTouchUri("selectPreset")
    serviceAvailability              = SoundTouchUri("serviceAvailability")
    services                         = SoundTouchUri("services")
    setBCOReset                      = SoundTouchUri("setBCOReset")
    setComponentSoftwareVersion      = SoundTouchUri("setComponentSoftwareVersion", SoundTouchUriScopes.OP_SCOPE_PRIVATE)
    setMargeAccount                  = SoundTouchUri("setMargeAccount")
    setMusicServiceAccount           = SoundTouchUri("setMusicServiceAccount")
    setMusicServiceOAuthAccount      = SoundTouchUri("setMusicServiceOAuthAccount")
    setPairedStatus                  = SoundTouchUri("setPairedStatus")
    setPairingStatus                 = SoundTouchUri("setPairingStatus")
    setPower                         = SoundTouchUri("setPower")
    setProductSerialNumber           = SoundTouchUri("setProductSerialNumber", SoundTouchUriScopes.OP_SCOPE_PRIVATE)
    setProductSoftwareVersion        = SoundTouchUri("setProductSoftwareVersion", SoundTouchUriScopes.OP_SCOPE_PRIVATE)
    setup                            = SoundTouchUri("setup")
    setWiFiRadio                     = SoundTouchUri("setWiFiRadio", SoundTouchUriScopes.OP_SCOPE_PRIVATE)
    setZone                          = SoundTouchUri("setZone")
    slaveMsg                         = SoundTouchUri("slaveMsg")
    SoftwareUpdateExit               = SoundTouchUri("SoftwareUpdateExit")
    soundTouchConfigurationStatus    = SoundTouchUri("soundTouchConfigurationStatus")
    soundTouchConfigurationUpdated   = SoundTouchUri("soundTouchConfigurationUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    sourceDiscoveryStatus            = SoundTouchUri("sourceDiscoveryStatus")
    sources                          = SoundTouchUri("sources")
    sourcesUpdated                   = SoundTouchUri("sourcesUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    speaker                          = SoundTouchUri("speaker")
    standby                          = SoundTouchUri("standby")
    StartSoftwareUpdate              = SoundTouchUri("StartSoftwareUpdate")
    stationInfo                      = SoundTouchUri("stationInfo")
    storePreset                      = SoundTouchUri("storePreset")
    supportedURLs                    = SoundTouchUri("supportedURLs")
    swUpdateAbort                    = SoundTouchUri("swUpdateAbort")
    swUpdateCheck                    = SoundTouchUri("swUpdateCheck")
    swUpdateQuery                    = SoundTouchUri("swUpdateQuery")
    swUpdateStart                    = SoundTouchUri("swUpdateStart")
    swUpdateStatusUpdated            = SoundTouchUri("swUpdateStatusUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    systemtimeout                    = SoundTouchUri("systemtimeout")
    systemtimeoutcontrol             = SoundTouchUri("systemtimeoutcontrol")
    test                             = SoundTouchUri("test")
    testCommandBA                    = SoundTouchUri("testCommandBA", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    testCommandSU                    = SoundTouchUri("testCommandSU", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)
    trackInfo                        = SoundTouchUri("trackInfo")
    updateGroup                      = SoundTouchUri("updateGroup")
    userActivity                     = SoundTouchUri("userActivity", SoundTouchUriScopes.OP_SCOPE_PRIVATE)
    userActivityUpdate               = SoundTouchUri("userActivityUpdate", SoundTouchUriScopes.OP_SCOPE_PRIVATE, SoundTouchUriTypes.OP_TYPE_EVENT)
    userPlayControl                  = SoundTouchUri("userPlayControl")
    userRating                       = SoundTouchUri("userRating")
    userTrackControl                 = SoundTouchUri("userTrackControl")
    volume                           = SoundTouchUri("volume")
    zoneUpdated                      = SoundTouchUri("zoneUpdated", uriType=SoundTouchUriTypes.OP_TYPE_EVENT)


    @classmethod
    def static_init(cls) -> None:
        """ 
        Initializes a new static instance of the class.
        """
        # Note - at this point, you cannot call any of the static methods in this class,
        # as we are still in the initilization phase!

        # load all uri objects to a dictionary.
        #for uri_name, uri in sys.modules[__name__].__dict__.items():
        for uri_name, uri in cls.__dict__.items():
            if isinstance(uri, SoundTouchUri):
                cls._AllUris[uri_name] = uri
