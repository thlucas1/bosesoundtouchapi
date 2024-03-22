from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    capabilities:Capabilities = client.GetCapabilities()
    print(capabilities.ToString())

    # get cached configuration, refreshing from device if needed.
    capabilities:Capabilities = client.GetCapabilities(False)
    print("\nCached configuration:\n%s" % capabilities.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.capabilities.Path in client.ConfigurationCache:
        capabilities:Capabilities = client.ConfigurationCache[SoundTouchNodes.capabilities.Path]
        print("\nCached configuration, direct:\n%s" % capabilities.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
