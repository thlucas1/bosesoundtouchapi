from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.130")
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current audio product level controls.
    # note that not all devices support retrieval of this information.
    cfgBefore:AudioProductLevelControls = None
    cfgBefore = client.GetAudioProductLevelControls()
    print("\nCurrent audio product level controls: \n%s" % cfgBefore.ToString())
        
    # create new audio product level controls object.
    cfgUpdate:AudioProductLevelControls = AudioProductLevelControls()

    # for testing purposes, toggle the FrontCenterSpeakerLevel level.  
    # if the level is currently minValue, then we will set to maxValue.
    cfgUpdate.FrontCenterSpeakerLevel.Value = cfgBefore.FrontCenterSpeakerLevel.MinValue
    if cfgUpdate.FrontCenterSpeakerLevel.Value == cfgBefore.FrontCenterSpeakerLevel.Value:
        cfgUpdate.FrontCenterSpeakerLevel.Value = cfgBefore.FrontCenterSpeakerLevel.MaxValue
    print("\nSetting audio product level controls FrontCenterSpeakerLevel to '%s' (from '%s') ..." % (cfgUpdate.FrontCenterSpeakerLevel.Value, cfgBefore.FrontCenterSpeakerLevel.Value))
                
    # for testing purposes, toggle the RearSurroundSpeakersLevel level.  
    # if the level is currently minValue, then we will set to maxValue.
    cfgUpdate.RearSurroundSpeakersLevel.Value = cfgBefore.RearSurroundSpeakersLevel.MinValue
    if cfgUpdate.RearSurroundSpeakersLevel.Value == cfgBefore.RearSurroundSpeakersLevel.Value:
        cfgUpdate.RearSurroundSpeakersLevel.Value = cfgBefore.RearSurroundSpeakersLevel.MaxValue
    print("Setting audio product level controls RearSurroundSpeakersLevel to '%s' (from '%s') ..." % (cfgUpdate.RearSurroundSpeakersLevel.Value, cfgBefore.RearSurroundSpeakersLevel.Value))
                
    # update audio product level controls.
    client.SetAudioProductLevelControls(cfgUpdate)
            
    # get current audio product level controls.
    cfgAfter:AudioProductLevelControls = client.GetAudioProductLevelControls(True)
    print("\nChanged audio product level controls: \n%s" % (cfgAfter.ToString()))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))

finally:
    
    if cfgBefore is not None:
        
        # restore audio product level controls to original values.
        client.SetAudioProductLevelControls(cfgBefore)            

        # get current audio product level controls.
        cfgAfter:AudioProductLevelControls = client.GetAudioProductLevelControls(True)
        print("\nRestored audio product level controls: \n%s" % (cfgAfter.ToString()))
