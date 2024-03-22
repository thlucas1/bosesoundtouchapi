import time
from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # play a notification beep.
    print("\nPlaying notification beep ...")
    client.PlayNotificationBeep()
   
except Exception as ex:

    print("** Exception: %s" % str(ex))
