from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    config:SoftwareUpdateQueryResponse = client.GetSoftwareUpdateStatus()
    print(config.ToString())

    # get cached configuration, refreshing from device if needed.
    config:SoftwareUpdateQueryResponse = client.GetSoftwareUpdateStatus(False)
    print("\nCached configuration:\n%s" % config.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.swUpdateQuery.Path in client.ConfigurationCache:
        config:SoftwareUpdateQueryResponse = client.ConfigurationCache[SoundTouchNodes.swUpdateQuery.Path]
        print("\nCached configuration, direct:\n%s" % config.ToString())
           
except Exception as ex:

    print("** Exception: %s" % str(ex))
