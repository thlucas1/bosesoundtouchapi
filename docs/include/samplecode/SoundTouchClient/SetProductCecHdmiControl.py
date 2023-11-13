from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.130")
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current product cec hdmi control.
    # note that not all devices support retrieval of this information.
    cfgBefore:ProductCecHdmiControl = None
    cfgBefore = client.GetProductCecHdmiControl()
    print("\nCurrent product cec hdmi control value: \n%s" % cfgBefore.ToString())
        
    # create new tone controls object.
    cfgUpdate:ProductCecHdmiControl = ProductCecHdmiControl()

    # for testing purposes, toggle the value from OFF to ON or vice versa.
    # if the level is currently ON, then we will set to OFF.
    cfgUpdate.CecMode = SoundTouchHdmiCecModes.OFF
    if cfgUpdate.CecMode == cfgBefore.CecMode:
        cfgUpdate.CecMode = SoundTouchHdmiCecModes.ON
    print("\nSetting product cec hdmi control to '%s' (from '%s') ..." % (cfgUpdate.CecMode, cfgBefore.CecMode))
                
    # update product cec hdmi control.
    client.SetProductCecHdmiControl(cfgUpdate)
            
    # get current product cec hdmi control.
    cfgAfter:ProductCecHdmiControl = client.GetProductCecHdmiControl(True)
    print("\nChanged product cec hdmi control: \n%s" % (cfgAfter.ToString()))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))

finally:
    
    if cfgBefore is not None:
        
        # restore product cec hdmi control to original values.
        client.SetProductCecHdmiControl(cfgBefore)            

        # get current product cec hdmi control.
        cfgAfter:ProductCecHdmiControl = client.GetProductCecHdmiControl(True)
        print("\nRestored product cec hdmi control: \n%s" % (cfgAfter.ToString()))
