from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    networkInfo:NetworkInfo = client.GetNetworkInfo()
    print(networkInfo.ToString(True))

    # get cached configuration, refreshing from device if needed.
    networkInfo:NetworkInfo = client.GetNetworkInfo(False)
    print("\nCached configuration:\n%s" % networkInfo.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.networkInfo.Path in client.ConfigurationCache:
        networkInfo:NetworkInfo = client.ConfigurationCache[SoundTouchNodes.networkInfo.Path]
        print("\nCached configuration, direct:\n%s" % networkInfo.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
