from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.80")
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current audio dsp controls.
    # note that not all devices support retrieval of this information.
    cfgBefore:AudioDspControls = None
    cfgBefore = client.GetAudioDspControls(True)
    print("\nCurrent audio dsp controls: \n%s" % (cfgBefore.ToString()))
    print("Supported Audio Modes array: %s" % (cfgBefore.ToSupportedAudioModesArray()))
            
    # create new audio dsp controls object.
    cfgUpdate:AudioDspControls = AudioDspControls()
    cfgUpdate.VideoSyncAudioDelay = cfgBefore.VideoSyncAudioDelay

    # for testing purposes, toggle the audio mode.
    # if the mode is currently "AUDIO_MODE_NORMAL" then we will use "AUDIO_MODE_DIALOG", or vice versa.
    cfgUpdate.AudioMode = AudioDspAudioModes.Normal
    if cfgUpdate.AudioMode == cfgBefore.AudioMode:
        cfgUpdate.AudioMode = AudioDspAudioModes.Dialog
    print("\nSetting audio dsp controls AudioMode to '%s' (from '%s') ..." % (cfgUpdate.AudioMode, cfgBefore.AudioMode))

    # set audio dsp controls to specific audio mode.
    client.SetAudioDspControls(cfgUpdate)
            
    # get current audio dsp controls.
    cfgAfter:AudioDspControls = client.GetAudioDspControls(True)
    print("\nChanged audio dsp controls: \n%s" % (cfgAfter.ToString()))

except Exception as ex:

    print("** Exception: %s" % str(ex))

finally:
    
    if cfgBefore is not None:
        
        # restore audio dsp controls to original values.
        client.SetAudioDspControls(cfgBefore)            

        # get current audio dsp controls.
        cfgAfter:AudioProductLevelControls = client.GetAudioDspControls(True)
        print("\nRestored audio dsp controls: \n%s" % (cfgAfter.ToString()))
