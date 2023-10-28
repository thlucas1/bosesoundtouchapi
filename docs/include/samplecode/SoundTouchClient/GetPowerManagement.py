from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    powerManagement:PowerManagement = client.GetPowerManagement()
    print(powerManagement.ToString())

    # get cached configuration, refreshing from device if needed.
    powerManagement:PowerManagement = client.GetPowerManagement(False)
    print("\nCached configuration:\n%s" % powerManagement.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.powerManagement.Path in client.ConfigurationCache:
        powerManagement:PowerManagement = client.ConfigurationCache[SoundTouchNodes.powerManagement.Path]
        print("\nCached configuration, direct:\n%s" % powerManagement.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
