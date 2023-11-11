from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.130")
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current audio dsp controls.
    dspBefore:AudioDspControls = client.GetAudioDspControls(True)
    if dspBefore is None:
        print("SoundTouch device does not support AudioDspControls!")
    else:
        print("\nCurrent Audio DSP Controls Supported Audio Modes array: %s" % (dspBefore.ToSupportedAudioModesArray()))
        print("\nCurrent Audio DSP Controls: %s" % (dspBefore.ToString()))
            
        # for testing purposes, toggle the audio mode.  if the mode is currently "AUDIO_MODE_NORMAL",
        # then we will use "AUDIO_MODE_DIALOG".
        newMode:str = "AUDIO_MODE_NORMAL"
        if dspBefore.AudioMode == newMode:
            newMode = "AUDIO_MODE_DIALOG"
        print("\nSetting Audio DSP Controls AudioMode to '%s' (from '%s') ..." % (newMode, dspBefore.AudioMode))
                
        # set audio dsp controls to specific audio mode.
        client.SetAudioDspControlAudioMode(newMode)
            
        # get current audio dsp controls.
        dspAfter:AudioDspControls = client.GetAudioDspControls(True)
        print("\nChanged Audio DSP Controls: %s" % (dspAfter.ToString()))

except Exception as ex:

    print("** Exception: %s" % str(ex))
