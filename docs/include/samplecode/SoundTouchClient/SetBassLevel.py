from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    print("Getting bass capability configuration ...")

    # get current bass capabilities.
    bassCapabilities:BassCapabilities = client.GetBassCapabilities()
    print(bassCapabilities.ToString())
    
    # does the device have the capability to change the bass level?
    if bassCapabilities.IsAvailable:

        # get current bass level.
        bassBefore:Bass = client.GetBass(True)
        print("\nCurrent Bass Levels: %s" % (bassBefore.ToString()))
            
        # for testing purposes, use a maximum bass level as defined by capabilities.
        # if the bass level is currently at maximum, then we will use a value of minimum.
        newLevel:int = bassCapabilities.Maximum
        if bassBefore.Actual == newLevel:
            newLevel = bassCapabilities.Minimum
        print("\nSetting Bass level to %d (from %s) ..." % (newLevel, bassBefore.Actual))

        # set bass to specific level.
        client.SetBassLevel(newLevel)
            
        # get current bass level.
        bassAfter:Bass = client.GetBass(True)
        print("\nChanged Bass Levels: %s" % (bassAfter.ToString()))
        
    else:
        
        print("Device '%s' does not support changing bass levels!" % device.DeviceName)
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
