from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get cached configuration objects, refreshing from device if needed.
    # since the refresh argument is false to all of these, they will request
    # real-time information from the device the first time, and then the
    # ConfigurationCache will be updated with the results.
    sourceList:SourceList = client.GetSourceList(False)
    
    print("\nCached configuration:\n%s" % sourceList.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.sources.Path in client.ConfigurationCache:
        sourceList:SourceList = client.ConfigurationCache[SoundTouchNodes.sources.Path]
        print("\nCached configuration, direct:\n%s" % sourceList.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
