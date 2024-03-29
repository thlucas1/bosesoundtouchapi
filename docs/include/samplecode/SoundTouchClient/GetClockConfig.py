from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    clockConfig:ClockConfig = client.GetClockConfig()
    print(clockConfig.ToString())

    # get cached configuration, refreshing from device if needed.
    clockConfig:ClockConfig = client.GetClockConfig(False)
    print("\nCached configuration:\n%s" % clockConfig.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.clockDisplay.Path in client.ConfigurationCache:
        clockConfig:ClockConfig = client.ConfigurationCache[SoundTouchNodes.clockDisplay.Path]
        print("\nCached configuration, direct:\n%s" % clockConfig.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
