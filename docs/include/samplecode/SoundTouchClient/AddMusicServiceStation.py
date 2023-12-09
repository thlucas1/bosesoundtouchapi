from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get my collection of PANDORA music service stations.
    criteria:Navigate = Navigate(SoundTouchSources.PANDORA, "YourMusicServiceUserId", NavigateMenuTypes.radioStations, 1, 100)
    resultsBefore:NavigateResponse = client.GetMusicServiceStations(criteria)
    print("\n%s Music Service Stations before:\n%s" % (criteria.Source, resultsBefore.ToString(True)))
        
    # add station to my collection of PANDORA music service stations.
    addStation:AddStation = AddStation(SoundTouchSources.PANDORA, "YourMusicServiceUserId", "R4328162", "Zach Williams & Essential Worship")
    print("\nAdding Station: %s" % addStation.ToString())
    client.AddMusicServiceStation(addStation)
        
    # get my collection of PANDORA music service stations.
    criteria:Navigate = Navigate(SoundTouchSources.PANDORA, "YourMusicServiceUserId", NavigateMenuTypes.radioStations, 1, 100)
    resultsAfter:NavigateResponse = client.GetMusicServiceStations(criteria)
    print("\n%s Music Service Stations after:\n%s" % (criteria.Source, resultsAfter.ToString(True)))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
