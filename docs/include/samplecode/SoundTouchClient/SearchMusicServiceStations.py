from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # search PANDORA music service stations for specified criteria.
    searchStation:SearchStation = SearchStation(SoundTouchSources.PANDORA, "YourMusicServiceUserId", "Zach Williams")
    print("\nSearching %s Music Service : %s" % (searchStation.Source, searchStation.ToString()))
    results:SearchStationResults = client.SearchMusicServiceStations(searchStation)
    print("\n%s Music Service Stations results:\n%s" % (results.Source, results.ToString(True)))
                
except Exception as ex:

    print("** Exception: %s" % str(ex))
