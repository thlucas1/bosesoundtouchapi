from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    info:Information = client.GetInformation()
    print(info.ToString())

    # get cached configuration, refreshing from device if needed.
    info:Information = client.GetInformation(False)
    print("\nCached configuration:\n%s" % info.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.info.Path in client.ConfigurationCache:
        info:Information = client.ConfigurationCache[SoundTouchNodes.info.Path]
        print("\nCached configuration, direct:\n%s" % info.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
