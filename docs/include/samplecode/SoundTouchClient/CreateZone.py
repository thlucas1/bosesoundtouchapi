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

    # initialize the new master zone configuration.
    masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host, True) # <- master
    masterZone.AddMember(ZoneMember("192.168.1.80", "E8EB11B9B723"))        # <- member
            
    # create a new master zone configuration on the device.
    client.CreateZone(masterZone)
               
    # get current zone configuration status.
    zoneAfter:Zone = client.GetZoneStatus()
    print("\nZone Status After:\n%s" % zoneAfter.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))

