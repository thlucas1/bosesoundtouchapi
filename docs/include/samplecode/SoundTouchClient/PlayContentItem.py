from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("(before): %s" % (nowPlaying.ToString()))

    # play the specified media content.
    content_item_radio:ContentItem = ContentItem("TUNEIN","stationurl","/v1/playback/station/s309605","",True,"K-LOVE 90s")
    client.PlayContentItem(content_item_radio)
            
    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("(after):  %s" % (nowPlaying.ToString()))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
