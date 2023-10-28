from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    bass:Bass = client.GetBass()
    print(bass.ToString())
    print("Bass Level = %d" % bass.Actual)

    # get cached configuration, refreshing from device if needed.
    bass:Bass = client.GetBass(False)
    print("\nCached configuration:\n%s" % bass.ToString())
    print("Bass Level = %d" % bass.Actual)

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.bass.Path in client.ConfigurationCache:
        bass:Bass = client.ConfigurationCache[SoundTouchNodes.bass.Path]
        print("\nCached configuration, direct:\n%s" % bass.ToString())
        print("Bass Level = %d" % bass.Actual)
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
