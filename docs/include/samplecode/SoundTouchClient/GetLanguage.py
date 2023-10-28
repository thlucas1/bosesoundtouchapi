from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    language:SimpleConfig = client.GetLanguage()
    print(language.ToString())
    print("\nDevice Language = '%s'" % language.Value)

    # get cached configuration, refreshing from device if needed.
    language:SimpleConfig = client.GetLanguage(False)
    print("\nCached configuration:\n%s" % language.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.language.Path in client.ConfigurationCache:
        language:SimpleConfig = client.ConfigurationCache[SoundTouchNodes.language.Path]
        print("\nCached configuration, direct:\n%s" % language.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
