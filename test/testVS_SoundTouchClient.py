import sys
sys.path.append("..")

import time
import unittest

# external package imports.
from collections.abc import Iterable 
import time
from smartinspectpython.siauto import *
from xml.etree.ElementTree import Element
from xml.etree import ElementTree

# our package imports.
from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *
from bosesoundtouchapi.ws import *

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# SoundTouchClient Tests - Single Device Environment
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

class Test_SoundTouchClient_OneDevice(unittest.TestCase):
    """
    Test client scenarios that utilize a single device.
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
                    
    
    def _CreateApiClient(self, ipAddress:str=None) -> SoundTouchClient:
        """
        Creates a new SoundTouchClient instance, and sets all properties for executing these test cases.

        Args:
            ipAddress (str):
                SoundTouch device IP Address to connect to; otherwise, None to use the default.
        
        Returns:
            An SoundTouchClient instance.
        """
        _logsi:SISession = SIAuto.Main            

        try:

            # set ip address of SoundTouch device to connect to.
            if ipAddress is None:
                ipAddress = "192.168.1.131" # Bose SoundTouch 10
                #ipAddress = "192.168.1.130" # Bose SoundTouch 300
                #ipAddress = "192.168.1.133" # non-existant ip
                #ipAddress = "x.168.1.133"   # invalid ip

            # create SoundTouchDevice instance.
            device:SoundTouchDevice = SoundTouchDevice(ipAddress)
            
            # create SoundTouchClient instance from device.
            client:SoundTouchClient = SoundTouchClient(device)
                       
            # return instance to caller.
            return client

        except Exception as ex:

            _logsi.LogException("Exception in Test Method \"{0}\"".format(SISession.GetMethodName()), ex)
            print("** Exception: %s" % str(ex))
            raise


    def _OnSoundTouchUpdateEvent(self, args:Element) -> None:
        
        _logsi:SISession = SIAuto.Main            

        if (args != None):
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device status update: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen)
            print("Status update args: %s", argsEncoded)
        

    def _OnSoundTouchInfoEvent(self, args:Element) -> None:
        
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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_Action"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_AddFavorite"

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
        

    def test_AddMusicServiceSources(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_AddMusicServiceSources"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined sources.
            sourceList:SourceList = client.GetSourceList()
            print("\nSource list before the change:\n%s" % sourceList.ToString(True))
    
            # get list of upnp media services detected by the device.
            mediaServerList:MediaServerList = client.GetMediaServerList()
            print("\nUPnP Media Server list before the change:\n%s" % mediaServerList.ToString(True))
    
            # ensure all upnp media servers are defined as sources.
            print("\n\nVerifying UPnP media servers are defined as sources ...")
            sourcesAdded:list[str] = client.AddMusicServiceSources()
            if len(sourcesAdded) == 0:
                print(" *** All UPnP media servers are already defined as sources")
            else:
                print("Sources added:\n%s" % str(sourcesAdded))

                # get list of defined sources.
                sourceList:SourceList = client.GetSourceList()
                print("\nSource list after the change:\n%s" % sourceList.ToString(True))

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    # def test_Bookmark(self):

    #     _logsi:SISession = SIAuto.Main            
    #     methodName:str = "test_Bookmark"

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
        

    def test_Get(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_Get"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get configuration for specified node.
            msg:SoundTouchMessage = client.Get(SoundTouchNodes.volume)
    
            if msg != None:
                ElementTree.indent(msg.Response)  # for pretty printing
                responseEncoded = ElementTree.tostring(msg.Response, encoding="unicode")
                print("Get Response Message:\n%s" %  responseEncoded)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetAudioDspControls(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetAudioDspControls"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

            # get real-time configuration from the device.
            # note that not all devices support retrieval of this information.
            config:AudioDspControls = client.GetAudioDspControls()
            print(config.ToString())
            print("\nCurrent Audio DSP Controls Supported Audio Modes array: %s" % (config.ToSupportedAudioModesArray()))

            # get cached configuration, refreshing from device if needed.
            config:AudioDspControls = client.GetAudioDspControls(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.audiodspcontrols.Path in client.ConfigurationCache:
                config:AudioDspControls = client.ConfigurationCache[SoundTouchNodes.audiodspcontrols.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                config:AudioDspControls = client.GetAudioDspControls()

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetAudioProductLevelControls(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetAudioProductLevelControls"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

            # get real-time configuration from the device.
            # note that not all devices support retrieval of this information.
            config:AudioProductLevelControls = client.GetAudioProductLevelControls()
            print(config.ToString())

            # get cached configuration, refreshing from device if needed.
            config:AudioProductLevelControls = client.GetAudioProductLevelControls(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.audioproductlevelcontrols.Path in client.ConfigurationCache:
                config:AudioProductLevelControls = client.ConfigurationCache[SoundTouchNodes.audioproductlevelcontrols.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                config:AudioProductLevelControls = client.GetAudioProductLevelControls()

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetAudioProductToneControls(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetAudioProductToneControls"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

            # get real-time configuration from the device.
            # note that not all devices support retrieval of this information.
            config:AudioProductToneControls = client.GetAudioProductToneControls()
            print(config.ToString())

            print("\nBass Range values: %s" % config.Bass.ToMinMaxString())
            print("Treble Range values: %s" % config.Treble.ToMinMaxString())

            # get cached configuration, refreshing from device if needed.
            config:AudioProductToneControls = client.GetAudioProductToneControls(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.audioproducttonecontrols.Path in client.ConfigurationCache:
                config:AudioProductToneControls = client.ConfigurationCache[SoundTouchNodes.audioproducttonecontrols.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                config:AudioProductToneControls = client.GetAudioProductToneControls()

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetAudioSpeakerAttributeAndSetting(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetAudioSpeakerAttributeAndSetting"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

            # get real-time configuration from the device.
            # note that not all devices support retrieval of this information.
            config:AudioSpeakerAttributeAndSetting = client.GetAudioSpeakerAttributeAndSetting()
            print(config.ToString())

            # get cached configuration, refreshing from device if needed.
            config:AudioSpeakerAttributeAndSetting = client.GetAudioSpeakerAttributeAndSetting(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.audiospeakerattributeandsetting.Path in client.ConfigurationCache:
                config:AudioSpeakerAttributeAndSetting = client.ConfigurationCache[SoundTouchNodes.audiospeakerattributeandsetting.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                config:AudioSpeakerAttributeAndSetting = client.GetAudioSpeakerAttributeAndSetting()

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetBalance(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetBalance"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetBass"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetBassCapabilities"

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
        

    def test_GetBlueToothInfo(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetBlueToothInfo"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()
            
            # get real-time configuration from the device.
            config:BlueToothInfo = client.GetBlueToothInfo()
            print(config.ToString())

            # get cached configuration, refreshing from device if needed.
            config:BlueToothInfo = client.GetBlueToothInfo(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.bluetoothInfo.Path in client.ConfigurationCache:
                config:BlueToothInfo = client.ConfigurationCache[SoundTouchNodes.bluetoothInfo.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetCapabilities(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetCapabilities"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetClockConfig"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetClockTime"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetDspMono"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetLanguage"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetMediaServerList"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetName"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetNetworkInfo"

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
                self.assertIsNotNone(intfc.TypeValue, "NetworkInfoInterface TypeValue property should not be None")
                self.assertIsNotNone(intfc.State, "NetworkInfoInterface State property should not be None")
                self.assertIsNotNone(intfc.MacAddress, "NetworkInfoInterface MacAddress property should not be None")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetNetworkStatus(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetNetworkStatus"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetNowPlayingStatus"

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
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_GetOptions"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetPowerManagement"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetPresetList"

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
        

    def test_GetProductCecHdmiControl(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetProductCecHdmiControl"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

            # get real-time configuration from the device.
            # note that not all devices support retrieval of this information.
            config:ProductCecHdmiControl = client.GetProductCecHdmiControl()
            print(config.ToString())

            # get cached configuration, refreshing from device if needed.
            config:ProductCecHdmiControl = client.GetProductCecHdmiControl(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.productcechdmicontrol.Path in client.ConfigurationCache:
                config:ProductCecHdmiControl = client.ConfigurationCache[SoundTouchNodes.productcechdmicontrol.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                config:ProductCecHdmiControl = client.GetProductCecHdmiControl()

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetProductHdmiAssignmentControls(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetProductHdmiAssignmentControls"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

            # get real-time configuration from the device.
            # note that not all devices support retrieval of this information.
            config:ProductHdmiAssignmentControls = client.GetProductHdmiAssignmentControls()
            print(config.ToString())

            # get cached configuration, refreshing from device if needed.
            config:ProductHdmiAssignmentControls = client.GetProductHdmiAssignmentControls(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.producthdmiassignmentcontrols.Path in client.ConfigurationCache:
                config:ProductHdmiAssignmentControls = client.ConfigurationCache[SoundTouchNodes.producthdmiassignmentcontrols.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                config:ProductHdmiAssignmentControls = client.GetProductHdmiAssignmentControls()

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetReBroadcastLatencyMode(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetReBroadcastLatencyMode"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get real-time configuration from the device.
            # note that not all devices support retrieval of this information.
            config:RebroadcastLatencyMode = client.GetReBroadcastLatencyMode()
            print(config.ToString())

            # get cached configuration, refreshing from device if needed.
            config:RebroadcastLatencyMode = client.GetReBroadcastLatencyMode(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.rebroadcastlatencymode.Path in client.ConfigurationCache:
                config:RebroadcastLatencyMode = client.ConfigurationCache[SoundTouchNodes.rebroadcastlatencymode.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetRecentList(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetRecentList"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetRequestToken"

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
        

    def test_GetServiceAvailability(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetServiceAvailability"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get real-time configuration from the device.
            config:ServiceAvailability = client.GetServiceAvailability()
            print(config.ToString(True))

            # get cached configuration, refreshing from device if needed.
            config:ServiceAvailability = client.GetServiceAvailability(False)
            print("\nCached configuration:\n%s" % config.ToString(True))

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.serviceAvailability.Path in client.ConfigurationCache:
                config:ServiceAvailability = client.ConfigurationCache[SoundTouchNodes.serviceAvailability.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString(True))
        
            # sort the list (in place) by ServiceType, ascending order.
            config.Services.sort(key=lambda x: x.ServiceType or "", reverse=False)
            print("\nList sorted by ServiceType:\n%s" % config.ToString(True))
           
            # sort the list (in place) by IsAvailable, ascending order.
            config.Services.sort(key=lambda x: x.IsAvailable or False, reverse=False)
            print("\nList sorted by IsAvailable:\n%s" % config.ToString(True))
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetSoftwareUpdateCheckInfo(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetSoftwareUpdateCheckInfo"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get real-time configuration from the device.
            config:SoftwareUpdateCheckResponse = client.GetSoftwareUpdateCheckInfo()
            print(config.ToString())

            # get cached configuration, refreshing from device if needed.
            config:SoftwareUpdateCheckResponse = client.GetSoftwareUpdateCheckInfo(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.swUpdateCheck.Path in client.ConfigurationCache:
                config:SoftwareUpdateCheckResponse = client.ConfigurationCache[SoundTouchNodes.swUpdateCheck.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetSoftwareUpdateStatus(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetSoftwareUpdateStatus"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get real-time configuration from the device.
            config:SoftwareUpdateQueryResponse = client.GetSoftwareUpdateStatus()
            print(config.ToString())

            # get cached configuration, refreshing from device if needed.
            config:SoftwareUpdateQueryResponse = client.GetSoftwareUpdateStatus(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.swUpdateQuery.Path in client.ConfigurationCache:
                config:SoftwareUpdateQueryResponse = client.ConfigurationCache[SoundTouchNodes.swUpdateQuery.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetSoundTouchConfigurationStatus(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetSoundTouchConfigurationStatus"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get real-time configuration from the device.
            config:SoundTouchConfigurationStatus = client.GetSoundTouchConfigurationStatus()
            print(config.ToString())

            # get cached configuration, refreshing from device if needed.
            config:SoundTouchConfigurationStatus = client.GetSoundTouchConfigurationStatus(False)
            print("\nCached configuration:\n%s" % config.ToString())

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.soundTouchConfigurationStatus.Path in client.ConfigurationCache:
                config:SoundTouchConfigurationStatus = client.ConfigurationCache[SoundTouchNodes.soundTouchConfigurationStatus.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString())
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_GetSourceList(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetSourceList"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetSystemTimeout"

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
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_GetVolume"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetWirelessProfile"

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
        

    def test_GetWirelessSiteSurvey(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetWirelessSiteSurvey"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get real-time configuration from the device.
            config:PerformWirelessSiteSurveyResponse = client.GetWirelessSiteSurvey()
            print(config.ToString(True))

            # get cached configuration, refreshing from device if needed.
            config:PerformWirelessSiteSurveyResponse = client.GetWirelessSiteSurvey(False)
            print("\nCached configuration:\n%s" % config.ToString(True))

            # get cached configuration directly from the configuration manager dictionary.
            if SoundTouchNodes.performWirelessSiteSurvey.Path in client.ConfigurationCache:
                config:PerformWirelessSiteSurveyResponse = client.ConfigurationCache[SoundTouchNodes.performWirelessSiteSurvey.Path]
                print("\nCached configuration, direct:\n%s" % config.ToString(True))
           
            # sort the list (in place) by SignalStrength, ascending order.
            config.SurveyResultItems.sort(key=lambda x: x.SignalStrength or 0, reverse=False)
            print("\nList sorted by SignalStrength:\n%s" % config.ToString(True))
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MakeRequest(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MakeRequest"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaNextTrack"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaPause"

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
            self.assertIn(statAfter.PlayStatus, ["PAUSE_STATE","STOP_STATE",None], "NowPlayingStatus PlayStatus should be PAUSE_STATE, STOP_STATE, or None if device is in STANDBY")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_MediaPlay(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaPlay"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaPlayPause"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaPreviousTrack"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaRepeatAll"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaRepeatOff"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaRepeatOne"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaResume"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaShuffleOff"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaShuffleOn"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MediaStop"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # stop nowPlaying media.
            client.MediaStop()
            
            time.sleep(3)
            
            # get current nowPlaying status.
            statAfter:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(after)  ", _logsi)

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertIn(statAfter.PlayStatus, ["PAUSE_STATE","STOP_STATE",None], "NowPlayingStatus PlayStatus should be STOP_STATE after MediaStop(), or None if device is in STANDBY")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_Mute(self):
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_Mute"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MuteOff"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_MuteOn"

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
            self.assertEqual(volAfter.IsMuted, True, "volume IsMuted should be True after MuteOn()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_PlayContentItem(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_PlayContentItem"

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
        

    def test_PlayNotificationBeep(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_PlayNotificationBeep"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # play a notification beep.
            print("\nPlaying notification beep ...")
            client.PlayNotificationBeep()
                    
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_PlayNotificationTTS(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_PlayNotificationTTS"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            statBefore:NowPlayingStatus = self._GetAndDisplayNowPlayingStatus(client, "(before) ", _logsi)

            # use google text to speech to say a message.
            print("\nSaying message via Google TTS (language=EN) ...")
            msg:SoundTouchMessage = client.PlayNotificationTTS("a.There is activity at the front door.")
   
            # was a message returned in the result?
            if msg.HasXmlMessage:
                _logsi.LogMessage("(result): %s" % (msg.XmlMessage), colorValue=SIColors.LightGreen)
                print("(result): %s" % (msg.XmlMessage))
   
            # if playing messages back to back, then give the message time to play
            # before playing the next one; otherwise the next message is lost.
            time.sleep(6)

            # use google text to speech to say a message.
            print("\nSaying message via Google TTS (language=DE) ...")
            msg:SoundTouchMessage = client.PlayNotificationTTS("a.There is activity at the front door.", 
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
            msg:SoundTouchMessage = client.PlayNotificationTTS("a.There is activity at the front door.", 
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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_PlayUrl"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_Power"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_PowerOff"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_PowerOn"

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
        

    def test_PowerStandby(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_PowerStandby"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("(before): '%s' - '%s'" % (nowPlaying.Source, nowPlaying.ContentItem.Name))
    
            # power standby (off) the device.
            client.PowerStandby()

            # get current nowPlaying status.
            statAfter:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("(after):  '%s' - '%s'" % (statAfter.Source, statAfter.ContentItem.Name))

            # test assertions.
            self.assertIsInstance(statAfter, (NowPlayingStatus), "Returned status object should be of type NowPlayingStatus")
            self.assertEqual(statAfter.Source, "STANDBY", "NowPlayingStatus should be STANDBY after PowerStandby()")

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_Put(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_Put"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # update configuration for specified node.
            msg:SoundTouchMessage = client.Put(SoundTouchNodes.volume, '<volume>10</volume>')
    
            if msg != None:
                ElementTree.indent(msg.Response)  # for pretty printing
                responseEncoded = ElementTree.tostring(msg.Response, encoding="unicode")
                print("Put Response Message:\n%s" %  responseEncoded)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_RemoveAllPresets(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_RemoveAllPresets"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined presets.
            presetsBefore:PresetList = self._GetAndDisplayPresetList(client, _logsi)

            # remove all stored presets.
            print("\nRemoving all presets ...")
            client.RemoveAllPresets()
            
            # give the device time to process the change.
            time.sleep(1)
            
            # get list of defined presets.
            presetsAfter:PresetList = self._GetAndDisplayPresetList(client, _logsi)
            
            # re-add presets from before.
            print("\nRestoring presets from before the removal ...")
            preset:Preset
            for preset in presetsBefore:
                print("- Adding preset: %s" % preset.Name)
                client.StorePreset(preset)
           
            # get list of defined presets.
            print("\nRestored presets ...")
            presetsRestored:PresetList = self._GetAndDisplayPresetList(client, _logsi)
            
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_RemoveFavorite(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_RemoveFavorite"

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
        

    def test_RemoveMusicServiceAccount(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_RemoveMusicServiceAccount"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined sources.
            sourceList:SourceList = client.GetSourceList()
            print("\nSource list before the change:\n%s" % sourceList.ToString(True))
    
            # remove music service account source.
            print("\n\nRemoving music service source: Source='STORED_MUSIC', Account='d09708a1-5953-44bc-a413-7d516e04b819' ...")
            client.RemoveMusicServiceAccount("STORED_MUSIC", "THLUCASI9: THLUCASI9 Media Library", "d09708a1-5953-44bc-a413-7d516e04b819/0", None)
               
            # get list of defined sources.
            sourceList:SourceList = client.GetSourceList()
            print("\nSource list after the set:\n%s" % sourceList.ToString(True))
                
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_RemovePreset(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_RemovePreset"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined presets.
            presetsBefore:PresetList = self._GetAndDisplayPresetList(client, _logsi)

            # remove specified preset id.
            print("\nRemoving preset id=4 ...")
            client.RemovePreset(4)
            
            # get list of defined presets.
            print("\nUpdated presets ...")
            presetsAfter:PresetList = self._GetAndDisplayPresetList(client, _logsi)
           
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectContentItem(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectContentItem"

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
        

    def test_SelectLastSoundTouchSource(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectLastSoundTouchSource"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            nowPlayingBefore:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("\n** Current Now Playing Status:\n%s" % nowPlayingBefore.ToString())

            # select last soundtouch source.
            client.SelectLastSoundTouchSource()

            # get current nowPlaying status.
            nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("\n** Updated Now Playing Status:\n%s" % nowPlaying.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectLastSource(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectLastSource"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            nowPlayingBefore:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("\n** Current Now Playing Status:\n%s" % nowPlayingBefore.ToString())

            # select last source.
            client.SelectLastSource()

            # get current nowPlaying status.
            nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("\n** Updated Now Playing Status:\n%s" % nowPlaying.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectLastWifiSource(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectLastWifiSource"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            nowPlayingBefore:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("\n** Current Now Playing Status:\n%s" % nowPlayingBefore.ToString())

            # select last wifi source.
            client.SelectLastWifiSource()

            # get current nowPlaying status.
            nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("\n** Updated Now Playing Status:\n%s" % nowPlaying.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectLocalSource(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectLocalSource"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get current nowPlaying status.
            nowPlayingBefore:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("\n** Current Now Playing Status:\n%s" % nowPlayingBefore.ToString())

            # select local source.
            client.SelectLocalSource()

            # get current nowPlaying status.
            nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
            print("\n** Updated Now Playing Status:\n%s" % nowPlaying.ToString())

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SelectPreset(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectPreset"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectPreset1"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectPreset2"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectPreset3"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectPreset4"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectPreset5"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectPreset6"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectRecent"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectSource"

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
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SelectSource_allSources"

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
        

    def test_SetAudioDspControls(self):
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_SetAudioDspControls"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

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
            cfgUpdate.AudioMode = SoundTouchAudioModes.NORMAL
            if cfgUpdate.AudioMode == cfgBefore.AudioMode:
                cfgUpdate.AudioMode = SoundTouchAudioModes.DIALOG
            print("\nSetting audio dsp controls AudioMode to '%s' (from '%s') ..." % (cfgUpdate.AudioMode, cfgBefore.AudioMode))

            # set audio dsp controls to specific audio mode.
            client.SetAudioDspControls(cfgUpdate)
            
            # get current audio dsp controls.
            cfgAfter:AudioDspControls = client.GetAudioDspControls(True)
            print("\nChanged audio dsp controls: \n%s" % (cfgAfter.ToString()))

            # restore audio dsp controls to original values.
            print("\nRestoring audio dsp controls to original values ...")
            client.SetAudioDspControls(cfgBefore)            

            # get current audio dsp controls.
            cfgAfter:AudioProductLevelControls = client.GetAudioDspControls(True)
            print("Restored audio dsp controls: \n%s" % (cfgAfter.ToString()))

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                client.SetAudioDspControls(cfgBefore)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SetAudioProductLevelControls(self):
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_SetAudioProductLevelControls"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

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

            # restore audio product level controls to original values.
            print("\nRestoring audio product level controls to original values ...")
            client.SetAudioProductLevelControls(cfgBefore)            

            # get current audio product level controls.
            cfgAfter:AudioProductLevelControls = client.GetAudioProductLevelControls(True)
            print("Restored audio product level controls: \n%s" % (cfgAfter.ToString()))

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                client.SetAudioProductLevelControls(cfgUpdate)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SetAudioProductToneControls(self):
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_SetAudioProductToneControls"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

            # get current audio product tone controls.
            # note that not all devices support retrieval of this information.
            cfgBefore:AudioProductToneControls = None
            cfgBefore = client.GetAudioProductToneControls()
            print("\nCurrent audio product tone controls: \n%s" % cfgBefore.ToString())
        
            # create new audio product tone controls object.
            cfgUpdate:AudioProductToneControls = AudioProductToneControls()

            # for testing purposes, toggle the Bass level.  
            # if the level is currently minValue, then we will set to maxValue.
            cfgUpdate.Bass.Value = cfgBefore.Bass.MinValue
            if cfgUpdate.Bass.Value == cfgBefore.Bass.Value:
                cfgUpdate.Bass.Value = cfgBefore.Bass.MaxValue
            print("\nSetting audio product tone controls Bass Level to '%s' (from '%s') ..." % (cfgUpdate.Bass.Value, cfgBefore.Bass.Value))
                
            # for testing purposes, toggle the Treble level.  
            # if the level is currently minValue, then we will set to maxValue.
            cfgUpdate.Treble.Value = cfgBefore.Treble.MinValue
            if cfgUpdate.Treble.Value == cfgBefore.Treble.Value:
                cfgUpdate.Treble.Value = cfgBefore.Treble.MaxValue
            print("Setting audio product tone controls Treble Level to '%s' (from '%s') ..." % (cfgUpdate.Treble.Value, cfgBefore.Treble.Value))
                
            # update audio product tone controls.
            client.SetAudioProductToneControls(cfgUpdate)
            
            # get current audio product tone controls.
            cfgAfter:AudioProductToneControls = client.GetAudioProductToneControls(True)
            print("\nChanged audio product tone controls: \n%s" % (cfgAfter.ToString()))

            # restore audio product tone controls to original values.
            print("\nRestoring audio product tone controls to original values ...")
            client.SetAudioProductToneControls(cfgBefore)            

            # get current audio product tone controls.
            cfgAfter:AudioProductToneControls = client.GetAudioProductToneControls(True)
            print("Restored audio product tone controls: \n%s" % (cfgAfter.ToString()))

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                client.SetAudioProductToneControls(cfgUpdate)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SetBassLevel(self):
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_SetBassLevel"

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
        

    def test_SetMusicServiceAccount(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SetMusicServiceAccount"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient()

            # get list of defined sources.
            sourceList:SourceList = client.GetSourceList()
            print("\nSource list before the change:\n%s" % sourceList.ToString(True))
    
            # set music service account source.
            print("\n\nAdding music service source: Source='STORED_MUSIC', Account='d09708a1-5953-44bc-a413-7d516e04b819' ...")
            client.SetMusicServiceAccount("STORED_MUSIC", "THLUCASI9: THLUCASI9 Media Library", "d09708a1-5953-44bc-a413-7d516e04b819/0", None)
                
            # get list of defined sources.
            sourceList:SourceList = client.GetSourceList()
            print("\nSource list after the set:\n%s" % sourceList.ToString(True))
                
            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SetName(self):
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_SetName"

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
        

    def test_SetProductCecHdmiControl(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_SetProductCecHdmiControl"

        try:

            print("Test Starting:  %s" % methodName)
            _logsi.LogMessage("Testing method: '%s'" % (methodName), colorValue=SIColors.LightGreen)

            # create BoseDevice instance.
            client:SoundTouchClient = self._CreateApiClient("192.168.1.130") # SoundTouch 300

            # get current product cec hdmi control.
            # note that not all devices support retrieval of this information.
            cfgBefore:ProductCecHdmiControl = None
            cfgBefore = client.GetProductCecHdmiControl()
            print("\nCurrent product cec hdmi control value: \n%s" % cfgBefore.ToString())
        
            # create new tone controls object.
            cfgUpdate:ProductCecHdmiControl = ProductCecHdmiControl()

            # for testing purposes, toggle the value from OFF to ON or vice versa.
            # if the level is currently ON, then we will set to OFF.
            cfgUpdate.CecMode = SoundTouchHdmiCecModes.OFF
            if cfgUpdate.CecMode == cfgBefore.CecMode:
                cfgUpdate.CecMode = SoundTouchHdmiCecModes.ON
            print("\nSetting product cec hdmi control to '%s' (from '%s') ..." % (cfgUpdate.CecMode, cfgBefore.CecMode))
                
            # update product cec hdmi control.
            client.SetProductCecHdmiControl(cfgUpdate)
            
            # get current product cec hdmi control.
            cfgAfter:ProductCecHdmiControl = client.GetProductCecHdmiControl(True)
            print("\nChanged product cec hdmi control: \n%s" % (cfgAfter.ToString()))

            # restore product cec hdmi control to original values.
            client.SetProductCecHdmiControl(cfgBefore)            

            # get current product cec hdmi control.
            cfgAfter:ProductCecHdmiControl = client.GetProductCecHdmiControl(True)
            print("\nRestored product cec hdmi control: \n%s" % (cfgAfter.ToString()))

            # test function not supported by device.
            with self.assertRaises(SoundTouchError, msg="\nShould have raised SoundTouchError for function not supported by device"):
                client:SoundTouchClient = self._CreateApiClient("192.168.1.131") # SoundTouch 10
                _logsi.LogMessage("Testing for function not supported by device ...", colorValue=SIColors.LightGreen)
                print("\nTesting for function not supported by device ...")
                client.SetProductCecHdmiControl(cfgUpdate)

            print("Test Completed: %s" % methodName)

        except Exception as ex:

            _logsi.LogException("Test Exception: %s" % (methodName), ex)
            print("** Exception: %s" % str(ex))
            raise
        

    def test_SetVolumeLevel(self):
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_SetVolumeLevel"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_StorePreset"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_StoreSnapshot"

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
            client.MuteOn()
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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_ThumbsDown"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_ThumbsUp"

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
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_VolumeDown"

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
        
        _logsi:SISession = SIAuto.Main
        methodName:str = "test_VolumeUp"

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
        

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# SoundTouchClient Tests - Multi-Room Environment
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

class Test_SoundTouchClient_MultiRoom(unittest.TestCase):
    """
    Test client scenarios that utilize two or more devices for multi-room (zone) functions.
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
                    
    
    def _CreateApiClient(self, ipAddress:str=None) -> SoundTouchClient:
        """
        Creates a new SoundTouchClient instance, and sets all properties for executing these test cases.

        Args:
            ipAddress (str):
                SoundTouch device IP Address to connect to; otherwise, None to use the default.
        
        Returns:
            An SoundTouchClient instance.
        """
        _logsi:SISession = SIAuto.Main            

        try:

            # set ip address of SoundTouch device to connect to.
            if ipAddress is None:
                ipAddress = "192.168.1.131" # Bose SoundTouch 10
                #ipAddress = "192.168.1.130" # Bose SoundTouch 300
                #ipAddress = "192.168.1.133" # non-existant ip
                #ipAddress = "x.168.1.133"   # invalid ip

            # create SoundTouchDevice instance.
            device:SoundTouchDevice = SoundTouchDevice(ipAddress)
            
            # create SoundTouchClient instance from device.
            client:SoundTouchClient = SoundTouchClient(device)
                       
            # return instance to caller.
            return client

        except Exception as ex:

            _logsi.LogException("Exception in Test Method \"{0}\"".format(SISession.GetMethodName()), ex)
            print("** Exception: %s" % str(ex))
            raise


    def _OnSoundTouchUpdateEvent(self, args:Element) -> None:
        _logsi:SISession = SIAuto.Main            

        if (args != None):
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device status update: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen)
            print("Status update args: %s", argsEncoded)
        

    def _OnSoundTouchInfoEvent(self, args:Element) -> None:
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

    def test_AddZoneMembers(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_AddZoneMembers"

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
        

    def test_CreateZone(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_CreateZone"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_CreateZoneFromDevices"

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
        

    def test_GetZoneStatus(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_GetZoneStatus"

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


    def test_RemoveZone(self):
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_RemoveZone"

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
        
        _logsi:SISession = SIAuto.Main            
        methodName:str = "test_RemoveZoneMembers"

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
        

# execute unit tests.
if __name__ == '__main__':
    unittest.main()
