from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # build list of zone members to add.
    zoneMembers:list = []
    zoneMembers.append(ZoneMember("192.168.1.80", "E8EB11B9B723"))
    zoneMembers.append(ZoneMember("192.168.1.82", "F9BC35A6D825"))
    zoneMembers.append(ZoneMember("192.168.1.83", "B8BD47C7F452"))

    # get current zone configuration status.
    zoneBefore:Zone = client.GetZoneStatus()
    print("\nCurrent Zone Status:\n%s" % zoneBefore.ToString(True))
    
    # if zone not active, then create one so that we have something to add.
    if len(zoneBefore.Members) == 0:
                
        print("Creating a new master zone so we have a master zone to add to ...")

        # initialize the new master zone configuration.
        masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host,True) # <- master
        member:ZoneMember
        for member in zoneMembers:
            masterZone.AddMember(member)                                        # <- member
            break   # only add 1 zone member, so it actually adds something below
            
        # create a new master zone configuration on the device.
        client.CreateZone(masterZone)

        # get current zone configuration status.
        zoneBefore:Zone = client.GetZoneStatus()
        print("\nZone Status Before:\n%s" % zoneBefore.ToString(True))

    # add zone members to the master zone configuration.
    client.AddZoneMembers(zoneMembers)

    # get current zone configuration status.
    zoneAfter:Zone = client.GetZoneStatus()
    print("\nZone Status After:\n%s" % zoneAfter.ToString(True))

except Exception as ex:

    print("** Exception: %s" % str(ex))
