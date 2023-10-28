from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # create a new preset - radio station.
    new_preset_radio:Preset = Preset(
        4,
        time.time(),
        None,
        "TUNEIN",
        "stationurl",
        "/v1/playback/station/s309605",
        "",
        True,
        "My New Preset",
        "http://cdn-profiles.tunein.com/s309605/images/logog.png?t=637986891960000000"
        )
            
    print("Storing Preset: '%s' - %s" % (new_preset_radio.Name, new_preset_radio.Location))
                
    # store preset.
    client.StorePreset(new_preset_radio)
            
    # get list of defined presets.
    presetList:PresetList = client.GetPresetList()
    print(presetList.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
