from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("(before): '%s'" % (nowPlaying.ToString()))
    print("\nIsSeekSupported = '%s'" % nowPlaying.IsSeekSupported)
    print("Position Setting Before = %s" % str(nowPlaying.Position))

    # is seek function allowed for currently playing media?
    if nowPlaying.IsSeekSupported:

        # start playing media at the specified position (in seconds).
        print("Seeking to position = 10 ...")
        client.MediaSeekToTime(10)
            
        # get current nowPlaying status.
        nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
        print("Position Setting After  = %s" % str(nowPlaying.Position))
        print("\n(after ): '%s'" % (nowPlaying.ToString()))

    else:

        print("\n** Seek function not available for currently playing media")

except Exception as ex:

    print("** Exception: %s" % str(ex))
