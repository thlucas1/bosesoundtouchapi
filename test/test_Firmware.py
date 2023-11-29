# external package imports.
from smartinspectpython.siauto import *

# our package imports.
from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.ws import *

# load SmartInspect settings from a configuration settings file.
print("** Loading SmartInspect configuration settings")
siConfigPath:str = "./test/smartinspect.cfg"
SIAuto.Si.LoadConfiguration(siConfigPath)

# start monitoring the configuration file for changes, and reload it when it changes.
# this will check the file for changes every 60 seconds.
print("** Starting SmartInspect configuration settings watchdog")
siConfig:SIConfigurationTimer = SIConfigurationTimer(SIAuto.Si, siConfigPath)

# get smartinspect logger reference and log basic system / domain details.
_logsi:SISession = SIAuto.Main
_logsi.LogSeparator(SILevel.Fatal)
_logsi.LogAppDomain(SILevel.Message)
_logsi.LogSystem(SILevel.Message)

print("** Test Starting\n")

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
    #device:SoundTouchDevice = SoundTouchDevice("192.168.1.130") # Bose SoundTouch 300

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)
    
    # play the given https url at the current volume level.
    print("\nPlaying HTTPS URL content from the web ...")
    client.PlayUrl("https://stream.radioparadise.com/aac-128",
                   getMetaDataFromUrlFile=True,
                   volumeLevel=0)

except Exception as ex:

    print("** Exception: %s" % str(ex))
        
finally:
            
    print("\n** Test Completed")

    # unwire events, and dispose of SmartInspect.
    print("** Disposing of SmartInspect resources")
    SIAuto.Si.Dispose()
