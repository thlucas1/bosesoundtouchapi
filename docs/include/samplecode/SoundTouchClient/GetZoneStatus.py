from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    zone:Zone = client.GetZoneStatus()
    print(zone.ToString(True))

    # get cached configuration, refreshing from device if needed.
    zone:Zone = client.GetZoneStatus(False)
    print("\nCached configuration:\n%s" % zone.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.getZone.Path in client.ConfigurationCache:
        zone:Zone = client.ConfigurationCache[SoundTouchNodes.getZone.Path]
        print("\nCached configuration, direct:\n%s" % zone.ToString(True))
                
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
