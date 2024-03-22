from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    mediaServerList:MediaServerList = client.GetMediaServerList()
    print(mediaServerList.ToString(True))

    # get cached configuration, refreshing from device if needed.
    mediaServerList:MediaServerList = client.GetMediaServerList(False)
    print("\nCached configuration:\n%s" % mediaServerList.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.listMediaServers.Path in client.ConfigurationCache:
        mediaServerList:MediaServerList = client.ConfigurationCache[SoundTouchNodes.listMediaServers.Path]
        print("\nCached configuration, direct:\n%s" % mediaServerList.ToString(True))
        
    # sort the list (in place) by ServerId, ascending order.
    mediaServerList.MediaServers.sort(key=lambda x: (x.ServerId or "").lower(), reverse=False)
    print("\nList sorted by ServerId:\n%s" % mediaServerList.ToString(True))

except Exception as ex:

    print("** Exception: %s" % str(ex))
