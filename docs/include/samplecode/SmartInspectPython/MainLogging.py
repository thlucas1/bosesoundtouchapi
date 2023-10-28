# import smartinspect logging support.
from smartinspectpython.siauto import *

# load SmartInspect settings from a configuration settings file.
siConfigPath:str = "./tests/smartinspect.cfg"
SIAuto.Si.LoadConfiguration(siConfigPath)

# start monitoring the configuration file for changes, and reload it when it changes.
# this will check the file for changes every 60 seconds.
siConfig:SIConfigurationTimer = SIConfigurationTimer(SIAuto.Si, siConfigPath, 60)

# get smartinspect logger reference.
_logsi:SISession = SIAuto.Main

# log system environment and application startup parameters.
_logsi.LogSeparator(SILevel.Fatal)
_logsi.LogAppDomain(SILevel.Verbose)
_logsi.LogSystem(SILevel.Verbose)
