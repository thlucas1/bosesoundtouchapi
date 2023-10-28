from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    print("Getting list of presets ...")
                
    # get list of defined presets.
    presetList:PresetList = client.GetPresetList()
    print(presetList.ToString(True))
   
    preset:Preset
    for preset in presetList:
        
        print("\nSelecting Preset: '%s' - %s" % (preset.Name, preset.Location))
                
        # select a preset, and delay 10 seconds after for the device to process the change.
        client.SelectPreset(preset, 10)
            
        # get current nowPlaying status.
        nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
        print("\nNow Playing: '%s' - '%s'" % (nowPlaying.ContentItem.Name, nowPlaying.ContentItem.Location))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
