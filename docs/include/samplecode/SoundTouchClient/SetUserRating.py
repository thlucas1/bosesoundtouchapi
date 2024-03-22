from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # note that PANDORA is currently the only source that supports ratings.
    # ratings are stored in the artist profile under "My Collection" settings.
    # if a ThumbsDown rating is assigned, then the current track play will stop
    # and advance to the next track.

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\nCurrent Now Playing Status:\n%s" % nowPlaying.ToString())

    # rate nowplaying content.
    print("\nRating Now Playing Content with ThumbsUp ...")
    client.SetUserRating(UserRatingTypes.ThumbsUp)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\nUpdated Now Playing Status:\n%s" % nowPlaying.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
