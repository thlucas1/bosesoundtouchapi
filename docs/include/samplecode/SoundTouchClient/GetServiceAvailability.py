from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    config:ServiceAvailability = client.GetServiceAvailability()
    print(config.ToString(True))

    # get cached configuration, refreshing from device if needed.
    config:ServiceAvailability = client.GetServiceAvailability(False)
    print("\nCached configuration:\n%s" % config.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.serviceAvailability.Path in client.ConfigurationCache:
        config:ServiceAvailability = client.ConfigurationCache[SoundTouchNodes.serviceAvailability.Path]
        print("\nCached configuration, direct:\n%s" % config.ToString(True))
        
    # sort the list (in place) by ServiceType, ascending order.
    config.Services.sort(key=lambda x: (x.ServiceType or "").lower(), reverse=False)
    print("\nList sorted by ServiceType:\n%s" % config.ToString(True))
           
    # sort the list (in place) by IsAvailable, ascending order.
    config.Services.sort(key=lambda x: x.IsAvailable or False, reverse=False)
    print("\nList sorted by IsAvailable:\n%s" % config.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
