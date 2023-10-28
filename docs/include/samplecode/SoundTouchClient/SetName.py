from bosesoundtouchapi import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    print("Name Before: '%s'" % client.Device.DeviceName)
    
    # set the device name.
    client.SetName('My SoundTouch 10')

    print("Name After:  '%s'" % client.Device.DeviceName)
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
