from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current volume level.
    volumeBefore:Volume = client.GetVolume(True)
    print("\nCurrent Volume Levels: %s" % (volumeBefore.ToString()))
            
    # for testing purposes, use a volume of 30.  if the volume is currently at 30,
    # then we will use a volume of 25.
    newLevel:int = 30
    if volumeBefore.Actual == newLevel:
        newLevel = 25
    print("\nSetting Volume level to %d (from %s) ..." % (newLevel, volumeBefore.Actual))
                
    # set volume to specific level.
    client.SetVolumeLevel(newLevel)
            
    # get current volume level.
    volumeAfter:Volume = client.GetVolume(True)
    print("\nChanged Volume Levels: %s" % (volumeAfter.ToString()))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
