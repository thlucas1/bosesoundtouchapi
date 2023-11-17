from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    config:SoftwareUpdateCheckResponse = client.GetSoftwareUpdateCheckInfo()
    print(config.ToString())

    # get cached configuration, refreshing from device if needed.
    config:SoftwareUpdateCheckResponse = client.GetSoftwareUpdateCheckInfo(False)
    print("\nCached configuration:\n%s" % config.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.swUpdateCheck.Path in client.ConfigurationCache:
        config:SoftwareUpdateCheckResponse = client.ConfigurationCache[SoundTouchNodes.swUpdateCheck.Path]
        print("\nCached configuration, direct:\n%s" % config.ToString())
           
except Exception as ex:

    print("** Exception: %s" % str(ex))
