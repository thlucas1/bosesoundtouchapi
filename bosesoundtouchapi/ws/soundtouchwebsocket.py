# external package imports.
from threading import Thread
from websocket import WebSocketApp
from xml.etree import ElementTree as xmltree

# our package imports.
from bosesoundtouchapi.bstutils import export
from bosesoundtouchapi.soundtouchclient import SoundTouchClient
from bosesoundtouchapi.soundtouchnotifycategorys import SoundTouchNotifyCategorys


# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SILevel, SISession
_logsi:SISession = SIAuto.Si.GetSession(__name__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__name__, True)
_logsi.SystemLogger = logging.getLogger(__name__)


class _SoundTouchWebSocketThread(Thread):
    """
    A small utility class wrapping the WebSocketApp::run_forever() method in an
    extra Thread.
    """

    def __init__(self, ws:WebSocketApp, pingInterval:int, pingTimeout:int) -> None:
        """
        Args:
            ws (WebSocketApp):
                A websocket client, that receives notifications from the SoundTouch device.
            pingInterval (int):
                Interval (in seconds) to send 'KeepAlive' ping request to the SoundTouch 
                WebSocket, if websocket support is enabled for the SoundTouch device.  Set
                this value to zero to disable keepalive ping requests.  
            pingTimeout (int):
                Interval (in seconds) to wait for the ping response from the SoundTouch 
                WebSocket, if websocket support is enabled for the SoundTouch device.
        """
        super().__init__()
        self._IsRunForeverActive:bool = False
        self._PingInterval:int = pingInterval
        self._PingTimeout:int = pingTimeout
        self._wsocket = ws


    @property
    def IsRunForeverActive(self) -> bool:
        """ 
        True if the websocket run_forever loop is still executing; otherwise, False.
        
        A value of False can indicate that an exception has occured that caused the run_forever()
        loop to exit.
        """
        return self._IsRunForeverActive


    def run(self) -> None:
        """
        Starts the event loop for WebSocket framework.  
        """
        self._IsRunForeverActive = True
        
        self._wsocket.run_forever(ping_interval=self._PingInterval, 
                                  ping_timeout=self._PingTimeout, 
                                  ping_payload='KeepAlive')
        
        self._IsRunForeverActive = False
        
#ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_interval=10, ping_timeout=5)


@export
class SoundTouchWebSocket:
    """
    A wrapper class to use the notification system provided by SoundTouch devices.

    In order to react to a message, there is a listener system. You can add
    functions as listener objects. The connection url is defined as follows:
    'ws://{Host}:{Port}/'.  Port 8080 is used by default.

    This class can be used in two ways. First, the object can open a
    connection through the `StartNotification` method and secondly, the with-statement
    can be used to create an instance.
    
    You must first check the device capabilities prior to using the support notifications
    functionality; if the device does not support it, then it's not going to work!
    To do this, fetch the device's capabilities and check for a `IsWebSocketApiProxyCapable = True`
    value.  If true, then the device supports sending notifications; if false, it does not.
    
    For more information and code samples refer to `bosesoundtouchapi.soundtouchclient.GetCapabilities`
    method.

    <details>
        <summary>Sample Code</summary>
    ```python
    .. include:: ../../docs/include/samplecode/SoundTouchWebSocket/_ClassInit.py
    ```
    </details>
    """
    
    _PING_TIMEOUT:int = 10
    """
    Time (in seconds) to wait for a ping request response from the SoundTouch device
    websocket server.
    """

    def __init__(self, client:SoundTouchClient, port:int=8080, pingInterval:int=0) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            client (SoundTouchClient):
                A `SoundTouchClient` instance to receive status notifications from.
            port (int):
                The port that the SoundTouch WebAPI socket is posting notifications on.  
                Default is 8080.
            pingInterval (int):
                Interval (in seconds) to send 'KeepAlive' ping request to the SoundTouch 
                WebSocket, if websocket support is enabled for the SoundTouch device.  Set
                this value to zero to disable keepalive ping requests.  
                Default is 0 (disabled).
        """
        # validations.
        if (port is None) or (not isinstance(port, int)):
            port = 8080
            
        if (pingInterval is None) or (not isinstance(pingInterval, int)):
            pingInterval = 60
        if (pingInterval > 0) and (pingInterval <= SoundTouchWebSocket._PING_TIMEOUT):
            pingInterval = 60

        # initialize internal storage.
        self._CachedListeners:dict = {}
        self._Client:SoundTouchClient = client
        self._PingInterval:int = int(pingInterval)
        self._Port:int = int(port)
        self._Thread = None
        self._WebsocketClient:WebSocketApp = None
        

    def __enter__(self) -> 'SoundTouchWebSocket':
        # if called via a context manager (e.g. "with" statement).
        self.StartNotification()
        return self


    def __exit__(self, etype, value, traceback) -> None:
        # if called via a context manager (e.g. "with" statement).
        self.StopNotification()
        self.ClearListeners()


    @property
    def Client(self) -> SoundTouchClient:
        """ 
        A `SoundTouchClient` instance to receive status notifications from.
        """
        return self._Client


    @property
    def IsThreadRunForeverActive(self) -> bool:
        """ 
        True if the websocket run_forever() loop is still executing; otherwise, False.
        
        A value of False can indicate that an exception has occured that caused the run_forever()
        loop to exit.
        """
        result:bool = False
        if self._Thread is not None:
            result = self._Thread.IsRunForeverActive
        return result


    @property
    def PingInterval(self) -> int:
        """ 
        Interval (in seconds) to send 'KeepAlive' ping request to the SoundTouch 
        WebSocket, if websocket support is enabled for the SoundTouch device.  
        
        Default is 60.  
        If zero, then keepalive requests are disabled.  
        """
        return self._PingInterval


    @property
    def Port(self) -> int:
        """ 
        The port that the SoundTouch WebAPI socket is posting notifications on.  

        Default is 8080.
        """
        return self._Port


    def _OnWebSocketClose(self, wsApp:WebSocketApp, closeCode, closeMessage:bytes) -> None:
        """
        Event raised by the web socket event listener when a socket has been closed.
        
        Args:
            wsApp (WebSocketApp):
                Event sender.
            closeCode:
                Close status code.
            closeMessage (bytes):
                Close message.
        """
        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogObject(SILevel.Verbose, "SoundTouch web socket event listener OnClose event: '%s' - (%s) %s" % (SoundTouchNotifyCategorys.WebSocketClose.value, str(closeCode), str(closeMessage)), closeMessage)
            
        # notify listeners.
        self.NotifyListeners(SoundTouchNotifyCategorys.WebSocketClose.value, SoundTouchNotifyCategorys.WebSocketClose.value)


    def _OnWebSocketError(self, wsApp:WebSocketApp, error:bytes) -> None:
        """
        Event raised by the web socket event listener when a socket error has occurred.
        
        Args:
            wsApp (WebSocketApp):
                Event sender.
            error (bytes):
                Event argument, in the form of socket error details.
        """
        # ignore pesky lambda function errors.
        # not sure why these happen, but the following code suppresses the error messaage.
        if isinstance(error, TypeError) and str(error).find("<lambda>() takes") != -1:
            return
        
        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogObject(SILevel.Verbose, "SoundTouch web socket event listener OnError event: '%s' - (%s) %s" % (SoundTouchNotifyCategorys.WebSocketError.value, str(type(error)), str(error)), error)
           
        # notify listeners.
        self.NotifyListeners(SoundTouchNotifyCategorys.WebSocketError.value, error)
            

    def _OnMessage(self, wsApp:WebSocketApp, message:bytes) -> None:
        """
        Event raised by the web socket event listener when a message is received from
        the monitored SoundTouch device.
        
        Args:
            wsApp (WebSocketApp):
                Event sender.
            message (bytes):
                Event argument, in the form of an xml-formatted message.
        """
        root = xmltree.fromstring(message)
        
        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogXml(SILevel.Verbose, "SoundTouch web socket event listener OnMessage event: '%s' - %s" % (root.tag, message), message, prettyPrint=True)

        # the SoundTouch device can send different types of notifications, which
        # need to be processed differently.
        # Examples: "userActivityUpdate", "updates", etc.

        # is this an "updates" message?
        if root.tag == 'updates':
            
            # "updates" messages will consist of child nodes that denote the type of update; like so:
            # <updates deviceID="9070658C9D4A">
            #   <connectionStateUpdated state="NETWORK_WIFI_CONNECTED" up="true" signal="GOOD_SIGNAL" />
            # </updates>

            # process all update child nodes (there could be multiple).
            for update in root:
                if (update.tag):
                    self.NotifyListeners(update.tag, update)

        else:

            # for all other messages, we will just process the root node; like so:
            # <SoundTouchSdkInfo serverVersion="4" serverBuild="trunk r46330 v4 epdbuild hepdswbld04" />
            # <userActivityUpdate deviceID="9070658C9D4A" />

            # process the root node (there is only one).
            self.NotifyListeners(root.tag, root)


    def _OnWebSocketOpen(self, wsApp:WebSocketApp) -> None:
        """
        Event raised by the web socket event listener when a socket has been opened.
        
        Args:
            wsApp (WebSocketApp):
                Event sender.
                
        Note that there is no message argument with this call.
        """
        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogVerbose("SoundTouch web socket event listener OnOpen event: '%s'" % (SoundTouchNotifyCategorys.WebSocketOpen.value))
            
        # notify listeners.
        self.NotifyListeners(SoundTouchNotifyCategorys.WebSocketOpen.value, SoundTouchNotifyCategorys.WebSocketOpen.value)


    def _OnWebSocketPing(self, wsApp:WebSocketApp, args:object) -> None:
        """
        Event raised by the web socket event listener when a server has sent a ping request.
        
        Args:
            wsApp (WebSocketApp):
                Event sender.
        """
        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogBinary(SILevel.Verbose, "SoundTouch web socket event listener OnPing event: '%s'" % (SoundTouchNotifyCategorys.WebSocketPing.value), args)
            
        # notify listeners.
        self.NotifyListeners(SoundTouchNotifyCategorys.WebSocketPing.value, SoundTouchNotifyCategorys.WebSocketPing.value)


    def _OnWebSocketPong(self, wsApp:WebSocketApp, args:object) -> None:
        """
        Event raised by the web socket event listener when a server has sent a ping response (e.g. pong).
        
        Args:
            wsApp (WebSocketApp):
                Event sender.
        """
        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogBinary(SILevel.Verbose, "SoundTouch web socket event listener OnPong event: '%s'" % (SoundTouchNotifyCategorys.WebSocketPong.value), args)
            
        # notify listeners.
        self.NotifyListeners(SoundTouchNotifyCategorys.WebSocketPong.value, SoundTouchNotifyCategorys.WebSocketPong.value)


    def AddListener(self, category:SoundTouchNotifyCategorys, listener) -> bool:
        """
        Adds a listener provided here to the given category.

        Since there are different types of events, the category-string can be used
        to add a listener to a specific notification category. The listener must take
        only two arguments: the `SoundTouchClient` instance, and an xml.etree.ElementTree.Element
        that contains the status update itself.

        Args:
            category (SoundTouchNotifyCategorys):
                The category this listener should be added to.  
                Use one of the pre-defined `SoundTouchNotifyCategorys` values to receive 
                updates for that category (e.g. "volumeUpdated", "nowPlayingUpdated", etc).  
                Use `SoundTouchNotifyCategorys.WebSocketError` to receive notifications for WebSocket errors.  
                Use `SoundTouchNotifyCategorys.ALL` to receive notifications for any type of update event.
            listener (object):
                A simple listener method which takes the XML-Element as a passed argument.
        
        Returns:
            True if the listener was added successfully; otherwise, False.
            
        Please refer to the `bosesoundtouchapi.soundtouchnotifycategorys.SoundTouchNotifyCategorys`
        class for more details on what events are raised and why / when they happen.
        """
        if (not category) or (not listener):
            return False
        
        # convert category argument to string.
        category = SoundTouchNotifyCategorys.toString(category)

        # add the listener to the category list of listeners.
        if category in self._CachedListeners:
            self._CachedListeners[category].append(listener)
        else:
            self._CachedListeners[category] = [listener]
        return True


    def ClearListeners(self) -> None:
        """
        Removes all listeners that were previously added.
        """
        # remove all listeners.
        if self._CachedListeners is not None:
            self._CachedListeners.clear()


    def GetListenerGroup(self, category:str) -> list: # list[function]
        """
        Searches for a specific category in the registered ones.

        This method is a convenient method to return all listeners that were added
        to a specific context.

        Args:
            category (str):
                The category, which has to be one of the `SoundTouchNotifyCategorys` values.
                    
        Returns:
            A list containing all listeners linked to the given category.
        """
        if not category:
            return []
        return self._CachedListeners[category]


    def NotifyListeners(self, category:str, event:xmltree.Element) -> None:
        """
        Notifies all listeners that were stored in the given context.

        The name of each context is defined to be the tag element of the update
        XML-Element.

        Args:
            category (str):
                The category of which listeners should be notified from.
            event (xmltree.Element):
                The event represents either an XML-Element with event.tag == category,
                or an Exception type if category = `SoundTouchNotifyCategorys.WebSocketError`.
        """
        category = str(category)

        # are listeners defined for ANY category?  if so, then notify them.
        if ('*' in self._CachedListeners):
            for listener in self.GetListenerGroup('*'):
                if (event != None) and (isinstance(event, xmltree.Element)):
                    eventEncoded = xmltree.tostring(event, encoding="unicode")
                    _logsi.LogXml(SILevel.Verbose, "SoundTouch device status update NOTIFY (*): '%s'" % (category), eventEncoded, prettyPrint=True)
                try:
                    listener(self._Client, event)
                except Exception as ex: 
                    pass  # ignore exceptions.
            return
            
        # are listeners defined for the specified category?  if so, then notify them.
        if (category in self._CachedListeners):
            for listener in self.GetListenerGroup(category):
                if (event != None) and (isinstance(event, xmltree.Element)):
                    eventEncoded = xmltree.tostring(event, encoding="unicode")
                    _logsi.LogXml(SILevel.Verbose, "SoundTouch device status update NOTIFY: '%s'" % (category), eventEncoded, prettyPrint=True)
                try:
                    listener(self._Client, event)
                except Exception as ex: 
                    pass  # ignore exceptions.
            return
        

    def RemoveListener(self, category:SoundTouchNotifyCategorys, listener) -> bool:
        """
        Removes a listener from the given category.

        Args:
            category (str):
                The category this listener should be removed from.  
                Use one of the pre-defined SoundTouchNotifyCategorys values to receive 
                updates for that category (e.g. "volumeUpdated", "nowPlayingUpdated", etc).
            listener (object):
                A simple listener method which takes the XML-Element as a passed argument.
        
        Returns:
            True if the listener was removed successfully; otherwise, False.
        """
        if not category or not listener: 
            return False
        
        # convert category argument to string.
        category = SoundTouchNotifyCategorys.toString(category)

        # remove the listener from the category list of listeners.
        if category not in self._CachedListeners: 
            listeners: list = self._CachedListeners[category]
            for ls in listeners:
                if ls == listener:
                    listeners.remove(ls)
                    return True
        return False


    def StartNotification(self) -> None:
        """
        Creates and starts a web socket event loop thread that listens for notifications 
        from the SoundTouch device.
        
        Only one web socket event loop thread will be started for the device.
        """
        if self._WebsocketClient is None:

            wsUrl = 'ws://%s:%d/' % (self._Client.Device.Host, self._Port)
            _logsi.LogVerbose("Creating SoundTouch web socket client (%s): pingInterval=%s, pingTimeout=%s." % (wsUrl, self._PingInterval, SoundTouchWebSocket._PING_TIMEOUT))
            
            self._WebsocketClient = WebSocketApp(
                    wsUrl,
                    on_message = lambda ws,msg:             self._OnMessage(ws,msg),
                    on_error   = lambda ws,msg:             self._OnWebSocketError(ws,msg),
                    on_close   = lambda ws,clscod,clsmsg:   self._OnWebSocketClose(ws,clscod,clsmsg),
                    on_open    = lambda ws:                 self._OnWebSocketOpen(ws),
                    on_ping    = lambda ws,args:            self._OnWebSocketPing(ws,args),
                    on_pong    = lambda ws,args:            self._OnWebSocketPong(ws,args),
                    subprotocols=['gabbo']
            )
            
            # start the run_forever loop to receive notifications.
            _logsi.LogVerbose("Starting SoundTouch web socket event listener thread")
            self._Thread = _SoundTouchWebSocketThread(self._WebsocketClient, self._PingInterval, SoundTouchWebSocket._PING_TIMEOUT)
            self._Thread.name = 'SoundTouchWSNotifyThread'
            self._Thread.start()


    def StopNotification(self) -> None:
        """
        Stops the web socket event loop thread, if one was previously started using 
        the `StartNotification` method.
        
        This method does nothing if the event loop thread was not started.
        """
        if self._WebsocketClient != None:
            _logsi.LogVerbose("Stopping SoundTouch web socket event listener thread")
            self._WebsocketClient.close()
            self._WebsocketClient = None
