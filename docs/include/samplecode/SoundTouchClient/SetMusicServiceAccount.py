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
    
    # set music service account source - Music Library on NAS (STORED_MUSIC).
    # note the userAccount value must match what is defined in the "/listMediaServers" service, with an ending "/0".
    print("\n\nAdding music service source: Music Library on NAS, Account='d09708a1-5953-44bc-a413-123456789012' ...")
    client.SetMusicServiceAccount("STORED_MUSIC", "Music Library on NAS", "d09708a1-5953-44bc-a413-123456789012/0", None)
                
    # set music service account source - PANDORA.
    print("\n\nAdding music service source: Pandora, Account='yourPandoraUserId' ...")
    client.SetMusicServiceAccount("PANDORA", "Pandora Account", "yourPandoraUserId", "yourPandoraPassword")
                
    # get list of defined sources.
    sourceList:SourceList = client.GetSourceList()
    print("\nSource list after the set:\n%s" % sourceList.ToString(True))

except Exception as ex:

    print("** Exception: %s" % str(ex))
