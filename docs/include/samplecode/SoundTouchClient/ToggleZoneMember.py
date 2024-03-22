from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # build zone member to toggle.
    zoneMember:ZoneMember = ZoneMember("192.168.1.82", "5072249B7B1D")

    # get current zone configuration status.
    zoneStatus:Zone = client.GetZoneStatus()
    print("\nCurrent Zone Status:\n%s" % zoneStatus.ToString(True))
           
    # toggle zone membership in the master zone configuration of the device.
    print("\nToggling zone member:\n%s" % (zoneMember.ToString()))
    msg:SoundTouchMessage = client.ToggleZoneMember(zoneMember)

    # get current zone configuration status.
    zoneStatus:Zone = client.GetZoneStatus()
    print("\nCurrent Zone Status:\n%s" % zoneStatus.ToString(True))

    # toggle zone membership in the master zone configuration of the device.
    print("\nToggling zone member:\n%s" % (zoneMember.ToString()))
    msg:SoundTouchMessage = client.ToggleZoneMember(zoneMember)

    # get current zone configuration status.
    zoneStatus:Zone = client.GetZoneStatus()
    print("\nCurrent Zone Status:\n%s" % zoneStatus.ToString(True))

except Exception as ex:

    print("** Exception: %s" % str(ex))
