from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    group:Group = client.GetGroupStereoPairStatus()
    print("\nGroup Status Before:\n%s" % group.ToString(True))

    # update group name.
    print("\nRenaming Group ...")
    groupAfter:Group = client.UpdateGroupStereoPairName("My Updated GroupName")
    print("\nGroup Status After:\n%s" % groupAfter.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))

