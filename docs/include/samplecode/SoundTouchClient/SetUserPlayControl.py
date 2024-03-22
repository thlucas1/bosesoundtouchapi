from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time

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

    # pause media that is currently playing.
    print("\nPause media that is currently playing ...")
    client.SetUserPlayControl(UserPlayControlTypes.Pause)

    time.sleep(3)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\nUpdated Now Playing Status:\n%s" % nowPlaying.ToString())
        
    # play media that is currently paused.
    print("\nPlay media that is currently paused. ...")
    client.SetUserPlayControl(UserPlayControlTypes.Play)

    time.sleep(3)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\nUpdated Now Playing Status:\n%s" % nowPlaying.ToString())

    # stop media that is currently playing.
    print("\nStop media that is currently playing ...")
    client.SetUserPlayControl(UserPlayControlTypes.Stop)

    time.sleep(3)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\nUpdated Now Playing Status:\n%s" % nowPlaying.ToString())

    # play media that is currently paused.
    print("\nPlay media that is currently stopped. ...")
    client.SetUserPlayControl(UserPlayControlTypes.Play)

    time.sleep(3)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\nUpdated Now Playing Status:\n%s" % nowPlaying.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
