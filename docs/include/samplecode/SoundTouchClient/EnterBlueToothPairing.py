import time
from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # enter bluetooth pairing mode.
    print("\nEntering Bluetooth pairing mode - check your mobile device Bluetooth list ...")
    client.EnterBluetoothPairing()
   
except Exception as ex:

    print("** Exception: %s" % str(ex))
