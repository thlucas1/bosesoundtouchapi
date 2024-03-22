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
    
    # power standby (low-power) the device.
    client.PowerStandbyLowPower()

    # note that no web-services api commands can be issued after this until the
    # device is physically powered back on by holding down the power button.

except Exception as ex:

    print("** Exception: %s" % str(ex))
