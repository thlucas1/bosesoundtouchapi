from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    volume:Volume = client.GetVolume()
    print("(before) %s" % volume.ToString())
    
    # tick volume up one notch.
    client.VolumeUp()

    # get real-time configuration from the device.
    volume:Volume = client.GetVolume()
    print("(after)  %s" % volume.ToString())

except Exception as ex:

    print("** Exception: %s" % str(ex))
