from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.130")
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current audio product tone controls.
    # note that not all devices support retrieval of this information.
    cfgBefore:AudioProductToneControls = None
    cfgBefore = client.GetAudioProductToneControls()
    print("\nCurrent Audio Product Tone Control Levels: \n%s" % cfgBefore.ToString())
        
    # create new tone controls object.
    cfgUpdate:AudioProductToneControls = AudioProductToneControls()

    # for testing purposes, toggle the Bass level.  
    # if the level is currently minValue, then we will set to maxValue.
    cfgUpdate.Bass.Value = cfgBefore.Bass.MinValue
    if cfgUpdate.Bass.Value == cfgBefore.Bass.Value:
        cfgUpdate.Bass.Value = cfgBefore.Bass.MaxValue
    print("\nSetting Audio Product Tone Control Bass Level to '%s' (from '%s') ..." % (cfgUpdate.Bass.Value, cfgBefore.Bass.Value))
                
    # for testing purposes, toggle the Treble level.  
    # if the level is currently minValue, then we will set to maxValue.
    cfgUpdate.Treble.Value = cfgBefore.Treble.MinValue
    if cfgUpdate.Treble.Value == cfgBefore.Treble.Value:
        cfgUpdate.Treble.Value = cfgBefore.Treble.MaxValue
    print("Setting Audio Product Tone Control Treble Level to '%s' (from '%s') ..." % (cfgUpdate.Treble.Value, cfgBefore.Treble.Value))
                
    # update audio product tone controls.
    client.SetAudioProductToneControls(cfgUpdate)
            
    # get current audio product tone controls.
    cfgAfter:AudioProductToneControls = client.GetAudioProductToneControls(True)
    print("\nChanged Audio Product Tone Controls: \n%s" % (cfgAfter.ToString()))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))

finally:
    
    if cfgBefore is not None:
        # reset audio product tone controls to original values.
        print("\nRestoring Audio Product Tone Controls to original values.")
        client.SetAudioProductToneControls(cfgBefore)            

        # get current audio product tone controls.
        cfgAfter:AudioProductToneControls = client.GetAudioProductToneControls(True)
        print("\nRestored Audio Product Tone Controls: \n%s" % (cfgAfter.ToString()))
