# external package imports.
from collections.abc import Iterable 
import time
from smartinspectpython.siauto import *
from smartinspectpython.sisourceid import *
from xml.etree.ElementTree import Element, tostring
from xml.etree import ElementTree

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
siConfig:SIConfigurationTimer = SIConfigurationTimer(SIAuto.Si, siConfigPath, 60)

# get smartinspect logger reference and log basic system / domain details.
_logsi:SISession = SIAuto.Main
_logsi.LogSeparator(SILevel.Fatal)
_logsi.LogAppDomain(SILevel.Message)
_logsi.LogSystem(SILevel.Message)

print("** Test Starting\n")

try:
    
    # create SoundTouch device instance.
    #device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.130") # Bose SoundTouch 300

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    sourceList:SourceList = client.GetSourceList()
    print(sourceList.ToString(True))
    print("\nDictionary:\n%s" % sourceList.ToDictionary())

except Exception as ex:

    print("** Exception: %s" % str(ex))
        
finally:
            
    print("\n** Test Completed")

    # unwire events, and dispose of SmartInspect.
    print("** Disposing of SmartInspect resources")
    SIAuto.Si.Dispose()
