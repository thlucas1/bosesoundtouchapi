from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131")
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    # note that not all devices support retrieval of this information.
    config:AudioSpeakerAttributeAndSetting = client.GetAudioSpeakerAttributeAndSetting()
    print(config.ToString())

    # get cached configuration, refreshing from device if needed.
    config:AudioSpeakerAttributeAndSetting = client.GetAudioSpeakerAttributeAndSetting(False)
    print("\nCached configuration:\n%s" % config.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.audiospeakerattributeandsetting.Path in client.ConfigurationCache:
        config:AudioSpeakerAttributeAndSetting = client.ConfigurationCache[SoundTouchNodes.audiospeakerattributeandsetting.Path]
        print("\nCached configuration, direct:\n%s" % config.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
