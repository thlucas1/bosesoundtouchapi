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
    results:NavigateResponse = client.GetMusicServiceStations(criteria)
    print("\nMy %s Music Service Stations:\n%s" % (results.Source, results.ToString(True)))
        
    # get my PANDORA music service content - sort by date created, descending.
    criteria:Navigate = Navigate(SoundTouchSources.PANDORA, "YourMusicServiceUserId")
    results:NavigateResponse = client.GetMusicServiceStations(criteria)
    print("\nMy %s Music Service Stations (sorted by DateCreated DESC):\n%s" % (results.Source, results.ToString(True)))

    # get my PANDORA music service content - sort by station name, ascending.
    criteria:Navigate = Navigate(SoundTouchSources.PANDORA, "YourMusicServiceUserId", sortType=NavigateSortTypes.StationName)
    results:NavigateResponse = client.GetMusicServiceStations(criteria)
    print("\nMy %s Music Service Stations (sorted by StationName ASC):\n%s" % (results.Source, results.ToString(True)))

    # sort the results (in place) by Name, descending order.
    results.Items.sort(key=lambda x: (x.Name or "").lower(), reverse=True)
    print("\nList sorted by Name descending:\n%s" % results.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
