## Change Log

All notable changes to this project are listed here.  

Change are listed in reverse chronological order (newest to oldest).  

<span class="changelog">

###### [ 1.0.18 ] - 2023/11/15

  *  Added VS test class `testVS_SoundTouchDiscovery.py` to test Zeroconf discovery scenarios.
  *  Updated VS test class `testVS_SoundTouchClient` with missing testing scenarios.

###### [ 1.0.18 ] - 2023/11/15

  *  Added method to `SoundTouchClient`: AddMusicServiceSources - Adds any servers in the `MediaServerList` to the sources list if they do not exist in the sources list as a "STORED_MUSIC" source.
  *  Added method to `SoundTouchClient`: RemoveMusicServiceAccount - Removes an existing music service account from the sources list.
  *  Added method to `SoundTouchClient`: SetMusicServiceAccount - Adds a music service account to the sources list.
  *  Updated model `PlayInfo`: ToXmlRequestBody method - changed default encoding value from 'unicode' to 'utf-8', which is what the ST webservices API expects.
  *  Updated model `SourceItem`: UserName property - changed to `FriendlyName`, as the value is a display name.
  *  Updated model `MusicServiceAccount`: UserName property - changed to `UserAccount`, as the value is an account name and not a user name.
  *  Updated model `MusicServiceAccount`: DisplayName property - changed to `FriendlyName`, to use the same naming standards for UI display fields.
  *  Updated any classes that did not have a `__str__` or `__repr__` method to call their `ToString` method.

###### [ 1.0.18 ] - 2023/11/15

  *  Updated model `AudioDspControls`.`ToSupportedAudioModesArray` method to return a sorted list of supported audio modes.
  *  Added method `ToMinMaxString` to model `ControlLevelInfo` to retrieve a description of the allowed Min / Max range values.
  *  Added new method to `SoundTouchClient`: PlayNotificationBeep - Plays a quick beep notification sound on devices that support it.
  *  Added new method to `SoundTouchClient`: GetSoftwareUpdateCheckInfo - Gets the latest available software update release version information for the device.
  *  Added new method to `SoundTouchClient`: GetSoftwareUpdateStatus - Gets the status of a SoundTouch software update for the device.
  *  Added new method to `SoundTouchClient`: GetWirelessSiteSurvey - Gets a list of wireless networks that can be detected by the device.
  *  Added new method to `SoundTouchClient`: SelectLastWiFiSource - Selects the last wifi source that was selected.

###### [ 1.0.17 ] - 2023/11/15

  *  Add sort support to model `MediaServerList`, to allow sorting on any column.
  *  Add sort support to model `PresetList`, to allow sorting on any column.
  *  Add sort support to model `RecentList`, to allow sorting on any column.
  *  Add sort support to model `ServiceAvailability`, to allow sorting on any column.
  *  Add sort support to model `SourceList`, to allow sorting on any column.
  *  Updated `SoundTouchClient`: GetMediaServerList method - automatically sorts the returned list objects by FriendlyName.
  *  Updated `SoundTouchClient`: GetServiceAvailability method - automatically sorts the returned list objects by ServiceType.
  *  Updated `SoundTouchClient`: GetSourceList method - automatically sorts the returned list objects by Source.

###### [ 1.0.16 ] - 2023/11/15

  *  Changed Zeroconf dependency, as it was interfering with Home Assistant dependencies.

###### [ 1.0.15 ] - 2023/11/14

  *  Added new class `SoundTouchDiscovery` to support discovery of SoundTouch devices on the network using Zeroconf MDNS.
  *  Added new method to `SoundTouchClient`: GetServiceAvailability - Gets the current service availability configuration of the device.
  *  Added new method to `SoundTouchClient`: GetSoundTouchConfigurationStatus - Gets the current SoundTouch configuration status of the device.

###### [ 1.0.14 ] - 2023/11/13

  *  Added new method to `SoundTouchClient`: GetAudioSpeakerAttributeAndSetting - allows speaker attribute and settings to be retrieved (Rear, SubWoofer01, SubWoofer02).
  *  Added new method to `SoundTouchClient`: GetAudioProductLevelControls - allows speaker levels to be retrieved (FrontCenterSpeakerLevel, RearSurroundSpeakersLevel).
  *  Added new method to `SoundTouchClient`: SetAudioProductLevelControls - allows speaker levels to be adjusted (FrontCenterSpeakerLevel, RearSurroundSpeakersLevel).
  *  Added new method to `SoundTouchClient`: SetAudioDspControls - allows audio dsp controls to be adjusted (AudioMode, VideoSyncAudioDelay, SupportedAudioModes).
  *  Removed method from `SoundTouchClient`: SetAudioDspControlsAudioMode - replaced this with the more robust SetAudioDspControls method.
  *  Added class `SoundTouchHdmiCecModes` to define HDMI CEC Mode values.
  *  Added class `SoundTouchAudioModes` to define Audio Mode values.
  *  Updated documentation for various classes and sample code snippets.

###### [ 1.0.13 ] - 2023/11/12

  *  Added new method to `SoundTouchClient`: SetProductCecHdmiControl - allows HDMI CEC mode to be turned ON/OFF.
  *  Updated documentation for various classes and sample code snippets.

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