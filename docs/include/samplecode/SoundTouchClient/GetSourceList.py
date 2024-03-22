from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    sourceList:SourceList = client.GetSourceList()
    print(sourceList.ToString(True))

    # get source list array.
    print("\nSourceArray:\n%s" % sourceList.ToSourceArray())

    # get source:account list array.
    print("\nSourceArray (with Account):\n%s" % sourceList.ToSourceArray(True))

    # get specific sourceitem with the source name.
    sourceItem = sourceList['TUNEIN']
    print("(by name 'TUNEIN')  %s" % (sourceItem.ToString()))

    # get specific sourceitem at the index position.
    sourceItem = sourceList[0]
    print("(by index 0)        %s" % (sourceItem.ToString()))

    # get cached configuration, refreshing from device if needed.
    sourceList:SourceList = client.GetSourceList(False)
    print("\nCached configuration:\n%s" % sourceList.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.sources.Path in client.ConfigurationCache:
        sourceList:SourceList = client.ConfigurationCache[SoundTouchNodes.sources.Path]
        print("\nCached configuration, direct:\n%s" % sourceList.ToString(True))
        
    # sort the list (in place) by SourceAccount, ascending order.
    sourceList.SourceItems.sort(key=lambda x: (x.SourceAccount or "").lower(), reverse=False)
    print("\nList sorted by SourceAccount:\n%s" % sourceList.ToString(True))
                       
except Exception as ex:

    print("** Exception: %s" % str(ex))
