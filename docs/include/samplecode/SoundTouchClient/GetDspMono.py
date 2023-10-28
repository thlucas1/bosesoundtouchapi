from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    dspMonoStereoItem:DSPMonoStereoItem = client.GetDspMono()
    print(dspMonoStereoItem.ToString())

    # get cached configuration, refreshing from device if needed.
    dspMonoStereoItem:DSPMonoStereoItem = client.GetDspMono(False)
    print("\nCached configuration:\n%s" % dspMonoStereoItem.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.DSPMonoStereo.Path in client.ConfigurationCache:
        dspMonoStereoItem:DSPMonoStereoItem = client.ConfigurationCache[SoundTouchNodes.DSPMonoStereo.Path]
        print("\nCached configuration, direct:\n%s" % dspMonoStereoItem.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
