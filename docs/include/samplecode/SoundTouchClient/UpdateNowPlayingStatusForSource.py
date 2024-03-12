from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    nowPlayingStatus:NowPlayingStatus = client.GetNowPlayingStatus()
    print("Device Status:\n%s" % nowPlayingStatus.ToString())
    
    # set source-specific variables.
    source:str = "PRODUCT"
    sourceAccount:str = "TV"

    # update source-specific NowPlayingStatus.
    client.UpdateNowPlayingStatusForSource(source=source,
                                           sourceAccount=sourceAccount,
                                           album="My Album Name",
                                           artist="Artist Name",
                                           track="Track # 1",
                                           artUrl="")

    # get cached configuration directly from the configuration manager dictionary.
    cacheKey = "%s-%s:%s" % (SoundTouchNodes.nowPlaying.Path, source, sourceAccount)
    if cacheKey in client.ConfigurationCache:
        nowPlayingStatus:NowPlayingStatus = client.ConfigurationCache[cacheKey]
        print("\nSource-Specific Status (%s):\n%s" % (cacheKey, nowPlayingStatus.ToString()))

except Exception as ex:

    print("** Exception: %s" % str(ex))
