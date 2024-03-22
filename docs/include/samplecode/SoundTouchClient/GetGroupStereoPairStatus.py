from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    group:Group = client.GetGroupStereoPairStatus()
    print(group.ToString(True))

    # get cached configuration, refreshing from device if needed.
    group:Group = client.GetGroupStereoPairStatus(False)
    print("\nCached configuration:\n%s" % group.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.getGroup.Path in client.ConfigurationCache:
        group:Group = client.ConfigurationCache[SoundTouchNodes.getGroup.Path]
        print("\nCached configuration, direct:\n%s" % group.ToString(True))
                       
except Exception as ex:

    print("** Exception: %s" % str(ex))
