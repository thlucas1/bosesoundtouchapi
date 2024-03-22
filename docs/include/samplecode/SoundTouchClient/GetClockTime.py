from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    clockTime:ClockTime = client.GetClockTime()
    print(clockTime.ToString())

    # get cached configuration, refreshing from device if needed.
    clockTime:ClockTime = client.GetClockTime(False)
    print("\nCached configuration:\n%s" % clockTime.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.clockDisplay.Path in client.ConfigurationCache:
        clockTime:ClockTime = client.ConfigurationCache[SoundTouchNodes.clockDisplay.Path]
        print("\nCached configuration, direct:\n%s" % clockTime.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
