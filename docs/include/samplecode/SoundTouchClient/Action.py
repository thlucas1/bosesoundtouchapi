from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # send a POWER action to toggle power state.
    client.Action(SoundTouchKeys.POWER)
    print("\nPOWER key was pressed")

except Exception as ex:

    print("** Exception: %s" % str(ex))
