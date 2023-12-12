from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current group configuration status.
    groupBefore:Group = client.GetGroupStereoPairStatus()
    print("\nGroup Status Before:\n%s" % groupBefore.ToString(True))

    # initialize the new group configuration.
    group:Group = Group(name="Bose-ST10-1 + Bose-ST10-4", masterDeviceId="9070658C9D4A")
    group.AddRole(GroupRole("192.168.1.131", "9070658C9D4A", GroupRoleTypes.Left))
    group.AddRole(GroupRole("192.168.1.134", "F45EAB3115DA", GroupRoleTypes.Right))
            
    # create a new group configuration on the device.
    print("\nCreating Group: %s" % group.Name)
    groupAfter:Group = client.CreateGroupStereoPair(group)
    print("\nGroup Status After:\n%s" % groupAfter.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))

