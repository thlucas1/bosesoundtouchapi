from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    systemTimeout:SystemTimeout = client.GetSystemTimeout()
    print(systemTimeout.ToString())

    # get cached configuration, refreshing from device if needed.
    systemTimeout:SystemTimeout = client.GetSystemTimeout(False)
    print("\nCached configuration:\n%s" % systemTimeout.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.systemtimeout.Path in client.ConfigurationCache:
        systemTimeout:SystemTimeout = client.ConfigurationCache[SoundTouchNodes.systemtimeout.Path]
        print("\nCached configuration, direct:\n%s" % systemTimeout.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
