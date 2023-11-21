import sys
sys.path.append("..")

import unittest

# external package imports.
from smartinspectpython.siauto import *

# our package imports.
from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *
from bosesoundtouchapi.ws import *

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# SoundTouchDiscovery Tests
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

class Test_SoundTouchDiscovery(unittest.TestCase):
    """
    Test discovery scenarios.
    """

    @classmethod
    def setUpClass(cls):
        
        try:

            print("*******************************************************************************")
            print("** unittest.TestCase - setUpClass() Started")

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
            
        except Exception as ex:

            print("** unittest.TestCase - Exception in setUpClass() method!\n" + str(ex))
            raise

        finally:

            print("** unittest.TestCase - setUpClass() Complete")
            print("*******************************************************************************")

    
    @classmethod
    def tearDownClass(cls):
        
        try:

            print("*******************************************************************************")
            print("** unittest.TestCase - tearDownClass() Started")

            # unwire events, and dispose of SmartInspect.
            print("** Disposing of SmartInspect resources")
            SIAuto.Si.Dispose()
            
        except Exception as ex:

            print("** unittest.TestCase - Exception in tearDownClass() method!\n" + str(ex))
            raise

        finally:

            print("** unittest.TestCase - tearDownClass() Complete")
            print("*******************************************************************************")
                    
    
    def setUp(self):
        
        try:

            print("*******************************************************************************")
            print("** unittest.TestCase - setUp() Started")

            # nothing to do here.
            
        except Exception as ex:

            print("** unittest.TestCase - Exception in setUp() method!\n" + str(ex))
            raise

        finally:

            print("** unittest.TestCase - setUp() Complete")
            print("*******************************************************************************")

    
    def tearDown(self):
        
        try:

            print("*******************************************************************************")
            print("** unittest.TestCase - tearDown() Started")

            # nothing to do here.
            
        except Exception as ex:

            print("** unittest.TestCase - Exception in tearDown() method!\n" + str(ex))
            raise

        finally:

            print("** unittest.TestCase - tearDown() Complete")
            print("*******************************************************************************")

                       
    ###################################################################################################################################
    # test methods start here - above are testing support methods.
    ###################################################################################################################################


    def test_DiscoverDevices(self) -> None:
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_DiscoverDevices"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

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
           
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

# execute unit tests.
if __name__ == '__main__':
    unittest.main()
