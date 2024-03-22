from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    name:SimpleConfig = client.GetName()
    print(name.ToString())
    print("\nDevice Name = '%s'" % name.Value)

    # get cached configuration, refreshing from device if needed.
    name:SimpleConfig = client.GetName(False)
    print("\nCached configuration:\n%s" % name.ToString())
    print("\nDevice Name = '%s'" % name.Value)

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.name.Path in client.ConfigurationCache:
        name:SimpleConfig = client.ConfigurationCache[SoundTouchNodes.name.Path]
        print("\nCached configuration, direct:\n%s" % name.ToString())
        print("\nDevice Name = '%s'" % name.Value)
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
