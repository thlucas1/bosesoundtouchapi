from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    presetList:PresetList = client.GetPresetList()
    print(presetList.ToString(True))

    # get cached configuration, refreshing from device if needed.
    presetList:PresetList = client.GetPresetList(False)
    print("\nCached configuration:\n%s" % presetList.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.presets.Path in client.ConfigurationCache:
        presetList:PresetList = client.ConfigurationCache[SoundTouchNodes.presets.Path]
        print("\nCached configuration, direct:\n%s" % presetList.ToString(True))
        
    # sort the list (in place) by Name, ascending order.
    presetList.Presets.sort(key=lambda x: x.Name or "", reverse=False)
    print("\nList sorted by Name:\n%s" % presetList.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
