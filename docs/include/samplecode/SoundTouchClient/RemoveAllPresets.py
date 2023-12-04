from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # remove all presets.
    presetList:PresetList = client.RemoveAllPresets()
    print(presetList.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
