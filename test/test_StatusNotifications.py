# external package imports.
from smartinspectpython.siauto import *
import time
from xml.etree.ElementTree import Element
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
siConfig:SIConfigurationTimer = SIConfigurationTimer(SIAuto.Si, siConfigPath)

# get smartinspect logger reference and log basic system / domain details.
_logsi:SISession = SIAuto.Main            
_logsi.LogSeparator(SILevel.Fatal)
_logsi.LogAppDomain(SILevel.Message)
_logsi.LogSystem(SILevel.Message)

class EventHandlerClass:

    def OnSoundTouchInfoEvent(self, client:SoundTouchClient, args:Element) -> None:
        if (args != None):
            ElementTree.indent(args)  # for pretty printing
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device information event: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen, prettyPrint=True)
            print("\n'%s' status update:\n%s" % (client.Device.DeviceName, argsEncoded))


    def OnSoundTouchWebSocketOpenEvent(self, client:SoundTouchClient, args:str) -> None:
        if (args != None):
            _logsi.LogVerbose("SoundTouch device websocket connection event: %s" % (str(args)), colorValue=SIColors.LightGreen)
            print("\n'%s' websocket connection event:\n%s" % (client.Device.DeviceName, str(args)))


    def OnSoundTouchWebSocketCloseEvent(self, client:SoundTouchClient, statCode=None, args:str=None) -> None:
        if (args != None):
            _logsi.LogVerbose("SoundTouch device websocket closed event: (%s) %s" % (str(statCode), str(args)), colorValue=SIColors.LightGreen)
            print("\n'%s' websocket connection event: (%s) %s" % (client.Device.DeviceName, str(statCode), str(args)))


    def OnSoundTouchWebSocketErrorEvent(self, client:SoundTouchClient, ex:Exception) -> None:
        if (ex != None):
            # args will be an Exception object for websocket errors.
            _logsi.LogError("SoundTouch device websocket error event: %s" % (str(ex)), colorValue=SIColors.LightGreen)
            print("\n'%s' websocket error:\n%s" % (client.Device.DeviceName, str(ex)))


    def OnSoundTouchWebSocketPingPongEvent(self, client:SoundTouchClient, args:str) -> None:
        if (args != None):
            # args will be a connection type: 'WebSocketPing', 'WebSocketPong'.
            _logsi.LogVerbose("SoundTouch device websocket pingpong event: %s" % (str(args)), colorValue=SIColors.LightGreen)
            print("\n'%s' websocket pingpong event:\n%s" % (client.Device.DeviceName, str(args)))


    def OnSoundTouchUpdateEvent(self, client:SoundTouchClient, args:Element) -> None:
        if (args != None):
            if (isinstance(args, Element)):
                ElementTree.indent(args)  # for pretty printing
                argsEncoded = ElementTree.tostring(args, encoding="unicode")
                _logsi.LogXml(SILevel.Message, "SoundTouch device status update: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen, prettyPrint=True)
                print("\n'%s' status update:\n%s" % (client.Device.DeviceName, argsEncoded))
            else:
                _logsi.LogMessage("SoundTouch device status update: '%s'" % (args), colorValue=SIColors.LightGreen)
                print("\n'%s' status update:\n%s" % (client.Device.DeviceName, args))
        

    def OnSoundTouchUpdateEvent_Volume(self, client:SoundTouchClient, args:Element) -> None:
        if (args != None):
            ElementTree.indent(args)  # for pretty printing
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device status update: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen, prettyPrint=True)
            print("\n'%s' status update:\n%s" % (client.Device.DeviceName, argsEncoded))
            
            config:Volume = Volume(root=args[0])
            print(str(config))
            
        
    def OnSoundTouchUpdateEvent_NowPlaying(self, client:SoundTouchClient, args:Element) -> None:
        if (args != None):
            ElementTree.indent(args)  # for pretty printing
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device status update: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen, prettyPrint=True)
            print("\n'%s' status update:\n%s" % (client.Device.DeviceName, argsEncoded))
            
            config:NowPlayingStatus = NowPlayingStatus(root=args[0])
            print(str(config))
            


try:

    print("Test Starting")
    _logsi.LogMessage("Testing Status Notifications", colorValue=SIColors.LightGreen)

    socket:SoundTouchWebSocket = None

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
    #device:SoundTouchDevice = SoundTouchDevice("192.168.1.80") # Bose SoundTouch 300
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)
    
    # activate recent list cache.
    client.UpdateRecentListCacheStatus(True, maxItems=100)

    # get device capabilities - must have IsWebSocketApiProxyCapable=True 
    # in order to support notifications.
    capabilities:Capabilities = client.GetCapabilities()
    if capabilities.IsWebSocketApiProxyCapable:
                
        # create and start a websocket to receive notifications from the device.
        socket = SoundTouchWebSocket(client, pingInterval=10)
        print(socket)
        
        # create event handler class instance.
        ehc:EventHandlerClass = EventHandlerClass()
                
        # add our listener(s) that will handle SoundTouch device status updates.
        socket.AddListener(SoundTouchNotifyCategorys.ALL, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.connectionStateUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.criticalErrorUpdate, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.errorNotification, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.errorUpdate, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.groupUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.languageUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.LowPowerStandbyUpdate, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.nameUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.nowPlayingUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.nowSelectionUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.presetsUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.recentsUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.soundTouchConfigurationUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.sourcesUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.swUpdateStatusUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.volumeUpdated, ehc.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.zoneUpdated, ehc.OnSoundTouchUpdateEvent)
                
        # you can also add methods for individual models, to make handling them easier.
        # add our listener(s) that will handle SoundTouch device status specific updates.
        # socket.AddListener(SoundTouchNotifyCategorys.nowPlayingUpdated, ehc.OnSoundTouchUpdateEvent_NowPlaying)
        socket.AddListener(SoundTouchNotifyCategorys.volumeUpdated, ehc.OnSoundTouchUpdateEvent_Volume)

        # add our listener(s) that will handle SoundTouch device informational events.
        socket.AddListener(SoundTouchNotifyCategorys.SoundTouchSdkInfo, ehc.OnSoundTouchInfoEvent)
        socket.AddListener(SoundTouchNotifyCategorys.userActivityUpdate, ehc.OnSoundTouchInfoEvent)
        
        # add our listener that will handle SoundTouch websocket related events.
        socket.AddListener(SoundTouchNotifyCategorys.WebSocketClose, ehc.OnSoundTouchWebSocketCloseEvent)
        socket.AddListener(SoundTouchNotifyCategorys.WebSocketError, ehc.OnSoundTouchWebSocketErrorEvent)
        socket.AddListener(SoundTouchNotifyCategorys.WebSocketOpen, ehc.OnSoundTouchWebSocketOpenEvent)
        socket.AddListener(SoundTouchNotifyCategorys.WebSocketPong, ehc.OnSoundTouchWebSocketPingPongEvent)

        # start receiving updates.
        socket.StartNotification()

        print("** Notification event loop has started.")
        print("** Try pressing some buttons on your SoundTouch remote or device ...")

        try:
            
            # for testing status notifications.
            maxcnt:int = 1200  # 1200=20 mins, 300=5 mins
            for i in range(maxcnt):
                
                # wait 1 second.
                time.sleep(1)
                
                # if i == 1:
                #     socket.StopNotification()
                #     break

                # if i == 10:
                #     print("Rebooting device ...")
                #     msg = device.RebootDevice()
                #     print("Response:\n%s" % msg)
            
                # did we lose the connection to the SoundTouch device?
                # if so, then stop / restart the notification event thread.
                if socket.IsThreadRunForeverActive == False:
                    print("socket.IsThreadRunForeverActive = %s - restarting notification thread ..." % (str(socket.IsThreadRunForeverActive)))
                    socket.StopNotification()
                    socket.StartNotification()
            
        except Exception as ex:
            
            _logsi.LogException(None, ex)
            print(str(ex))
            
    else:
        
        print("SoundTouch device '%s' does not support Bose WebSocket API.")
        
    print("Tests Completed")

except Exception as ex:

    _logsi.LogException(None, ex)
    print(str(ex))
    raise
        
finally:
            
    # stop listening for Bose SoundTouch status updates.
    if (socket != None):
        socket.StopNotification()
        socket.ClearListeners()

    # unwire events, and dispose of SmartInspect.
    print("** Disposing of SmartInspect resources")
    SIAuto.Si.Dispose()
