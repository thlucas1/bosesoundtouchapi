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

    # select last wifi source.
    client.SelectLastWifiSource()

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\n** Updated Now Playing Status:\n%s" % nowPlaying.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
