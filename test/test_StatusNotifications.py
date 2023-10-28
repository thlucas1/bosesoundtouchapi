# external package imports.
from smartinspectpython.siauto import *
from smartinspectpython.sisourceid import *
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
siConfig:SIConfigurationTimer = SIConfigurationTimer(SIAuto.Si, siConfigPath, 60)

# get smartinspect logger reference and log basic system / domain details.
_logsi:SISession = SIAuto.Main            
_logsi.LogSeparator(SILevel.Fatal)
_logsi.LogAppDomain(SILevel.Message)
_logsi.LogSystem(SILevel.Message)

class EventHandlerClass:

    def OnSoundTouchInfoEvent(client:SoundTouchClient, args:Element) -> None:
        if (args != None):
            ElementTree.indent(args)  # for pretty printing
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device information event: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen)
            print("\n'%s' status update:\n%s" % (client.Device.DeviceName, argsEncoded))


    def OnSoundTouchWebSocketCloseEvent(client:SoundTouchClient, ex:Exception) -> None:
        if (ex != None):
            # args will be an Exception object for websocket close.
            _logsi.LogError("SoundTouch device websocket close event: %s" % (str(ex)), colorValue=SIColors.LightGreen)
            print("\n'%s' websocket close:\n%s" % (client.Device.DeviceName, str(ex)))


    def OnSoundTouchWebSocketErrorEvent(client:SoundTouchClient, ex:Exception) -> None:
        if (ex != None):
            # args will be an Exception object for websocket errors.
            _logsi.LogError("SoundTouch device websocket error event: %s" % (str(ex)), colorValue=SIColors.LightGreen)
            print("\n'%s' websocket error:\n%s" % (client.Device.DeviceName, str(ex)))


    def OnSoundTouchUpdateEvent(client:SoundTouchClient, args:Element) -> None:
        if (args != None):
            ElementTree.indent(args)  # for pretty printing
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device status update: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen)
            print("\n'%s' status update:\n%s" % (client.Device.DeviceName, argsEncoded))
        

    def OnSoundTouchUpdateEvent_Volume(client:SoundTouchClient, args:Element) -> None:
        if (args != None):
            ElementTree.indent(args)  # for pretty printing
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device status update: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen)
            print("\n'%s' status update:\n%s" % (client.Device.DeviceName, argsEncoded))
            
            config:Volume = Volume(root=args[0])
            print(str(config))
            
        
    def OnSoundTouchUpdateEvent_NowPlaying(client:SoundTouchClient, args:Element) -> None:
        if (args != None):
            ElementTree.indent(args)  # for pretty printing
            argsEncoded = ElementTree.tostring(args, encoding="unicode")
            _logsi.LogXml(SILevel.Message, "SoundTouch device status update: '%s'" % (args.tag), argsEncoded, SIColors.LightGreen)
            print("\n'%s' status update:\n%s" % (client.Device.DeviceName, argsEncoded))
            
            config:NowPlayingStatus = NowPlayingStatus(root=args[0])
            print(str(config))
            


try:

    print("Test Starting")
    _logsi.LogMessage("Testing Status Notifications", colorValue=SIColors.LightGreen)

    socket:SoundTouchWebSocket = None

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
    #device:SoundTouchDevice = SoundTouchDevice("192.168.1.130") # Bose SoundTouch 300
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get device capabilities - must have IsWebSocketApiProxyCapable=True 
    # in order to support notifications.
    capabilities:Capabilities = client.GetCapabilities()
    if capabilities.IsWebSocketApiProxyCapable:
                
        # create and start a websocket to receive notifications from the device.
        socket = SoundTouchWebSocket(client)
                
        # add our listener(s) that will handle SoundTouch device status updates.
        #socket.AddListener(SoundTouchNotifyCategorys.ALL, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.connectionStateUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.criticalErrorUpdate, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.errorNotification, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.errorUpdate, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.groupUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.languageUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.LowPowerStandbyUpdate, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.nameUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.nowPlayingUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.nowSelectionUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.presetsUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.recentsUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.soundTouchConfigurationUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.sourcesUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.swUpdateStatusUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.volumeUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
        # socket.AddListener(SoundTouchNotifyCategorys.zoneUpdated, EventHandlerClass.OnSoundTouchUpdateEvent)
                
        # you can also add methods for individual models, to make handling them easier.
        # add our listener(s) that will handle SoundTouch device status specific updates.
        # socket.AddListener(SoundTouchNotifyCategorys.nowPlayingUpdated, EventHandlerClass.OnSoundTouchUpdateEvent_NowPlaying)
        socket.AddListener(SoundTouchNotifyCategorys.volumeUpdated, EventHandlerClass.OnSoundTouchUpdateEvent_Volume)

        # add our listener(s) that will handle SoundTouch device informational events.
        socket.AddListener(SoundTouchNotifyCategorys.SoundTouchSdkInfo, EventHandlerClass.OnSoundTouchInfoEvent)
        socket.AddListener(SoundTouchNotifyCategorys.userActivityUpdate, EventHandlerClass.OnSoundTouchInfoEvent)
        
        # add our listener that will handle SoundTouch websocket related events.
        socket.AddListener(SoundTouchNotifyCategorys.WebSocketClose, EventHandlerClass.OnSoundTouchWebSocketCloseEvent)
        socket.AddListener(SoundTouchNotifyCategorys.WebSocketError, EventHandlerClass.OnSoundTouchWebSocketErrorEvent)

        # start receiving updates.
        socket.StartNotification()

        print("** Notification event loop has started.")
        print("** Try pressing some buttons on your SoundTouch remote or device ...")

        # for testing status notifications.
        maxcnt:int = 1200  # 1200=20 mins, 300=5 mins
        for i in range(maxcnt):
                
            # wait 1 second.
            time.sleep(1)
            
            # did we lose the connection to the SoundTouch device?
            # if so, then stop / restart the notification event thread.
            if socket.IsThreadRunForeverActive == False:
                print("socket.IsThreadRunForeverActive = %s - restarting notification thread ..." % (str(socket.IsThreadRunForeverActive)))
                socket.StopNotification()
                socket.StartNotification()
            
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

    # unwire events, and dispose of SmartInspect.
    print("** Disposing of SmartInspect resources")
    SIAuto.Si.Dispose()
