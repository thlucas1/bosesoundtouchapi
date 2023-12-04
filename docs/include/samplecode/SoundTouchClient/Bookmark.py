from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\nCurrent Now Playing Status:\n%s" % nowPlaying.ToString())

    # bookmark the currently playing media.
    client.Bookmark()
                       
    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\nUpdated Now Playing Status:\n%s" % nowPlaying.ToString())

except Exception as ex:

    print("** Exception: %s" % str(ex))
