from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # remove preset #4.
    client.RemovePreset(4)
            
    # get list of defined presets.
    presetList:PresetList = client.GetPresetList()
    print(presetList.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
