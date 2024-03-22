from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    config:PerformWirelessSiteSurveyResponse = client.GetWirelessSiteSurvey()
    print(config.ToString(True))

    # get cached configuration, refreshing from device if needed.
    config:PerformWirelessSiteSurveyResponse = client.GetWirelessSiteSurvey(False)
    print("\nCached configuration:\n%s" % config.ToString(True))

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.performWirelessSiteSurvey.Path in client.ConfigurationCache:
        config:PerformWirelessSiteSurveyResponse = client.ConfigurationCache[SoundTouchNodes.performWirelessSiteSurvey.Path]
        print("\nCached configuration, direct:\n%s" % config.ToString(True))
           
    # sort the list (in place) by SignalStrength, ascending order.
    config.SurveyResultItems.sort(key=lambda x: x.SignalStrength or 0, reverse=False)
    print("\nList sorted by SignalStrength:\n%s" % config.ToString(True))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
