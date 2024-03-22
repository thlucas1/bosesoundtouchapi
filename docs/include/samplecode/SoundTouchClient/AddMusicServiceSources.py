from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time 

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get list of defined sources.
    sourceList:SourceList = client.GetSourceList()
    print("\nSource list before the change:\n%s" % sourceList.ToString(True))
    
    # get list of upnp media services detected by the device.
    mediaServerList:MediaServerList = client.GetMediaServerList()
    print("\nUPnP Media Server list before the change:\n%s" % mediaServerList.ToString(True))
    
    # ensure all upnp media servers are defined as sources.
    print("\n\nVerifying UPnP media servers are defined as sources ...")
    sourcesAdded:list[str] = client.AddMusicServiceSources()
    if len(sourcesAdded) == 0:
        print(" *** All UPnP media servers are already defined as sources")
    else:
        print("Sources added:\n%s" % str(sourcesAdded))

        # get list of defined sources.
        sourceList:SourceList = client.GetSourceList()
        print("\nSource list after the change:\n%s" % sourceList.ToString(True))

except Exception as ex:

    print("** Exception: %s" % str(ex))
