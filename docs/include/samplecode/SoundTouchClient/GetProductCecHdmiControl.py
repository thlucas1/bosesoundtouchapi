from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81")
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    # note that not all devices support retrieval of this information.
    config:ProductCecHdmiControl = client.GetProductCecHdmiControl()
    print(config.ToString())

    # get cached configuration, refreshing from device if needed.
    config:ProductCecHdmiControl = client.GetProductCecHdmiControl(False)
    print("\nCached configuration:\n%s" % config.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.productcechdmicontrol.Path in client.ConfigurationCache:
        config:ProductCecHdmiControl = client.ConfigurationCache[SoundTouchNodes.productcechdmicontrol.Path]
        print("\nCached configuration, direct:\n%s" % config.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
