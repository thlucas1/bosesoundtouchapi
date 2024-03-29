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
    config:ProductHdmiAssignmentControls = client.GetProductHdmiAssignmentControls()
    print(config.ToString())

    # get cached configuration, refreshing from device if needed.
    config:ProductHdmiAssignmentControls = client.GetProductHdmiAssignmentControls(False)
    print("\nCached configuration:\n%s" % config.ToString())

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.producthdmiassignmentcontrols.Path in client.ConfigurationCache:
        config:ProductHdmiAssignmentControls = client.ConfigurationCache[SoundTouchNodes.producthdmiassignmentcontrols.Path]
        print("\nCached configuration, direct:\n%s" % config.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
