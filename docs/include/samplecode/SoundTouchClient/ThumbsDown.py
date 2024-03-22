from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\nCurrent Now Playing Status:\n%s" % nowPlaying.ToString())

    # are rating functions allowed for currently playing media?
    if nowPlaying.IsRatingEnabled:
                
        # rate the currently playing media.
        client.ThumbsDown()
            
        # give the device time to process the change.
        time.sleep(1)
            
        # get current nowPlaying status.
        nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
        print("\nUpdated Now Playing Status:\n%s" % nowPlaying.ToString())

    else:
                
        print("\Ratings are not enabled for currently playing media")

except Exception as ex:

    print("** Exception: %s" % str(ex))
