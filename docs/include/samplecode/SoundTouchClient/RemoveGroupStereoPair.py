from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current group configuration status.
    groupBefore:Group = client.GetGroupStereoPairStatus()
    print("\nGroup Status Before:\n%s" % groupBefore.ToString(True))
    
    # remove existing group configuration on the device.
    print("\nRemoving Group: '%s'" % groupBefore.Name)
    client.RemoveGroupStereoPair()

    # get current group configuration status.
    groupBefore:Group = client.GetGroupStereoPairStatus()
    print("\nGroup Status After:\n%s" % groupBefore.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))

