from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get my collection of PANDORA music service stations.
    criteria:Navigate = Navigate(SoundTouchSources.PANDORA, "YourMusicServiceUserId")
    resultsBefore:NavigateResponse = client.GetMusicServiceStations(criteria)
    print("\n%s Music Service Stations before:\n%s" % (criteria.Source, resultsBefore.ToString(True)))

    # remove station from my collection of PANDORA music service stations.
    removeStation:RemoveStation = RemoveStation(SoundTouchSources.PANDORA, "YourMusicServiceUserId", "98000573042799134", "Zach Williams & Essential Worship")
    print("\nRemoving Station: %s" % removeStation.ToString())
    client.RemoveMusicServiceStation(removeStation)

    # commented out in case you really don't want to do this ...
    # remove all stations from my collection of PANDORA music service stations.
    # item:NavigateItem
    # for item in resultsBefore.Items:
    #     removeStation:RemoveStation = RemoveStation(contentItem=item.ContentItem)
    #     print("\nRemoving Station: %s" % removeStation.ToString())
    #     client.RemoveMusicServiceStation(removeStation)
        
    # get my collection of PANDORA music service stations.
    criteria:Navigate = Navigate(SoundTouchSources.PANDORA, "YourMusicServiceUserId")
    resultsAfter:NavigateResponse = client.GetMusicServiceStations(criteria)
    print("\n%s Music Service Stations after:\n%s" % (criteria.Source, resultsAfter.ToString(True)))

except Exception as ex:

    print("** Exception: %s" % str(ex))
