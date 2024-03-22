from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current zone configuration status.
    zoneBefore:Zone = client.GetZoneStatus()
    print("\nZone Status Before:\n%s" % zoneBefore.ToString(True))

    # create new device instances for all zone members.
    device_master:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # master
    device_member:SoundTouchDevice = SoundTouchDevice("192.168.1.80") # member
            
    # create a new master zone configuration on the device.
    masterZone:Zone = client.CreateZoneFromDevices(device_master, [device_member])
    print("\nMaster Zone created:\n%s" % (masterZone.ToString(True)))
               
    # get current zone configuration status.
    zoneAfter:Zone = client.GetZoneStatus()
    print("\nZone Status After:\n%s" % zoneAfter.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))


