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
    print(nowPlayingStatus.ToString())

    # get cached configuration, refreshing from device if needed.
    nowPlayingStatus:NowPlayingStatus = client.GetNowPlayingStatus(False)
    print("\nCached configuration:\n%s" % nowPlayingStatus.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.nowPlaying.Path in client.ConfigurationCache:
        nowPlayingStatus:NowPlayingStatus = client.ConfigurationCache[SoundTouchNodes.nowPlaying.Path]
        print("\nCached configuration, direct:\n%s" % nowPlayingStatus.ToString())

except Exception as ex:

    print("** Exception: %s" % str(ex))
