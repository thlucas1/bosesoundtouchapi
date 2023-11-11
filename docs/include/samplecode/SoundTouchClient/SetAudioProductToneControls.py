from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.130")
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current audio product tone controls.
    toneBefore:AudioProductToneControls = client.GetAudioProductToneControls()
    if toneBefore is None:
        print("SoundTouch device does not support AudioProductToneControls!")
    else:
        print("\nCurrent Audio Product Tone Control Levels: \n%s" % toneBefore.ToString())
        
        # create new tone controls object.
        toneUpdate:AudioProductToneControls = AudioProductToneControls()

        # for testing purposes, toggle the Bass level.  
        # if the level is currently minValue, then we will set to maxValue.
        toneUpdate.Bass.Value = toneBefore.Bass.MinValue
        if toneUpdate.Bass.Value == toneBefore.Bass.Value:
            toneUpdate.Bass.Value = toneBefore.Bass.MaxValue
        print("\nSetting Audio Product Tone Control Bass Level to '%s' (from '%s') ..." % (toneUpdate.Bass.Value, toneBefore.Bass.Value))
                
        # for testing purposes, toggle the Treble level.  
        # if the level is currently minValue, then we will set to maxValue.
        toneUpdate.Treble.Value = toneBefore.Treble.MinValue
        if toneUpdate.Treble.Value == toneBefore.Treble.Value:
            toneUpdate.Treble.Value = toneBefore.Treble.MaxValue
        print("Setting Audio Product Tone Control Treble Level to '%s' (from '%s') ..." % (toneUpdate.Treble.Value, toneBefore.Treble.Value))
                
        # update audio product tone controls.
        client.SetAudioProductToneControls(toneUpdate)
            
        # get current audio product tone controls.
        toneAfter:AudioProductToneControls = client.GetAudioProductToneControls(True)
        print("\nChanged Audio Product Tone Controls: \n%s" % (toneAfter.ToString()))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))

finally:
    
    if toneBefore is not None:
        # reset audio product tone controls to original values.
        print("\nRestoring Audio Product Tone Controls to original values.")
        client.SetAudioProductToneControls(toneBefore)            

        # get current audio product tone controls.
        toneAfter:AudioProductToneControls = client.GetAudioProductToneControls(True)
        print("\nRestored Audio Product Tone Controls: \n%s" % (toneAfter.ToString()))
