from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    bassCapabilities:BassCapabilities = client.GetBassCapabilities()
    print(bassCapabilities.ToString())

    # get cached configuration, refreshing from device if needed.
    bassCapabilities:BassCapabilities = client.GetBassCapabilities(False)
    print("\nCached configuration:\n%s" % bassCapabilities.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.bassCapabilities.Path in client.ConfigurationCache:
        bassCapabilities:BassCapabilities = client.ConfigurationCache[SoundTouchNodes.bassCapabilities.Path]
        print("\nCached configuration, direct:\n%s" % bassCapabilities.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
