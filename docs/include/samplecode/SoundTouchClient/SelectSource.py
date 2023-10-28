from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlayingBefore:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\n** Current Now Playing Status:\n%s" % nowPlayingBefore.ToString())

    # get list of source items.
    sources:SourceList = client.GetSourceList()
    
    print("\n** Sources supported by the device:\n%s" % sources.ToString(True))
    print("\n** Selecting Sources one-by-one ...")
            
    # select each source.
    sourceItem:SourceItem
    for sourceItem in sources:

        # trace.
        print("- Source='%s', SourceAccount='%s' ..." % (sourceItem.Source, sourceItem.SourceAccount))
                    
        # select an input source.
        msg:SoundTouchMessage = client.SelectSource(sourceItem.Source, sourceItem.SourceAccount)

    print("\n** Restoring original source ...")

    # play original source (if one was selected).
    if nowPlayingBefore.ContentItem.Source != "STANDBY":
        client.SelectContentItem(nowPlayingBefore.ContentItem)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\n** Updated Now Playing Status:\n%s" % nowPlaying.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
