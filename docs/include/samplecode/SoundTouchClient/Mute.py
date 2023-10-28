from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    volume:Volume = client.GetVolume()
    print("(before) %s" % volume.ToString())
    
    # toggle mute / unmute of the device.
    client.Mute()

    # get real-time configuration from the device.
    volume:Volume = client.GetVolume()
    print("(after)  %s" % volume.ToString())

except Exception as ex:

    print("** Exception: %s" % str(ex))
