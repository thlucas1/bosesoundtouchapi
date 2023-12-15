from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    config:SupportedUrls = client.GetSupportedUrls()
    print(config.ToString(True))

    # get cached configuration, refreshing from device if needed.
    config:SupportedUrls = client.GetSupportedUrls(False)
    print("\nCached configuration:\n%s" % config.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.supportedURLs.Path in client.ConfigurationCache:
        config:SupportedUrls = client.ConfigurationCache[SoundTouchNodes.supportedURLs.Path]
        print("\nCached configuration, direct:\n%s" % config.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
