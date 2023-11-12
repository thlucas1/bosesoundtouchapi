## Change Log

All notable changes to this project are listed here.  

Change are listed in reverse chronological order (newest to oldest).  

<span class="changelog">

###### [ 1.0.12 ] - 2023/11/11

  *  Added new methods to `SoundTouchClient`: GetAudioProductToneControls, SetAudioProductToneControls.
  *  Updated `SoundTouchClient` methods GetAudioDspControls, GetBlueToothInfo, GetProductCecHdmiControl, GetProductHdmiAssignmentControls, GetRebroadcastLatencyMode, and SetAudioDspControlAudioMode to check device capabilities prior to executing the request.  A `SoundTouchError` will be thrown if the device does not support the capability.

###### [ 1.0.11 ] - 2023/11/11

  *  Added several new methods to SoundTouchClient: GetAudioDspControls, GetBlueToothInfo, GetProductCecHdmiControl, GetProductHdmiAssignmentControls, GetRebroadcastLatencyMode, SetAudioDspControlAudioMode.

###### [ 1.0.10 ] - 2023/11/10

  *  Added several new methods to SoundTouchClient: SelectLastSoundTouchSource(), SelectLastSource(), SelectLocalSource().

###### [ 1.0.9 ] - 2023/11/08

  *  Accidentally changed the GetrSourceList() method to GetCapabilities() method while testing and pushed the change to PyPi.org.  Changed it back, but hda to update the release to 1.0.9.

###### [ 1.0.8 ] - 2023/11/08

  *  Added SoundTouchWebSocket.ClearListeners() method to allow all listeners to be removed with one call.
  *  Changed classifier to "Development Status 5 - Production/Stable".

###### [ 1.0.7 ] - 2023/11/08

  *  Added SourceList.ToSourceArray() method that returns an array of available source list items.

###### [ 1.0.6 ] - 2023/11/04

  *  Added Ping and Pong functionality to the SoundTouchWebSocket class.  This allows 'keep-alive' ping send requests and pong responses to be tracked by the websocket.  PingInterval is also configurable, and can also be disabled (default setting) if configured to do so.

###### [ 1.0.5 ] - 2023/11/03

  *  Updated Firmware namespace classes to more closely resemble the index.xml output (e.g. changed property names, fixed PROTOCOL processing, etc).  Also added sample code to the SoundTouchFirmware class.

###### [ 1.0.4 ] - 2023/11/01

  *  Updated SoundTouchWebSocket OnClose event processing to only pass 2 parameters instead of 3.  There is no message argument when a connection is closed.  I also added an OnOpen event to allow the user to listen for when a connection is opened.

###### [ 1.0.3 ] - 2023/10/30

  *  Updated SoundTouchClient `PlayUrl` method to handle metadata retrieval errors more gracefully.

###### [ 1.0.2 ] - 2023/10/28

  *  Updated documentation link for PyPi.org.

###### [ 1.0.1 ] - 2023/10/28

  *  Added support for ReadtheDocs documentation hosting.

###### [ 1.0.0 ] - 2023/10/05

  *  Version 1 initial release.

</span>