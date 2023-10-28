import sys
sys.path.append("..")

import unittest

# external package imports.
from collections.abc import Iterable 
import time
from smartinspectpython.siauto import *
from smartinspectpython.sisourceid import *
from xml.etree.ElementTree import Element
from xml.etree import ElementTree

# our package imports.
from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *
from bosesoundtouchapi.ws import *


class Test_SoundTouchClient(unittest.TestCase):
    """
    Test all Client scenarios.
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
                    
    
    def _CreateApiClient(self) -> SoundTouchClient:
        """
        Creates a new SoundTouchClient instance, and sets all properties for executing these test cases.

        Returns:
            An SoundTouchClient instance.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            

        try:

            # create SoundTouchDevice instance.
            device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            #device:SoundTouchDevice = SoundTouchDevice("192.168.1.130") # Bose SoundTouch 300
            #device:SoundTouchDevice = SoundTouchDevice("192.168.1.133") # non-existant ip
            #device:SoundTouchDevice = SoundTouchDevice("x.168.1.133") # invalid ip
            
            # create SoundTouchClient instance from device.
            client:SoundTouchClient = SoundTouchClient(device)
                       
            # return instance to caller.
            return client

        except Exception as ex:

            _logsi.LogException("Exception in Test Method \"{0}\"".format(SISession.GetMethodName()), ex)
            print("** Exception: %s" % str(ex))
            raise


    def _OnSoundTouchUpdateEvent(self, args:Element) -> None:
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            

        if (args != None):
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device status update: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen)
            print("Status update args: %s", argsEncoded)
        

    def _OnSoundTouchInfoEvent(self, args:Element) -> None:
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            

        if (args != None):
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device information event: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen)
            print("Status info args: %s", argsEncoded)
        

    def _GetAndDisplayPresetList(self, client:SoundTouchClient, _logsi:SISession, log_trace:bool = True) -> PresetList:
    
            # get list of defined presets.
            preset_list:PresetList = client.GetPresetList()

            # trace.
            if log_trace:
                
                print(preset_list.ToString())
                
                preset:Preset
                for preset in preset_list:
                    _logsi.LogObject(SILevel.Message, preset.ToString(), preset, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                    print(preset.ToString())
        
            # return current list to caller.
            return preset_list
    

    def _GetAndDisplayRecentList(self, client:SoundTouchClient, _logsi:SISession, log_trace:bool = True) -> RecentList:
    
            # get list of defined recents.
            recent_list:RecentList = client.GetRecentList()

            # trace.
            if log_trace:
                
                print(recent_list.ToString())
                
                recent:Recent
                for recent in recent_list:
                    _logsi.LogObject(SILevel.Message, recent.ToString(), recent, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                    print(recent.ToString())
        
            # return current list to caller.
            return recent_list
    

    def _GetAndDisplayZoneStatus(self, client:SoundTouchClient, log_prefix:str, _logsi:SISession, log_trace:bool = True) -> Zone:
    
            # get current multiroom config.
            zone:Zone = client.GetZoneStatus()
            
            # trace.
            if log_trace:

                _logsi.LogObject(SILevel.Message, "%s%s" % (log_prefix, zone.ToString()), zone, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print("%s%s" % (log_prefix, zone.ToString()))
                
                zone_member:ZoneMember
                for zone_member in zone:
                    _logsi.LogObject(SILevel.Message, zone_member.ToString(), zone_member, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                    print(zone_member.ToString())
        
            # return current multiroom config to caller.
            return zone
    

    def _GetAndDisplayNowPlayingStatus(self, client:SoundTouchClient, log_prefix:str, _logsi:SISession, log_trace:bool = True) -> NowPlayingStatus:
    
            # get current nowPlaying status.
            status:NowPlayingStatus = client.GetNowPlayingStatus(True)

            # trace.
            if log_trace:
                
                _logsi.LogObject(SILevel.Message, "%s%s" % (log_prefix, status.ToString()), status, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print("%s%s" % (log_prefix, status.ToString()))
                
            # return current status to caller.
            return status


    def _GetAndDisplayVolume(self, client:SoundTouchClient, log_prefix:str, _logsi:SISession, log_trace:bool = True) -> Volume:
    
            # get current volume levels.
            vol:Volume = client.GetVolume(True)

            # trace.
            if log_trace:
                
                _logsi.LogObject(SILevel.Message, "%s%s" % (log_prefix, vol.ToString()), vol, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print("%s%s" % (log_prefix, vol.ToString()))
                
            # return current volume to caller.
            return vol

    ###################################################################################################################################
    # test methods start here - above are testing support methods.
    ###################################################################################################################################

    def test_Action(self):
        """
        Test Action method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # send a POWER action to toggle power state.
            client.Action(SoundTouchKeys.POWER)
           
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_AddFavorite(self):
        """
        Test AddFavorite method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # can the nowPlaying item be a favorite?
            if statBefore.IsFavoriteEnabled:
                
                # add the currently playing media to the device favorites.
                client.AddFavorite()
            
                # give the device time to process the change.
                time.sleep(1)
            
                # get current nowPlaying status.
                statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

                # test assertions.
                self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                if statBefore.IsFavoriteEnabled:
                    self.assertEqual(statAfter.IsFavorite, True, "NowPlayingStatus IsFavorite should be True")
                    
            else:
                
                print("Favorites not enabled for currently playing media")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_AddZoneMembers(self):
        """ 
        Test AddZoneMembers method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # build list of zone members to add.
            zoneMembers:list = []
            zoneMembers.append(ZoneMember("192.168.1.130", "E8EB11B9B723"))
            zoneMembers.append(ZoneMember("192.168.1.132", "F9BC35A6D825"))
            zoneMembers.append(ZoneMember("192.168.1.133", "B8BD47C7F452"))

            # get current zone configuration status.
            zoneBefore:Zone = self._GetAndDisplayZoneStatus(client, "(curent) ", _logsi)
            
            # if zone not active, then create one so that we have something to add.
            if len(zoneBefore.Members) == 0:
                
                print("Creating a new master zone so we have a zone member to add ...")

                # initialize the new master zone configuration.
                masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host,True) # <- master
                member:ZoneMember
                for member in zoneMembers:
                    masterZone.AddMember(member)                                        # <- member
                    break   # only add 1 zone member, so it actually adds something below
            
                # create a new master zone configuration on the device.
                client.CreateZone(masterZone)

                # get current zone configuration status.
                zoneBefore:Zone = self._GetAndDisplayZoneStatus(client, "(before) ", _logsi)

            # add zone members to the master zone configuration.
            msg:SoundTouchMessage = client.AddZoneMembers(zoneMembers)

            # get current zone configuration status.
            zoneAfter:Zone = self._GetAndDisplayZoneStatus(client, "(after)  ", _logsi)

            # test assertions.
            #self.assertNotEqual(len(zoneAfter), len(zoneBefore), "Zone count should not be the same before and after CreateZone()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    # def test_Bookmark(self):
    #     """
    #     Test Bookmark method scenarios.
    #     """
    #     # set SmartInspect logger reference.        
    #     _logsi:SISession = SIAuto.Main            
    #     # set method name for console output.
    #     methodName:str = SISession.GetMethodName()

    #     try:

    #         print("Test Starting:  %s" % methodName)
    #         _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

    #         # create BoseDevice instance.
    #         client:SoundTouchClient = self._CreateApiClient()

    #         # get current nowPlaying status.
    #         statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

    #         # add the currently playing media to the device favorites.
    #         client.Bookmark()
            
    #         # give the device time to process the change.
    #         time.sleep(1)
            
    #         # get current nowPlaying status.
    #         statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

    #         # test assertions.
    #         # self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
    #         # self.assertEqual(statAfter.IsFavorite, True, "NowPlayingStatus IsFavorite should be True")
                    
    #         print("Test Completed: %s" % methodName)

    #     except Exception as ex:

    #         _logsi.LogException("Test Exception: %s" % (methodName), ex)
    #         print("** Exception: %s" % str(ex))
    #         raise
        

    def test_CreateZone(self):
        """
        Test CreateZone method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current zone configuration status.
            zoneBefore:Zone = self._GetAndDisplayZoneStatus(client, "(before) ", _logsi)

            # initialize the new master zone configuration.
            masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host,True) # <- master
            masterZone.AddMember(ZoneMember("192.168.1.130", "E8EB11B9B723"))       # <- member
            
            # create a new master zone configuration on the device.
            msg:SoundTouchMessage = client.CreateZone(masterZone)

            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))
            
            # get current zone configuration status.
            zoneAfter:Zone = self._GetAndDisplayZoneStatus(client, "(after)  ", _logsi)

            # test assertions.
            #self.assertNotEqual(len(zoneAfter), len(zoneBefore), "Zone count should not be the same before and after CreateZone()")

            # test group member missing device id.
            with self.assertRaises(SoundTouchWarning, msg="Should have raised SoundTouchWarning for group member with no device id"):
                _logsi.LogMessage("Testing for group member with no device id ...", colorValue=SIColors.LightGreen)
                print("Testing for group member with no device id ...")
                masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host,True)   # <- master device
                masterZone.AddMember(ZoneMember("192.168.1.130"))      # <- missing device id
                client.CreateZone(masterZone)

            # test zone not supplied.
            with self.assertRaises(SoundTouchWarning, msg="Should have raised SoundTouchWarning for Zone object is None"):
                _logsi.LogMessage("Testing for Zone object is None ...", colorValue=SIColors.LightGreen)
                print("Testing for Zone object is None ...")
                client.CreateZone(None)

            # test invalid zone type.
            with self.assertRaises(SoundTouchWarning, msg="Should have raised SoundTouchWarning for invalid Zone type"):
                _logsi.LogMessage("Testing for invalid Zone type ...", colorValue=SIColors.LightGreen)
                print("Testing for invalid Zone type ...")
                client.CreateZone(SoundTouchClient)

            # test zone with no zone members.
            with self.assertRaises(SoundTouchWarning, msg="Should have raised SoundTouchWarning for Zone with no ZoneMember objects"):
                _logsi.LogMessage("Testing for Zone with no ZoneMember objects ...", colorValue=SIColors.LightGreen)
                print("Testing Zone with no ZoneMember objects ...")
                masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host,True)   # <- master device
                client.CreateZone(masterZone)

            # test invalid zone member type.
            with self.assertRaises(SoundTouchWarning, msg="Should have raised SoundTouchWarning for invalid ZoneMember object"):
                _logsi.LogMessage("Testing for invalid ZoneMember object ...", colorValue=SIColors.LightGreen)
                print("Testing for invalid ZoneMember object ...")
                masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host,True)   # <- master device
                masterZone.AddMember(SoundTouchClient)
                client.CreateZone(masterZone)

            # test add master as zone member.
            with self.assertRaises(SoundTouchWarning, msg="Should have raised SoundTouchWarning for adding master as ZoneMember"):
                _logsi.LogMessage("Testing for adding master as ZoneMember ...", colorValue=SIColors.LightGreen)
                print("Testing for adding master as ZoneMember ...")
                masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host,True)   # <- master device
                masterZone.AddMember(ZoneMember(masterZone.MasterIpAddress, masterZone.MasterDeviceId)) # <- master device
                client.CreateZone(masterZone)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_CreateZoneFromDevices(self):
        """
        Test CreateZoneFromDevices method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current zone configuration status.
            zoneBefore:Zone = self._GetAndDisplayZoneStatus(client, "(before) ", _logsi)

            # create new device instances for all zone members.
            device_master:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # master
            device_member:SoundTouchDevice = SoundTouchDevice("192.168.1.130") # member
            
            # create a new master zone configuration on the device.
            masterZone:Zone = client.CreateZoneFromDevices(device_master, [device_member])
            print("Master Zone created:\n%s" % (masterZone.ToString(True)))
            
            # get current zone configuration status.
            zoneAfter:Zone = self._GetAndDisplayZoneStatus(client, "(after)  ", _logsi)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetBalance(self):
        """
        Test GetBalance method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current balance configuration.
            balance:Balance = client.GetBalance()
            
            # test assertions.
            self.assertIsInstance(balance, (Balance), "Returned object should be of type Balance")
            _logsi.LogObject(SILevel.Message, balance.ToString(), balance, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(balance.ToString())
            self.assertIsNotNone(balance.Actual, "Balance Actual property should not be None")
            self.assertIsNotNone(balance.IsAvailable, "Balance IsAvailable property should not be None")

            # get cached configuration, refreshing from device if needed.
            balance:Balance = client.GetBalance(False)
            print("\nCached configuration:\n%s" % balance.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.balance.Path in client.ConfigurationCache:
                balance:Balance = client.ConfigurationCache[SoundTouchNodes.balance.Path]
                print("\nCached configuration, direct:\n%s" % balance.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetBass(self):
        """
        Test GetBass method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current bass configuration.
            bass:Bass = client.GetBass()
            
            # test assertions.
            self.assertIsInstance(bass, (Bass), "Returned object should be of type Bass")
            _logsi.LogObject(SILevel.Message, bass.ToString(), bass, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(bass.ToString())
            self.assertIsNotNone(bass.Actual, "Bass Actual property should not be None")
            self.assertIsNotNone(bass.Target, "Bass Target property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetBassCapabilities(self):
        """
        Test GetBassCapabilities method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current bass capabilities configuration.
            bass_caps:BassCapabilities = client.GetBassCapabilities()
            
            # test assertions.
            self.assertIsInstance(bass_caps, (BassCapabilities), "Returned object should be of type BassCapabilities")
            _logsi.LogObject(SILevel.Message, bass_caps.ToString(), bass_caps, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(bass_caps.ToString())
            self.assertIsNotNone(bass_caps.Minimum, "BassCapabilities Minimum property should not be None")
            self.assertIsNotNone(bass_caps.Maximum, "BassCapabilities Maximum property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetCapabilities(self):
        """
        Test GetCapabilities method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current capabilities configuration.
            capabilities:Capabilities = client.GetCapabilities()
            
            # test assertions.
            self.assertIsInstance(capabilities, (Capabilities), "Returned object should be of type Capabilities")
            self.assertIsInstance(capabilities, (Iterable), "Returned object should be of type Iterable")
            _logsi.LogObject(SILevel.Message, capabilities.ToString(), capabilities, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(capabilities.ToString())

            # list capability dictionary.
            capability:str
            for capability in capabilities:
                self.assertIsInstance(capability, (str), "Returned objects in Capabilities list should be of type str")
                _logsi.LogString(SILevel.Message, "- '%s' = '%s'" % (capability, capabilities[capability]), colorValue=SIColors.LightGreen)
                print("- '%s' = '%s'" % (capability, capabilities[capability]))

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetClockConfig(self):
        """
        Test GetClockConfig method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current clock configuration.
            clock_config:ClockConfig = client.GetClockConfig()
            
            # test assertions.
            self.assertIsInstance(clock_config, (ClockConfig), "Returned object should be of type ClockConfig")
            _logsi.LogObject(SILevel.Message, clock_config.ToString(), clock_config, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(clock_config.ToString())
            self.assertIsNotNone(clock_config.TimeZoneInfo, "ClockConfig TimeZoneInfo property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetClockTime(self):
        """
        Test GetClockTime method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current clock time configuration.
            clock_time:ClockTime = client.GetClockTime()
            
            # test assertions.
            self.assertIsInstance(clock_time, (ClockTime), "Returned object should be of type ClockTime")
            _logsi.LogObject(SILevel.Message, clock_time.ToString(), clock_time, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(clock_time.ToString())
            self.assertIsNotNone(clock_time.TimeFormat, "ClockTime TimeFormat property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetDspMono(self):
        """
        Test GetDspMono method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current digital signal processor configuration.
            dsp_profile:DSPMonoStereoItem = client.GetDspMono()
            
            # test assertions.
            self.assertIsInstance(dsp_profile, (DSPMonoStereoItem), "Returned object should be of type DSPMonoStereoItem")
            _logsi.LogObject(SILevel.Message, dsp_profile.ToString(), dsp_profile, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(dsp_profile.ToString())
            self.assertIsNotNone(dsp_profile.DeviceId, "DSPMonoStereoItem DeviceId property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetLanguage(self):
        """
        Test GetLanguage method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current language configuration.
            config:SimpleConfig = client.GetLanguage()
            
            # test assertions.
            self.assertIsInstance(config, (SimpleConfig), "Returned object should be of type SimpleConfig")
            _logsi.LogObject(SILevel.Message, config.ToString(), config, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(config.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetMediaServerList(self):
        """
        Test GetMediaServerList method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()
            
            # queries all UPnP media servers found by the SoundTouch device.
            media_servers:MediaServerList = client.GetMediaServerList()
            
            # test assertions.
            self.assertIsInstance(media_servers, (MediaServerList), "Returned source items list should be of type MediaServerList")
            self.assertIsInstance(media_servers, (Iterable), "Returned object should be of type Iterable")
            _logsi.LogArray(SILevel.Message, media_servers.ToString(), media_servers, colorValue=SIColors.LightGreen)
            print(media_servers.ToString())
           
            # test assertions of list items.
            media_server:MediaServer = None
            for media_server in media_servers:

                # test assertions.
                self.assertIsInstance(media_server, (MediaServer), "Returned objects in MediaServerList list should be of type MediaServer")
                _logsi.LogObject(SILevel.Message, media_server.ToString(), media_server, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print(media_server.ToString())
                self.assertIsNotNone(media_server.ServerId, "MediaServer ServerId property should not be None")
                self.assertIsNotNone(media_server.FriendlyName, "MediaServer FriendlyName property should not be None")
                self.assertIsNotNone(media_server.IpAddress, "MediaServer IpAddress property should not be None")
                self.assertIsNotNone(media_server.MacAddress, "MediaServer MacAddress property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetName(self):
        """
        Test GetName method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current name configuration.
            config:SimpleConfig = client.GetName()
            
            # test assertions.
            self.assertIsInstance(config, (SimpleConfig), "Returned object should be of type SimpleConfig")
            _logsi.LogObject(SILevel.Message, config.ToString(), config, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(config.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetNetworkInfo(self):
        """
        Test GetNetworkInfo method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()
            
            # get current network info configuration.
            netinfo:NetworkInfo = client.GetNetworkInfo()
            
            # test assertions.
            self.assertIsInstance(netinfo, (NetworkInfo), "Returned object should be of type NetworkInfo")
            _logsi.LogObject(SILevel.Message, netinfo.ToString(), netinfo, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(netinfo.ToString())
            
            # process list of defined networks.
            intfc:NetworkInfoInterface = None
            for intfc in netinfo:

                # test assertions.
                self.assertIsInstance(intfc, (NetworkInfoInterface), "Returned objects in NetworkInfo list should be of type NetworkInfoInterface")
                _logsi.LogObject(SILevel.Message, intfc.ToString(), intfc, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print(intfc.ToString())
                self.assertIsNotNone(intfc.Name, "NetworkInfoInterface Name property should not be None")
                self.assertIsNotNone(intfc.InterfaceType, "NetworkInfoInterface InterfaceType property should not be None")
                self.assertIsNotNone(intfc.State, "NetworkInfoInterface State property should not be None")
                self.assertIsNotNone(intfc.MacAddress, "NetworkInfoInterface MacAddress property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetNetworkStatus(self):
        """
        Test GetNetworkStatus method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()
            
            # get current network status configuration.
            netstats:NetworkStatus = client.GetNetworkStatus()
            
            # test assertions.
            self.assertIsInstance(netstats, (NetworkStatus), "Returned object should be of type NetworkStatus")
            _logsi.LogObject(SILevel.Message, netstats.ToString(), netstats, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(netstats.ToString())
            
            # process list of defined interfaces.
            intfc:NetworkStatusInterface = None
            for intfc in netstats:

                # test assertions.
                self.assertIsInstance(intfc, (NetworkStatusInterface), "Returned network interface object should be of type NetworkStatusInterface")
                _logsi.LogObject(SILevel.Message, intfc.ToString(), intfc, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print(intfc.ToString())
                self.assertIsNotNone(intfc.Name, "NetworkStatusInterface Name property should not be None")
                self.assertIsNotNone(intfc.MacAddress, "NetworkStatusInterface MacAddress property should not be None")
                self.assertIsNotNone(intfc.IsRunning, "NetworkStatusInterface IsRunning property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetNowPlayingStatus(self):
        """
        Test GetNowPlayingStatus method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # query the current playing status.
            status:NowPlayingStatus = client.GetNowPlayingStatus()
            
            # test assertions.
            self.assertIsInstance(status, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            _logsi.LogObject(SILevel.Message, status.ToString(), status, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(status.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetOptions(self):
        """
        Test GetOptions method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # list available HTTP-Methods for a specific node.
            node:SoundTouchUri = SoundTouchNodes.volume
            methods:list = client.GetOptions(node)
            print("Options for '%s' node: %s" % (node.Path, str(methods)))
    
            # test assertions.
            self.assertIsInstance(methods, (list), "Returned methods object should be of type list")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetPowerManagement(self):
        """
        Test GetPowerManagement method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()
            
            # get current power management status configuration.
            pwrmgmt:PowerManagement = client.GetPowerManagement()
            
            # test assertions.
            self.assertIsInstance(pwrmgmt, (PowerManagement), "Returned object should be of type PowerManagement")
            _logsi.LogObject(SILevel.Message, pwrmgmt.ToString(), pwrmgmt, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(pwrmgmt.ToString())
            self.assertIn(pwrmgmt.State, ["FullPower"], "Unrecognized value for PowerManagement State property")
            self.assertIsNotNone(pwrmgmt.BatteryCapable, "PowerManagement BatteryCapable property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetPresetList(self):
        """
        Test GetPresetList method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current preset list configuration.
            presets:PresetList = client.GetPresetList()
            
            # test assertions.
            self.assertIsInstance(presets, (PresetList), "Returned presets should be of type PresetList")
            self.assertIsInstance(presets, (Iterable), "Returned object should be of type Iterable")
            _logsi.LogArray(SILevel.Message, presets.ToString(), presets, colorValue=SIColors.LightGreen)
            print(presets.ToString())
            
            # test assertions of list items.
            preset:Preset
            for preset in presets:
                self.assertIsInstance(preset, (Preset), "Returned objects in PresetList list should be of type Preset")
                _logsi.LogObject(SILevel.Message, preset.ToString(), preset, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print(preset.ToString())
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetRecentList(self):
        """
        Test GetRecentList method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current recent list configuration.
            recents:RecentList = client.GetRecentList()
            
            # test assertions.
            self.assertIsInstance(recents, (RecentList), "Returned recents should be of type RecentList")
            self.assertIsInstance(recents, (Iterable), "Returned object should be of type Iterable")
            _logsi.LogArray(SILevel.Message, recents.ToString(), recents, colorValue=SIColors.LightGreen)
            print(recents.ToString())
            
            # test assertions of list items.
            recent:Recent
            for recent in recents:
                self.assertIsInstance(recent, (Recent), "Returned objects in RecentList list should be of type Recent")
                _logsi.LogObject(SILevel.Message, recent.ToString(), recent, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print(recent.ToString())
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetRequestToken(self):
        """
        Test GetRequestToken method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()
            
            # requests a new token generated by the device.
            config:SimpleConfig = client.GetRequestToken()
            
            # test assertions.
            self.assertIsInstance(config, (SimpleConfig), "Returned object should be of type SimpleConfig")
            _logsi.LogObject(SILevel.Message, config.ToString(), config, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(config.ToString())
            _logsi.LogString(SILevel.Message, "GetRequestToken: token", config.Attribute['value'], colorValue=SIColors.LightGreen)
            print("token=%s" % config.Attribute['value'])
            self.assertIsNotNone(config.Attribute, "SimpleConfig Attribute property should not be None")
            self.assertIsNone(config.Value, "SimpleConfig Value property should be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetSourceList(self):
        """
        Test GetSourceList method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current source list configuration.
            source_items:SourceList = client.GetSourceList()
            
            # test assertions.
            self.assertIsInstance(source_items, (SourceList), "Returned source items list should be of type SourceList")
            self.assertIsInstance(source_items, (Iterable), "Returned object should be of type Iterable")
            _logsi.LogArray(SILevel.Message, source_items.ToString(), source_items, colorValue=SIColors.LightGreen)
            print(source_items.ToString())
            
            # test assertions of list items.
            source_item:SourceItem
            for source_item in source_items:
                self.assertIsInstance(source_item, (SourceItem), "Returned objects in SourceList list should be of type SourceItem")
                _logsi.LogObject(SILevel.Message, source_item.ToString(), source_item, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print(source_item.ToString())

            # get specific sourceitem with the source name.
            source_item = source_items['TUNEIN']

            # test assertions.
            self.assertIsInstance(source_item, (SourceItem), "Returned source item should be of type SourceItem")
            _logsi.LogObject(SILevel.Message, "(by name)  %s" % (source_item.ToString()), source_item, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print("(by name 'TUNEIN')  %s" % (source_item.ToString()))

            # get specific sourceitem at the index position.
            source_item = source_items[0]

            # test assertions.
            self.assertIsInstance(source_item, (SourceItem), "Returned source item should be of type SourceItem")
            _logsi.LogObject(SILevel.Message, "(by index) %s" % (source_item.ToString()), source_item, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print("(by index 0)        %s" % (source_item.ToString()))
                    
            print("Test Completed: %s" % methodName)
            
            _logsi.LogDictionary(SILevel.Verbose, "Current ConfigurationCache Dictionary", client.ConfigurationCache)

            # get cached source list configuration.
            if SoundTouchNodes.sources.Path in client.ConfigurationCache:
                source_items:SourceList = client.ConfigurationCache[SoundTouchNodes.sources.Path]
                print("(cached) %s" % source_items.ToString(True))
                _logsi.LogArray(SILevel.Message, "(cached) %s" % source_items.ToString(), source_items, colorValue=SIColors.LightGreen)
            pass
            


        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetSystemTimeout(self):
        """
        Test GetSystemTimeout method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()
            
            # queries whether power saving is enabled or not.
            systimeout:SystemTimeout = client.GetSystemTimeout()
            
            # test assertions.
            self.assertIsInstance(systimeout, (SystemTimeout), "Returned object should be of type SystemTimeout")
            _logsi.LogObject(SILevel.Message, systimeout.ToString(), systimeout, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(systimeout.ToString())
            self.assertIn(systimeout.IsPowersavingEnabled, [True,False], "SystemTimeout IsPowersavingEnabled property should return True or False")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetVolume(self):
        """
        Test GetVolume method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current volume levels.
            volume:Volume = client.GetVolume()
            _logsi.LogObject(SILevel.Message, volume.ToString(), volume, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(volume.ToString())

            # test assertions.
            self.assertIsInstance(volume, (Volume), "Returned volume object should be of type Volume")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetWirelessProfile(self):
        """
        Test GetWirelessProfile method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # queries the active wireless profile.
            wifi_profile:WirelessProfile = client.GetWirelessProfile()
            
            # test assertions.
            self.assertIsInstance(wifi_profile, (WirelessProfile), "Returned object should be of type WirelessProfile")
            _logsi.LogObject(SILevel.Message, wifi_profile.ToString(), wifi_profile, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(wifi_profile.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetZoneStatus(self):
        """
        Test GetZoneStatus method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()
            
            # queries the current multiroom config.
            zone_config:Zone = client.GetZoneStatus()
            
            # test assertions.
            self.assertIsInstance(zone_config, (Zone), "Returned object should be of type Zone")
            self.assertIsInstance(zone_config, (Iterable), "Returned object should be of type Iterable")
            _logsi.LogObject(SILevel.Message, zone_config.ToString(), zone_config, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print(zone_config.ToString())
            
            # process list of defined zone members.
            zone_slave:ZoneMember = None
            for zone_slave in zone_config:

                # test assertions.
                self.assertIsInstance(zone_slave, (ZoneMember), "Returned Zone object should be of type ZoneMember")
                _logsi.LogObject(SILevel.Message, zone_slave.ToString(), zone_slave, colorValue=SIColors.LightGreen, excludeNonPublic=True)
                print(zone_slave.ToString())
                # self.assertIsNotNone(zone_slave.DeviceId, "ZoneMember DeviceId property should not be None")
                self.assertIsNotNone(zone_slave.IpAddress, "ZoneMember IpAddress property should not be None")
                # self.assertIsNotNone(zone_slave.DeviceRole, "ZoneMember DeviceRole property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MakeRequest(self):
        """
        Test MakeRequest method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()
            
            # manually make a request to the volume status node.
            volume:Volume = Volume(25)
            print("\nVolume object:\n%s" % volume.ToString())
            reqBody:str = volume.ToXmlRequestBody()
            message = SoundTouchMessage(SoundTouchNodes.volume, reqBody)
            client.MakeRequest('POST', message)
            print("\nMakeRequest Response:\n%s" % message.XmlMessage)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaNextTrack(self):
        """
        Test MediaNextTrack method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # move to the next track in the current media playlist.
            client.MediaNextTrack()
            
            # give the device time to process the change.
            time.sleep(3)
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statAfter.Track, statBefore.Track, "NowPlayingStatus Track should have changed")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaPause(self):
        """
        Test MediaPause method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # pause nowPlaying media.
            client.MediaPause()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertIn(statAfter.PlayStatus, ["STOP_STATE",None], "NowPlayingStatus PlayStatus should be STOP_STATE, or None if device is in STANDBY")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaPlay(self):
        """
        Test MediaPlay method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # play currently paused media.
            client.MediaPlay()
            
            # give the device time to process the change.
            time.sleep(1)

            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statBefore.PlayStatus, statAfter.PlayStatus, "NowPlayingStatus PlayStatus should have changed")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaPlayPause(self):
        """
        Test MediaPlayPause method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # toggle play / pause nowPlaying media.
            client.MediaPlayPause()
            
            # give the device time to process the change.
            time.sleep(1)
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statBefore.PlayStatus, statAfter.PlayStatus, "NowPlayingStatus PlayStatus should have changed")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaPreviousTrack(self):
        """
        Test MediaPreviousTrack method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # move to the previous track in the current media playlist.
            client.MediaPreviousTrack()
            
            # give the device time to process the change.
            time.sleep(3)
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statAfter.Track, statBefore.Track, "NowPlayingStatus Track should have changed")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaRepeatAll(self):
        """
        Test MediaRepeatAll method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # enable repeat all processing for the current media playlist.
            client.MediaRepeatAll()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statAfter.RepeatSetting, statBefore.RepeatSetting, "NowPlayingStatus RepeatSetting should have changed")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaRepeatOff(self):
        """
        Test MediaRepeatOff method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # disable repeat (all / one) processing for the current media playlist.
            client.MediaRepeatOff()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statAfter.RepeatSetting, statBefore.RepeatSetting, "NowPlayingStatus RepeatSetting should have changed")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaRepeatOne(self):
        """
        Test MediaRepeatOne method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # enable repeat one processing for the current media playlist.
            client.MediaRepeatOne()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statAfter.RepeatSetting, statBefore.RepeatSetting, "NowPlayingStatus RepeatSetting should have changed")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaResume(self):
        """
        Test MediaResume method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # resume playing media.
            client.MediaResume()
            
            # give SoundTouch device time to catch up.
            time.sleep(2)

            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertIn(statAfter.PlayStatus, ["PLAY_STATE","BUFFERING_STATE",None], "NowPlayingStatus PlayStatus should be PLAY_STATE or BUFFERING_STATE after Resume(), or None if device is in STANDBY")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaShuffleOff(self):
        """
        Test MediaShuffleOff method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # disable shuffling of the current media playlist. 
            client.MediaShuffleOff()
            
            # give SoundTouch device time to catch up.
            time.sleep(2)

            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statAfter.ShuffleSetting, statBefore.ShuffleSetting, "NowPlayingStatus ShuffleSetting should have changed")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaShuffleOn(self):
        """
        Test MediaShuffleOn method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # enable shuffling of the current media playlist. 
            client.MediaShuffleOn()
            
            # give SoundTouch device time to catch up.
            time.sleep(2)

            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statAfter.ShuffleSetting, statBefore.ShuffleSetting, "NowPlayingStatus ShuffleSetting should have changed")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaStop(self):
        """
        Test MediaStop method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # stop nowPlaying media.
            client.MediaStop()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertIn(statAfter.PlayStatus, ["STOP_STATE",None], "NowPlayingStatus PlayStatus should be STOP_STATE after MediaStop(), or None if device is in STANDBY")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_Mute(self):
        """
        Test mute method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current volume levels.
            volBefore:Volume = self._GetAndDisplayVolume(client, "(before) ", _logsi)

            # toggle mute / unmute.
            client.Mute()
            
            # get current volume levels.
            volAfter:Volume = self._GetAndDisplayVolume(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(volAfter, (Volume), "Returned volume object should be of type Volume")
            self.assertNotEqual(volBefore.IsMuted, volAfter.IsMuted, "volume IsMuted property should not be the same before and after mute()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MuteOff(self):
        """
        Test MuteOff method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current volume levels.
            volBefore:Volume = self._GetAndDisplayVolume(client, "(before) ", _logsi)

            # unmute device.
            client.MuteOff()
            
            # give SoundTouch device time to catch up.
            time.sleep(1)

            # get current volume levels.
            volAfter:Volume = self._GetAndDisplayVolume(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(volAfter, (Volume), "Returned status object should be of type Volume")
            self.assertEqual(volAfter.IsMuted, False, "volume IsMuted should be False after MuteOff()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MuteOn(self):
        """
        Test mute_on method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current volume levels.
            volBefore:Volume = self._GetAndDisplayVolume(client, "(before) ", _logsi)

            # mute device.
            client.MuteOn()
            
            # give SoundTouch device time to catch up.
            time.sleep(1)

            # get current volume levels.
            volAfter:Volume = self._GetAndDisplayVolume(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(volAfter, (Volume), "Returned status object should be of type Volume")
            self.assertEqual(volAfter.IsMuted, True, "volume IsMuted should be True after mute_on()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_PlayContentItem(self):
        """
        Test PlayContentItem method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # create various content items to play.
            content_item_radio_01:ContentItem = ContentItem("TUNEIN","stationurl","/v1/playback/station/s249983","",True,"Christian Hits")
            content_item_radio_02:ContentItem = ContentItem("TUNEIN","stationurl","/v1/playback/station/s309605","",True,"K-LOVE 90s")

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # ensure the now playing changes.
            play_content_item = content_item_radio_01
            if statBefore.ContentItem != None:
                if statBefore.ContentItem.Location == content_item_radio_01.Location:
                    play_content_item = content_item_radio_02

            # play the specified media content.
            msg:SoundTouchMessage = client.PlayContentItem(play_content_item)
            
            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))

            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(msg, (SoundTouchMessage), "Result object should be of type SoundTouchMessage")
            self.assertIn(statAfter.PlayStatus, ["PLAY_STATE","BUFFERING_STATE",None], "NowPlayingStatus PlayStatus should be PLAY_STATE or BUFFERING_STATE after play(), or None if device is in STANDBY")
            self.assertNotEqual(statBefore.StationName, statAfter.StationName, "NowPlayingStatus StationName should have changed after play()")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_PlayNotificationTTS(self):
        """
        Test PlayNotificationTTS method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # use google text to speech to say a message.
            print("\nSaying message via Google TTS (language=EN) ...")
            msg:SoundTouchMessage = client.PlayNotificationTTS("There is activity at the front door.")
   
            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))
   
            # if playing messages back to back, then give the message time to play
            # before playing the next one; otherwise the next message is lost.
            time.sleep(6)

            # use google text to speech to say a message.
            print("\nSaying message via Google TTS (language=DE) ...")
            msg:SoundTouchMessage = client.PlayNotificationTTS("There is activity at the front door.", 
                                                               "http://translate.google.com/translate_tts?ie=UTF-8&tl=DE&client=tw-ob&q={saytext}",
                                                                volumeLevel=30)

            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))
   
            # if playing messages back to back, then give the message time to play
            # before playing the next one; otherwise the next message is lost.
            time.sleep(6)

            # use google text to speech to say a message.
            print("\nSaying message via Google TTS (language=EN) ...")
            msg:SoundTouchMessage = client.PlayNotificationTTS("There is activity at the front door.", 
                                                               "http://translate.google.com/translate_tts?ie=UTF-8&tl=EN&client=tw-ob&q={saytext}",
                                                               "Activity Detected", # <- appears in nowPlaying.Artist
                                                               "Front Door",        # <- appears in nowPlaying.Album
                                                               "Motion Sensor",     # <- appears in nowPlaying.Track
                                                               volumeLevel=20)

            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))
   
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(msg, (SoundTouchMessage), "Result object should be of type SoundTouchMessage")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_PlayUrl(self):
        """
        Test PlayUrl method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # play the given url at the current volume level.
            print("\nPlaying URL content from the web ...")
            msg:SoundTouchMessage = client.PlayUrl("http://www.hyperion-records.co.uk/audiotest/14%20Clementi%20Piano%20Sonata%20in%20D%20major,%20Op%2025%20No%206%20-%20Movement%202%20Un%20poco%20andante.MP3",
                                                   "Clementi",
                                                   "Movements Album",
                                                   "Piano Sonata in D major",
                                                   volumeLevel=0)

            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))
   
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(msg, (SoundTouchMessage), "Result object should be of type SoundTouchMessage")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_Power(self):
        """
        Test Power method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # toggle power on / off.
            client.Power()
            
            # give SoundTouch device time to catch up.
            time.sleep(1)

            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statBefore.Source, statAfter.Source, "NowPlayingStatus Source should not be the same before and after Power()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_PowerOff(self):
        """
        Test PowerOff method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # power off device.
            client.PowerOff()
            
            # give SoundTouch device time to catch up.
            time.sleep(1)

            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertEqual(statAfter.Source, "STANDBY", "NowPlayingStatus should be STANDBY after PowerOff()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_PowerOn(self):
        """
        Test PowerOn method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # power on device.
            client.PowerOn()
            
            # give SoundTouch device time to catch up.
            time.sleep(1)

            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertNotEqual(statAfter.Source, "STANDBY", "NowPlayingStatus should not be STANDBY after PowerOn()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_RemoveAllPresets(self):
        """
        Test RemoveAllPresets method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined presets.
            presetsBefore:PresetList = self._GetAndDisplayPresetList(client, _logsi)

            # remove all stored presets.
            client.RemoveAllPresets()
            
            # give the device time to process the change.
            time.sleep(1)
            
            # get list of defined presets.
            presetsAfter:PresetList = self._GetAndDisplayPresetList(client, _logsi)
           
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_RemoveFavorite(self):
        """
        Test RemoveFavorite method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # can the nowPlaying item be a favorite?
            if statBefore.IsFavoriteEnabled:
                
                # remove the currently playing media from the device favorites.
                client.RemoveFavorite()
            
                # give the device time to process the change.
                time.sleep(1)
            
                # get current nowPlaying status.
                statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

                # test assertions.
                self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                if statBefore.IsFavoriteEnabled:
                    self.assertEqual(statAfter.IsFavorite, False, "NowPlayingStatus IsFavorite should be False")
                    
            else:
                
                print("Favorites not enabled for currently playing media")
                
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_RemovePreset(self):
        """
        Test RemovePreset method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined presets.
            presetsBefore:PresetList = self._GetAndDisplayPresetList(client, _logsi)

            # remove specified preset id.
            client.RemovePreset(4)
            
            # get list of defined presets.
            presetsAfter:PresetList = self._GetAndDisplayPresetList(client, _logsi)
           
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_RemoveZone(self):
        """ 
        Test RemoveZone method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current zone configuration status.
            zoneBefore:Zone = self._GetAndDisplayZoneStatus(client, "(curent) ", _logsi)
            
            # if zone not active, then create one so that we have something to remove.
            if len(zoneBefore.Members) == 0:
                
                print("Creating a new master zone so we have a zone member to remove ...")

                # initialize the new multiroom config.
                masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host,True) # <- master
                masterZone.AddMember(ZoneMember("192.168.1.130", "E8EB11B9B723"))       # <- member
            
                # create a new multiroom group (zone) using the multiroom config.
                client.CreateZone(masterZone)

                # get current zone configuration status.
                zoneAfter:Zone = self._GetAndDisplayZoneStatus(client, "(before) ", _logsi)

            # remove master zone.
            msg:SoundTouchMessage = client.RemoveZone()

            # get current zone configuration status.
            zoneAfter:Zone = self._GetAndDisplayZoneStatus(client, "(after)  ", _logsi)

            # test assertions.
            #self.assertNotEqual(len(zoneAfter), len(zoneBefore), "Zone count should not be the same before and after CreateZone()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_RemoveZoneMembers(self):
        """ 
        Test RemoveZoneMembers method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # build list of zone members to remove.
            zoneMembers:list = []
            zoneMembers.append(ZoneMember("192.168.1.130", "E8EB11B9B723"))

            # get current zone configuration status.
            zoneBefore:Zone = self._GetAndDisplayZoneStatus(client, "(curent) ", _logsi)
            
            # if zone not active, then create one so that we have something to remove.
            if len(zoneBefore.Members) == 0:
                
                print("Creating a new master zone so we have a zone member to remove ...")
                
                # initialize the new master zone configuration.
                masterZone:Zone = Zone(client.Device.DeviceId, client.Device.Host, True) # <- master
                member:ZoneMember
                for member in zoneMembers:
                    masterZone.AddMember(member)                                         # <- member
            
                # create a new master zone configuration on the device.
                client.CreateZone(masterZone)

                # get current zone configuration status.
                zoneBefore:Zone = self._GetAndDisplayZoneStatus(client, "(before) ", _logsi)

            # remove zone members from the master zone configuration on the device.
            msg:SoundTouchMessage = client.RemoveZoneMembers(zoneMembers)

            # get current zone configuration status.
            zoneAfter:Zone = self._GetAndDisplayZoneStatus(client, "(after)  ", _logsi)

            # test assertions.
            #self.assertNotEqual(len(zoneAfter), len(zoneBefore), "Zone count should not be the same before and after CreateZone()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectContentItem(self):
        """
        Test SelectContentItem method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # create various content items to play.
            content_item_radio_01:ContentItem = ContentItem("TUNEIN","stationurl","/v1/playback/station/s249983","",True,"Christian Hits")
            content_item_radio_02:ContentItem = ContentItem("TUNEIN","stationurl","/v1/playback/station/s309605","",True,"K-LOVE 90s")

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # ensure the now playing changes.
            play_content_item = content_item_radio_01
            if statBefore.ContentItem != None:
                if statBefore.ContentItem.Location == content_item_radio_01.Location:
                    play_content_item = content_item_radio_02

            # selects the specified content item.
            msg:SoundTouchMessage = client.SelectContentItem(play_content_item)
            
            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(msg, (SoundTouchMessage), "Result object should be of type SoundTouchMessage")
            self.assertIn(statAfter.PlayStatus, ["PLAY_STATE","BUFFERING_STATE",None], "NowPlayingStatus PlayStatus should be PLAY_STATE or BUFFERING_STATE after select_content_item(), or None if device is in STANDBY")
            self.assertNotEqual(statBefore.StationName, statAfter.StationName, "NowPlayingStatus StationName should have changed after select_content_item()")

            # create various content items to play.
            selections:list = []
            selections.append(ContentItem("TUNEIN","stationurl","/v1/playback/station/s249983",None,True,"Christian Hits"))
            selections.append(ContentItem("UPNP",None,"http://192.168.1.186:8123/api/tts_proxy/c96b99f3a949febd2a1f680e3b6dc4f01eb67e68_en_-_google_translate.mp3","UPnPUserName",True))
            selections.append(ContentItem("LOCAL_INTERNET_RADIO","stationurl","https://content.api.bose.io/core02/svc-bmx-adapter-orion/prod/orion/station?data=eyJuYW1lIjoiSm1uIDgwOTYiLCJpbWFnZVVybCI6IiIsInN0cmVhbVVybCI6Imh0dHA6Ly9qbThuLi5jb20vODA5Ni9zdHJlYW0ifQ%3D%3D",None,True,"Jmn 8096"))
            selections.append(ContentItem("TUNEIN","stationurl","/v1/playback/station/s309605",None,True,"K-LOVE 90s"))

            # play them all
            selection:ContentItem
            for selection in selections:
                msg:SoundTouchMessage = client.SelectContentItem(selection, 10)
            
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectPreset(self):
        """
        Test SelectPreset method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined presets.
            presets:PresetList = self._GetAndDisplayPresetList(client, _logsi)
            
            # process list in reverse, so we wind up on preset 1.
            preset:Preset = None
            for i, preset in reversed(list(enumerate(presets))):
            
                print("Selecting Preset: '%s' - %s" % (preset.Name, preset.Location))
                _logsi.LogMessage("Selecting Preset: '%s' - %s" % (preset.Name, preset.Location), colorValue=SIColors.LightGreen)
                
                # get current nowPlaying status.
                statBefore:NowPlayingStatus = client.GetNowPlayingStatus(True)

                # select a preset, and delay 10 seconds after for the device to process the change.
                client.SelectPreset(preset, 10)
            
                # get current nowPlaying status.
                statAfter:NowPlayingStatus = client.GetNowPlayingStatus(True)

                # test assertions.
                self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                self.assertIn(statAfter.PlayStatus, ["PLAY_STATE","BUFFERING_STATE",None], "NowPlayingStatus PlayStatus should be PLAY_STATE or BUFFERING_STATE after SelectPreset(), or None if device is in STANDBY")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectPreset1(self):
        """
        Test SelectPreset1 method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # select the preset, and delay 3 seconds after for the device to process the change.
            client.SelectPreset1()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectPreset2(self):
        """
        Test SelectPreset2 method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # select the preset, and delay 3 seconds after for the device to process the change.
            client.SelectPreset2()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectPreset3(self):
        """
        Test SelectPreset3 method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # select the preset, and delay 3 seconds after for the device to process the change.
            client.SelectPreset3()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectPreset4(self):
        """
        Test SelectPreset4 method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # select the preset, and delay 3 seconds after for the device to process the change.
            client.SelectPreset4()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectPreset5(self):
        """
        Test SelectPreset5 method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # select the preset, and delay 3 seconds after for the device to process the change.
            client.SelectPreset5()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectPreset6(self):
        """
        Test SelectPreset6 method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # select the preset, and delay 3 seconds after for the device to process the change.
            client.SelectPreset6()
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectRecent(self):
        """
        Test SelectRecent method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined recents.
            recents:RecentList = self._GetAndDisplayRecentList(client, _logsi)
            
            # process list.
            recent:Recent = None
            for i, recent in list(enumerate(recents)):
            
                print("Selecting Recent: '%s' - %s" % (recent.Name, recent.Location))
                _logsi.LogMessage("Selecting Recent: '%s' - %s" % (recent.Name, recent.Location), colorValue=SIColors.LightGreen)
                
                # get current nowPlaying status.
                statBefore:NowPlayingStatus = client.GetNowPlayingStatus(True)

                # select a recent, and delay 10 seconds after for the device to process the change.
                client.SelectRecent(recent, 10)
            
                # get current nowPlaying status.
                statAfter:NowPlayingStatus = client.GetNowPlayingStatus(True)

                # test assertions.
                self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                self.assertIn(statAfter.PlayStatus, ["PLAY_STATE","BUFFERING_STATE",None], "NowPlayingStatus PlayStatus should be PLAY_STATE or BUFFERING_STATE after SelectRecent(), or None if device is in STANDBY")
                
                # only process a few of the recent entries, as there could be a lot.
                if i >= 2:
                    break
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectSource(self):
        """
        Test SelectSource method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # ensure the source changes.
            inputSource:SoundTouchSources = SoundTouchSources.BLUETOOTH
            inputSourceAccount = None
            if statBefore.Source == inputSource.value:
                inputSource = SoundTouchSources.AUX
                inputSourceAccount = SoundTouchSources.AUX.value

            # select an input source.
            msg:SoundTouchMessage = client.SelectSource(inputSource, inputSourceAccount)
            
            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(msg, (SoundTouchMessage), "Result object should be of type SoundTouchMessage")
            self.assertNotIn(statAfter.Source, [SoundTouchSources.INVALID.value, SoundTouchSources.STANDBY.value], "NowPlayingStatus Source should not be INVALID_SOURCE or STANDBY")
            self.assertNotEqual(statBefore.Source, statAfter.Source, "NowPlayingStatus Source should have changed after select_source()")

            # test invalid source select exception.
            with self.assertRaises(Exception, msg="Should have raised Exception since invalid source was specified"):

                _logsi.LogMessage("Testing invalid source selection ...", colorValue=SIColors.LightGreen)
                print("Testing invalid source selection ...")

                # select an invalid input source.
                msg:SoundTouchMessage = client.SelectSource('MY_INVALID_SOURCE')

                # was a message returned in the result?
                if msg.HasXmlMessage:
                    _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                    print("(result): %s" % (msg.XmlMessage))

            # play original source (if one was selected).
            if statBefore.ContentItem.Source != "STANDBY":
                client.SelectContentItem(statBefore.ContentItem)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectSource_allSources(self):
        """
        Test SelectSource method scenarios for ALL sources.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of source items.
            source_items:SourceList = client.GetSourceList()
            
            # trace.
            _logsi.LogArray(SILevel.Message, source_items.ToString(), source_items, colorValue=SIColors.LightGreen)
            print(source_items.ToString())
            
            # select each source.
            source_item:SourceItem
            for source_item in source_items:

                # trace.
                _logsi.LogMessage("Selecting Source='%s', SourceAccount='%s'" % (source_item.Source, source_item.SourceAccount), colorValue=SIColors.LightGreen)
                print("Selecting Source='%s', SourceAccount='%s'" % (source_item.Source, source_item.SourceAccount))
                    
                # select an input source.
                msg:SoundTouchMessage = client.SelectSource(source_item.Source, source_item.SourceAccount)
            
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SetBassLevel(self):
        """
        Test SetBassLevel method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current bass level.
            bassBefore:Bass = client.GetBass(True)
            _logsi.LogObject(SILevel.Message, "(before): %s" % (bassBefore.ToString()), bassBefore, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print("(before): %s" % (bassBefore.ToString()))
            
            # for testing purposes, use a bass level of 0 (max).  if the bass level is currently at 0,
            # then we will use a value of -9 (min).
            # you can also call "GetBassCapabilities()" method to retrieve min / max bass levels.
            BASS_VALUE:int = 0
            if bassBefore.Actual == BASS_VALUE:
                BASS_VALUE = -9

            # set bass to specific level.
            msg:SoundTouchMessage = client.SetBassLevel(BASS_VALUE)
            
            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))
            
            # get current bass level.
            bassAfter:Bass = client.GetBass(True)
            _logsi.LogObject(SILevel.Message, "(after):  %s" % (bassAfter.ToString()), bassAfter, colorValue=SIColors.LightGreen, excludeNonPublic=True)
            print("(after):  %s" % (bassAfter.ToString()))

            # test assertions.
            self.assertIsInstance(msg, (SoundTouchMessage), "Result object should be of type SoundTouchMessage")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SetName(self):
        """
        Test SetName method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            oldName:str = client.Device.DeviceName
            print("Name Before: '%s'" % client.Device.DeviceName)
    
            # set the device name.
            client.SetName('SoundTouch 10B')

            print("Name After:  '%s'" % client.Device.DeviceName)

            # test assertions.
            self.assertNotEqual(oldName, client.Device.DeviceName, "DeviceName should not be the same before and after SetName()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SetVolumeLevel(self):
        """
        Test SetVolumeLevel method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current volume levels.
            volBefore:Volume = self._GetAndDisplayVolume(client, "(before) ", _logsi)
            
            # for testing purposes, use a volume of 30.  if the volume is currently at 30,
            # then we will use a volume of 25.
            VOLUME_VALUE:int = 30
            if volBefore.Actual == VOLUME_VALUE:
                VOLUME_VALUE = 25

            # set volume to specific level.
            client.SetVolumeLevel(VOLUME_VALUE)
            
            # get current volume levels.
            volAfter:Volume = self._GetAndDisplayVolume(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(volAfter, (Volume), "Returned volume object should be of type Volume")
            self.assertNotEqual(volBefore.Actual, volAfter.Actual, "Actual property should not be the same before and after SetVolumeLevel()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_StorePreset(self):
        """
        Test StorePreset method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined presets.
            presetsBefore:PresetList = self._GetAndDisplayPresetList(client, _logsi)

            # create a new preset - radio station.
            new_preset_radio:Preset = Preset(
                4,
                time.time(),
                None,
                "TUNEIN",
                "stationurl",
                "/v1/playback/station/s309605",
                "",
                True,
                "My Copy K-Love 90s",
                "http://cdn-profiles.tunein.com/s309605/images/logog.png?t=637986891960000000"
                )
            
            print("Storing Preset: '%s' - %s" % (new_preset_radio.Name, new_preset_radio.Location))
            _logsi.LogObject(SILevel.Message, "Storing Preset: '%s' - %s" % (new_preset_radio.Name, new_preset_radio.Location), new_preset_radio, colorValue=SIColors.LightGreen, excludeBuiltIn=True)

            _logsi.LogXml(SILevel.Message, "Preset XML representation", new_preset_radio.ToXmlString('utf-8'), colorValue=SIColors.LightGreen)
            _logsi.LogXml(SILevel.Message, "Preset Display representation", new_preset_radio.ToString(), colorValue=SIColors.LightGreen)
                
            # store preset.
            client.StorePreset(new_preset_radio)
            
            # get list of defined presets.
            presetsAfter:PresetList = self._GetAndDisplayPresetList(client, _logsi)

            # test assertions.
            #self.assertNotEqual(statBefore.StationName, statAfter.StationName, "nowPlaying StationName should have changed after StorePreset(); note that you should select preset #1 prior to running this test.  the presets will be processed in reverse, and will end up with preset #1 selected if all tests pass.  this test will fail if there is only 1 preset.")
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_StoreSnapshot(self):
        """
        Test StoreSnapshot method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current settings that will be restored by the snapshot.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)
            volBefore:Volume = self._GetAndDisplayVolume(client, "(before) ", _logsi)
            
            # store current settings to snapshot.
            client.StoreSnapshot()
            
            print("Changing Source, Volume, Mute, and NowPlaying settings on the device ...")

            # select a different source.
            client.SelectSource(SoundTouchSources.BLUETOOTH)
            
            # change the volume level.
            client.SetVolumeLevel(5)
            time.sleep(1)

            # mute the device.
            client.mute_on()
            time.sleep(1)

            # get current settings before the snapshot restore.
            statTemp:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(temp)   ", _logsi)
            volTemp:Volume = self._GetAndDisplayVolume(client, "(temp)   ", _logsi)
            
            # restore settings from snapshot.
            client.RestoreSnapshot()

            # get current settings after the snapshot restore.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)
            volAfter:Volume = self._GetAndDisplayVolume(client, "(after)  ", _logsi)
            
            # test assertions.
            self.assertEqual(statBefore.Source, statAfter.Source, "NowPlayingStatus Before / After Source values should be equal after restoring the snapshot")
            self.assertEqual(statBefore.ContentItem.ItemType, statAfter.ContentItem.ItemType, "NowPlayingStatus Before / After ContentItem ItemType values should be equal after restoring the snapshot")
            self.assertEqual(statBefore.ContentItem.Location, statAfter.ContentItem.Location, "NowPlayingStatus Before / After ContentItem Location values should be equal after restoring the snapshot")
            self.assertEqual(statBefore.ContentItem.SourceAccount, statAfter.ContentItem.SourceAccount, "NowPlayingStatus Before / After ContentItem SourceAccount values should be equal after restoring the snapshot")
            self.assertEqual(volBefore.Actual, volAfter.Actual, "Volume Before / After actual values should be equal after restoring the snapshot")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_ThumbsDown(self):
        """
        Test ThumbsDown method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # can the nowPlaying item be a favorite?
            if statBefore.IsFavoriteEnabled:
                
                # remove the currently playing media from the device favorites.
                client.ThumbsDown()
            
                # give the device time to process the change.
                time.sleep(1)
            
                # get current nowPlaying status.
                statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

                # test assertions.
                self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                if statBefore.IsFavoriteEnabled:
                    self.assertEqual(statAfter.IsFavorite, False, "NowPlayingStatus IsFavorite should be False")
                    
            else:
                
                print("Favorites not enabled for currently playing media")
                
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_ThumbsUp(self):
        """
        Test ThumbsUp method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main            
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # can the nowPlaying item be a favorite?
            if statBefore.IsFavoriteEnabled:
                
                # add the currently playing media to the device favorites.
                client.ThumbsUp()
            
                # give the device time to process the change.
                time.sleep(1)
            
                # get current nowPlaying status.
                statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

                # test assertions.
                self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
                if statBefore.IsFavoriteEnabled:
                    self.assertEqual(statAfter.IsFavorite, True, "NowPlayingStatus IsFavorite should be True")
                    
            else:
                
                print("Favorites not enabled for currently playing media")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_VolumeDown(self):
        """
        Test VolumeDown method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current volume levels.
            volBefore:Volume = self._GetAndDisplayVolume(client, "(before) ", _logsi)

            # turn volume down a notch.
            client.VolumeDown()
            
            # get current volume levels.
            volAfter:Volume = self._GetAndDisplayVolume(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(volAfter, (Volume), "Returned volAfter object should be of type Volume")
            self.assertNotEqual(volBefore.Actual, volAfter.Actual, "Volume Actual property should not be the same before and after. is the device turned on?")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_VolumeUp(self):
        """
        Test VolumeUp method scenarios.
        """
        # set SmartInspect logger reference.        
        _logsi:SISession = SIAuto.Main
        # set method name for console output.
        methodName:str = SISession.GetMethodName()

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current volume levels.
            volBefore:Volume = self._GetAndDisplayVolume(client, "(before) ", _logsi)

            # turn volume up a notch.
            client.VolumeUp()
            
            # get current volume levels.
            volAfter:Volume = self._GetAndDisplayVolume(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(volAfter, (Volume), "Returned volume object should be of type Volume")
            self.assertNotEqual(volBefore.Actual, volAfter.Actual, "Volume Actual property should not be the same before and after. is the device turned on?")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    # def _DISABLED_test_StatusNotifications(self):
    #     """
    #     Test Mute method scenarios.
    #     """
    #     # set SmartInspect logger reference.        
    #     _logsi:SISession = SIAuto.Main            
    #     # set method name for console output.
    #     methodName:str = SISession.GetMethodName()

    #     try:

    #         print("Test Starting:  %s" % methodName)
    #         _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

    #         # create BoseDevice instance.
    #         client:SoundTouchClient = self._CreateApiClient()

    #         # fetch device's capabilities - must have IsWebSocketApiProxyCapable=True in order to support notifications.
    #         capabilities = client.GetCapabilities()
    #         if capabilities.IsWebSocketApiProxyCapable:
                
    #             # create and start a websocket to receive notifications from the device.
    #             socket:SoundTouchWebSocket = SoundTouchWebSocket(client.Device)
                
    #             # add our listener(s) that will handle SoundTouch device status updates.
    #             socket.add_listener(SoundTouchNotifyCategorys.ALL, self._OnSoundTouchUpdateEvent)
                
    #             # start receiving updates.
    #             socket.start_notification()

    #         # for testing status notifications.
    #         # start the test with the SoundTouch device power off (standby mode).
    #         maxcnt:int = 20
    #         for i in range(maxcnt):
    #             time.sleep(1)

    #             # first test is to power on.
    #             if i == 0:
    #                 func = "client.power_on()"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.power_on()
    #                 time.sleep(2)

    #             if i == 2:
    #                 func = "client.volume_up()"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.volume_up()
    #                 time.sleep(2)

    #             if i == 4:
    #                 func = "client.volume_down()"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.volume_down()
    #                 time.sleep(2)

    #             if i == 6:
    #                 func = "client.mute()"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.mute()
    #                 time.sleep(2)
                    
    #             if i == 8:
    #                 func = "client.mute()"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.mute()
    #                 time.sleep(2)

    #             if i == 10:
    #                 func = "client.pause()"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.pause()
    #                 time.sleep(2)

    #             if i == 12:
    #                 func = "client.resume()"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.resume()
    #                 time.sleep(2)

    #             if i == 14:
    #                 func = "client.SetVolumeLevel(30)"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.SetVolumeLevel(50)
    #                 time.sleep(2)

    #             if i == 16:
    #                 func = "client.SetVolumeLevel(20)"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.SetVolumeLevel(10)
    #                 time.sleep(2)

    #             # last test is to power off (standby).
    #             if i == (maxcnt - 1):
    #                 func = "client.power_off()"
    #                 print("%s - %s", str(i), func)
    #                 _logsi.LogMessage("Testing method: %s", func)
    #                 client.power_off()

    #         # with self.assertRaises(Exception, msg="Should have raised Exception since dictionary key was not found and raiseExceptionIfNotFound=True."):
    #         #     result = svc.GetDictKeyValueBool(dictStringTrue, KEY_NAME_NOTFOUND, True)
    #         # result = svc.GetDictKeyValueBool(dictStringTrue, KEY_NAME_NOTFOUND, False)
    #         # self.assertIsNone(result, "Should have returned None since dictionary key was not found and raiseExceptionIfNotFound=False.")

    #         print("Mute Tests Completed")

    #     except Exception as ex:

    #         _logsi.LogException("Test Exception: %s" % (methodName), ex)
    #         print("** Exception: %s" % str(ex))
    #         raise
        
    #     finally:
            
    #         # stop listening for Bose SoundTouch status updates.
    #         if (socket):
    #             socket.stop_notification()


# execute unit tests.
if __name__ == '__main__':
    unittest.main()
