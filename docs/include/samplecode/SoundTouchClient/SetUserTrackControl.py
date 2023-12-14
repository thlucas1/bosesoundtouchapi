from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time

try:
    
    # note that PANDORA is currently the only source that supports ratings.
    # ratings are stored in the artist profile under "My Collection" settings.
    # if a ThumbsDown rating is assigned, then the current track play will stop
    # and advance to the next track.

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("NowPlaying Track = '%s'" % nowPlaying.Track)

    # play next track.
    print("\nPlay next track ...\n")
    client.SetUserTrackControl(UserTrackControlTypes.Next)
    time.sleep(3)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("NowPlaying Track = '%s'" % nowPlaying.Track)
        
    # play previous track.
    print("\nRestart track from beginning (after 10 seconds) ...\n")
    time.sleep(10)
    client.SetUserTrackControl(UserTrackControlTypes.Previous)
    time.sleep(3)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("NowPlaying Track = '%s'" % nowPlaying.Track)

    # play previous track.
    print("\nFORCE Play previous track (after 10 seconds) ...\n")
    time.sleep(10)
    client.SetUserTrackControl(UserTrackControlTypes.PreviousForce)
    time.sleep(3)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("NowPlaying Track = '%s'" % nowPlaying.Track)

except Exception as ex:

    print("** Exception: %s" % str(ex))
