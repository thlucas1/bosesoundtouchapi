from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    networkStatus:NetworkStatus = client.GetNetworkStatus()
    print(networkStatus.ToString(True))

    # get cached configuration, refreshing from device if needed.
    networkStatus:NetworkStatus = client.GetNetworkStatus(False)
    print("\nCached configuration:\n%s" % networkStatus.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.netStats.Path in client.ConfigurationCache:
        networkStatus:NetworkStatus = client.ConfigurationCache[SoundTouchNodes.netStats.Path]
        print("\nCached configuration, direct:\n%s" % networkStatus.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
