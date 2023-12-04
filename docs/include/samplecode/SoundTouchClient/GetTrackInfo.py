from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    trackInfo:TrackInfo = client.GetTrackInfo()
    print(trackInfo.ToString())

    # get cached configuration, refreshing from device if needed.
    trackInfo:TrackInfo = client.GetTrackInfo(False)
    print("\nCached configuration:\n%s" % trackInfo.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.trackInfo.Path in client.ConfigurationCache:
        trackInfo:TrackInfo = client.ConfigurationCache[SoundTouchNodes.trackInfo.Path]
        print("\nCached configuration, direct:\n%s" % trackInfo.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
