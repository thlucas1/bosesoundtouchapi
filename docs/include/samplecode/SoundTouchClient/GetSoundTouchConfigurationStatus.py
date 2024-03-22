from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    config:SoundTouchConfigurationStatus = client.GetSoundTouchConfigurationStatus()
    print(config.ToString())

    # get cached configuration, refreshing from device if needed.
    config:SoundTouchConfigurationStatus = client.GetSoundTouchConfigurationStatus(False)
    print("\nCached configuration:\n%s" % config.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.soundTouchConfigurationStatus.Path in client.ConfigurationCache:
        config:SoundTouchConfigurationStatus = client.ConfigurationCache[SoundTouchNodes.soundTouchConfigurationStatus.Path]
        print("\nCached configuration, direct:\n%s" % config.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
