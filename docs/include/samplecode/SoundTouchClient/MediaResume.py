from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("(before): '%s' - '%s'" % (nowPlaying.ContentItem.Name, nowPlaying.ContentItem.Location))

    # resume currently playing media.
    client.MediaResume()

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("(after):  '%s' - '%s'" % (nowPlaying.ContentItem.Name, nowPlaying.ContentItem.Location))

except Exception as ex:

    print("** Exception: %s" % str(ex))
