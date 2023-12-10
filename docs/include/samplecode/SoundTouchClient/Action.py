from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # send a PRESET_1 action to play a preset (only release state required).
    print("Sending PRESET_1 key release ...")
    client.Action(SoundTouchKeys.PRESET_1, KeyStates.Release)
    time.sleep(5)
           
    # send a PRESET_1 action to store a preset (only press state required).
    print("Sending PRESET_1 key press ...")
    client.Action(SoundTouchKeys.PRESET_1, KeyStates.Press)
    time.sleep(5)
           
    # send a VOLUME_UP action to adjust volume (both press and release states required).
    print("Sending VOLUME_UP key press and release ...")
    client.Action(SoundTouchKeys.VOLUME_UP, KeyStates.Both)
    time.sleep(5)
           
    # send a MUTE action to mute volume (only press state required).
    print("Sending MUTE key press ...")
    client.Action(SoundTouchKeys.MUTE, KeyStates.Press)
    time.sleep(5)
           
    # send a POWER action to toggle power state (both press and release states required).
    print("Sending POWER key press and release ...")
    client.Action(SoundTouchKeys.POWER, KeyStates.Both)

except Exception as ex:

    print("** Exception: %s" % str(ex))
