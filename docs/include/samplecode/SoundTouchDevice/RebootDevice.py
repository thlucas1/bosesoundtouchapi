from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # reboot device.
    print("Rebooting device: '%s' ..." % device.DeviceName)
    response:str = device.RebootDevice()
    print("Device Response:\n%s" % response)
            
except Exception as ex:

    print("** Exception: %s" % str(ex))

