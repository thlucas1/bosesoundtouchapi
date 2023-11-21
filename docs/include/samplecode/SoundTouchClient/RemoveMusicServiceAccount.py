from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time 

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get list of defined sources.
    sourceList:SourceList = client.GetSourceList()
    print("\nSource list before the change:\n%s" % sourceList.ToString(True))
    
    # get list of upnp media services detected by the device.
    mediaServerList:MediaServerList = client.GetMediaServerList()
    print("\nUPnP Media Server list before the change:\n%s" % mediaServerList.ToString(True))
    
    # remove all music service account sources for upnp media servers.
    print("\n\nRemoving all music service 'STORED_MUSIC' account sources ...")
    mediaServer:MediaServer
    for mediaServer in mediaServerList:
        sourceAccount:str = "%s%s" % (mediaServer.ServerId, "/0")
        sourceItem:SourceItem
        for sourceItem in sourceList:
            if sourceItem.SourceAccount == mediaServer.ServerId:
                print("- Removing source: '%s' (%s)" % (mediaServer.FriendlyName, sourceItem.SourceAccount))
                client.RemoveMusicServiceAccount(sourceItem.Source, sourceItem.FriendlyName, sourceItem.SourceAccount, None)
                break
            elif sourceItem.SourceAccount == sourceAccount:
                print("- Removing source: '%s' (%s)" % (mediaServer.FriendlyName, sourceAccount))
                client.RemoveMusicServiceAccount(sourceItem.Source, sourceItem.FriendlyName, sourceAccount, None)
                break
                
    # get real-time configuration from the device.
    sourceList:SourceList = client.GetSourceList()
    print("\nSource list after the remove:\n%s" % sourceList.ToString(True))
           
    # add all music service account sources for upnp media servers.
    print("\nAdding all UPnP media servers as 'STORED_MUSIC' account sources ...")
    mediaServer:MediaServer
    for mediaServer in mediaServerList:
        sourceAccount:str = "%s%s" % (mediaServer.ServerId, "/0")
        print("- Adding source: '%s' (%s)" % (mediaServer.FriendlyName, sourceAccount))
        client.SetMusicServiceAccount("STORED_MUSIC", mediaServer.FriendlyName, sourceAccount, None)
                
    # get list of defined sources.
    sourceList:SourceList = client.GetSourceList()
    print("\nSource list after the set:\n%s" % sourceList.ToString(True))

except Exception as ex:

    print("** Exception: %s" % str(ex))
