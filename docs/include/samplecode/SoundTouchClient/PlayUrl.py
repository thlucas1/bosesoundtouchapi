from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\n(before): %s" % (nowPlaying.ToString()))

    # play the given https url at the current volume level.
    print("\nPlaying HTTPS URL content from the web ...")
    client.PlayUrl("https://freetestdata.com/wp-content/uploads/2021/09/Free_Test_Data_1MB_MP3.mp3",
                   "FreeTestData.com",
                   "MP3 Test Data",
                   "Free_Test_Data_1MB_MP3",
                   volumeLevel=0)
    
    # play the given http url at the current volume level.
    print("\nPlaying HTTP URL content from the web ...")
    client.PlayUrl("http://www.hyperion-records.co.uk/audiotest/14%20Clementi%20Piano%20Sonata%20in%20D%20major,%20Op%2025%20No%206%20-%20Movement%202%20Un%20poco%20andante.MP3",
                   "Clementi",
                   "Movements Album",
                   "Piano Sonata in D major",
                   volumeLevel=0)
    
    # play the given url, retrieving metadata (artist,album,track) from the url content.
    print("\nPlaying HTTP URL content from Home Assistant ...")
    client.PlayUrl("http://homeassistant.local:8123/media/local/06%20Flawless.mp3?authSig=xxxx",
                   getMetaDataFromUrlFile=True,
                   volumeLevel=0)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\n(after):  %s" % (nowPlaying.ToString()))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
