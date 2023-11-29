# external package imports.
from smartinspectpython.siauto import *

# our package imports.
from bosesoundtouchapi import *

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

try:

    print("Test Starting\n")
    _logsi.LogMessage("Testing ZeroConf (MDNS) Discovery", colorValue=SIColors.LightGreen)

    # create a new instance of the discovery class.
    # we will verify device connections, as well as print device details
    # to the console as they are discovered.
    discovery:SoundTouchDiscovery = SoundTouchDiscovery(True, printToConsole=True)

    # discover SoundTouch devices on the network, waiting up to 
    # 5 seconds for all devices to be discovered.
    discovery.DiscoverDevices(timeout=5)
            
    # print all discovered devices.
    _logsi.LogText(SILevel.Message, "Discovered SoundTouch Devices (%i items)" % len(discovery), discovery.ToString(True), colorValue=SIColors.LightGreen)
    print("\n%s" % (discovery.ToString(True)))
                   
except Exception as ex:

    _logsi.LogException(None, ex)
    print(str(ex))
        
finally:
            
    print("\nTests Completed")

    # dispose of SmartInspect.
    print("** Disposing of SmartInspect resources")
    SIAuto.Si.Dispose()