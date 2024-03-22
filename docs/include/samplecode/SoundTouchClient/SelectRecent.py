from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    print("Getting list of recents ...")

    # get list of defined recents.
    recents:RecentList = client.GetRecentList()
    print(recents.ToString(True))

    # process list.
    recent:Recent = None
    for i, recent in list(enumerate(recents)):
            
        print("\nSelecting Recent: '%s' - %s" % (recent.Name, recent.Location))
                
        # select a recent, and delay 10 seconds after for the device to process the change.
        client.SelectRecent(recent, 10)
            
        # get current nowPlaying status.
        nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
        print("\nNow Playing: '%s' - '%s'" % (nowPlaying.ContentItem.Name, nowPlaying.ContentItem.Location))

        # only process a few of the recent entries, as there could be a lot.
        if i >= 2:
            break

except Exception as ex:

    print("** Exception: %s" % str(ex))
