from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    recentList:RecentList = client.GetRecentList()
    print(recentList.ToString(True))
    
    # get cached configuration, refreshing from device if needed.
    recentList:RecentList = client.GetRecentList(False)
    print("\nCached configuration:\n%s" % recentList.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.recents.Path in client.ConfigurationCache:
        recentList:RecentList = client.ConfigurationCache[SoundTouchNodes.recents.Path]
        print("\nCached configuration, direct:\n%s" % recentList.ToString(True))

    # sort the list (in place) by Name, ascending order.
    recentList.Recents.sort(key=lambda x: (x.Name or "").lower(), reverse=False)
    print("\nList sorted by Name:\n%s" % recentList.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
