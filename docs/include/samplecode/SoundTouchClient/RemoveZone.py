from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current zone configuration status.
    zoneBefore:Zone = client.GetZoneStatus()
    print("\nCurrent Zone Status:\n%s" % zoneBefore.ToString(True))
    
    # if zone not active, then create one so that we have something to remove.
    if len(zoneBefore.Members) == 0:
                
        print("Creating a new master zone so we have a zone to remove ...")

        # build list of zone members to remove.
        zoneMembers:list = []
        zoneMembers.append(ZoneMember("192.168.1.80", "E8EB11B9B723"))

        # initialize the new master zone configuration.
        masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host, True) # <- master
        member:ZoneMember
        for member in zoneMembers:
            masterZone.AddMember(member)                                         # <- member
            
        # create a new master zone configuration on the device.
        client.CreateZone(masterZone)

        # get current zone configuration status.
        zoneBefore:Zone = client.GetZoneStatus()
        print("\nZone Status Before:\n%s" % zoneBefore.ToString(True))

    # remove the master zone configuration from the device.
    client.RemoveZone()

    # get current zone configuration status.
    zoneAfter:Zone = client.GetZoneStatus()
    print("\nZone Status After:\n%s" % zoneAfter.ToString(True))

except Exception as ex:

    print("** Exception: %s" % str(ex))
