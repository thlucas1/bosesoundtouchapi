## Change Log

All notable changes to this project are listed here.  

Change are listed in reverse chronological order (newest to oldest).  

<span class="changelog">

###### [ 1.0.39 ] - 2023/12/22

  * Added method `AudioDspControls`.`ToSupportedAudioModeTitlesArray` - Returns a string array of titles for SupportedAudioModes.
  * Added method `AudioDspAudioModes`.`GetNameByValue` - Returns a name for the given audioMode value; No exception will be thrown by this method if the value is not found.
  * Added method `AudioDspAudioModes`.`GetValueByName` - Returns a value for the given audioMode name; No exception will be thrown by this method if the name is not found.
  
###### [ 1.0.38 ] - 2023/12/21

  * Updated socket close processing in `SoundTouchWebSocket` to include a close status code and message upon socket closure.
  
###### [ 1.0.37 ] - 2023/12/21

  * Added method `SourceList`.`GetTitleBySource` - Returns a `SourceItem`.`SourceTitle` string for the given source and sourceAccount values.
  * Renamed method `SourceList`.`FromSourceTitle` to `GetSourceItemByTitle` - Returns a `SourceItem` instance for the given source title value.
  * Added model `PlayStatusTypes` - play status types enumeration.
  
###### [ 1.0.36 ] - 2023/12/20

  * Added property `SourceItem`.`SourceTitle` - source title of media content (e.g. "Tunein", "Airplay", "NAS Music Server", etc).
  * Added method `SourceList`.`FromSourceTitle` - Returns a `SourceItem` instance for the given source title value.
  * Added method `SourceList`.`ToSourceTitleArray` - Returns an array of source title strings.

###### [ 1.0.35 ] - 2023/12/16

  * Fixed error processing logic for `SoundTouchClient`.  Prior to this fix, some error conditions were not being caught.

###### [ 1.0.34 ] - 2023/12/16

  * Fixed logging of eventhandler exceptions in `SoundTouchWebSocket`.  Prior to this fix, exceptions were being ignored.

###### [ 1.0.33 ] - 2023/12/16

  * Added logging of eventhandler exceptions in `SoundTouchWebSocket`.  Prior to this fix, exceptions were being ignored.
  * Added property `PresetList`.`LastUpdatedOn` - indicates when the list was last updated.
  * Added property `RecentList`.`LastUpdatedOn` - indicates when the list was last updated.

###### [ 1.0.32 ] - 2023/12/15

  * Added `Information` and `SupportedURLs` objects to `SoundTouchClient`.`ConfigurationCache` upon class initialization.  These are used by the `SoundTouchDevice` class.
  * Added properties to `SoundTouchDevice` class - `UnknownUrlNames`, `UnSupportedUrlNames`.

###### [ 1.0.31 ] - 2023/12/15

  * Added method `SoundTouchClient`.`GetInformation` - Gets the information configuration of the device.
  * Added method `SoundTouchClient`.`GetIntrospectData` - Gets introspect data for a specified source.
  * Added model `Component` - component configuration.
  * Added model `Information` - info configuration.
  * Added model `InformationNetworkInfo` - info network information configuration.
  * Added model `Introspect` - introspect configuration.
  * Added model `SupportedUrl` - supported url configuration.
  * Added model `SupportedUrls` - supported urls configuration.
  * Removed `SoundTouchDeviceComponent` class, as it was replaced by the `Component` model.
  * Removed `InfoNetworkConfig` model, as it was replaced by the `InformationNetworkInfo` model.

###### [ 1.0.30 ] - 2023/12/13

  * Updated method `SoundTouchWebSocket`.`_OnWebSocketClose` - Close event handler was missing 2 arguments that are passed for the event.

###### [ 1.0.29 ] - 2023/12/13

  * Added method `SoundTouchDevice`.`RebootDevice` - Reboots the operating system of the SoundTouch device.
  * Removed method `SoundTouchClient`.`Bookmark` - No longer necessary, as Pandora removed bookmark functionality; per Pandora, use thumbs up / down instead.
  * Added method `SoundTouchClient`.`SetUserPlayControl` - Sends a user play control type command to stop / pause / play / resume media content playback.
  * Added method `SoundTouchClient`.`SetUserRating` - Rates the currently playing media, if ratings are supported.
  * Added method `SoundTouchClient`.`SetUserTrackControl` - Sends a user track control type command to control track playback (next, previous, repeat, shuffle, etc).
  * Added model `UserPlayControl` - user play control configuration.
  * Added model `UserPlayControlTypes` - user play control types enumeration.
  * Added model `UserRating` - user rating configuration.
  * Added model `UserRatingTypes` - user rating types enumeration.
  * Added model `UserTrackControl` - user track control configuration.
  * Added model `UserTrackControlTypes` - user track control types enumeration.

###### [ 1.0.28 ] - 2023/12/13

  * Added method `SoundTouchClient`.`RemoveGroupStereoPair` - Removes an existing left / right stereo pair speaker group configuration from the device.
  * Removed the `SoundTouchException` class, as it was not used; SoundTouchError class is used instead.
  * cleaned up some unused references.

###### [ 1.0.27 ] - 2023/12/12

  * Updated code to include pretty print of raw xml responses for easier debugging.

###### [ 1.0.26 ] - 2023/12/12

  * Added method `SoundTouchClient`.`CreateGroupStereoPair` - Creates a new left / right stereo pair speaker group configuration for the device.
  * Added method `SoundTouchClient`.`GetGroupStereoPairStatus` - Gets the current left / right stereo pair speaker group configuration of the device.
  * Added method `SoundTouchClient`.`SetBalanceLevel` - Sets the device balance level to the given level.
  * Added method `SoundTouchClient`.`UpdateGroupStereoPairName` - Updates the name of the current left / right stereo pair speaker group configuration for the device.
  * Added model `Group` - group (stereo pair) configuration.
  * Added model `GroupRole` - group (stereo pair) role configuration.
  * Added model `GroupRoleTypes` - group (stereo pair) role types enumeration.
  * Added model `GroupStatusTypes` - group (stereo pair) status types enumeration.
  * Updated property descriptions for various classes.

###### [ 1.0.25 ] - 2023/12/10

  * Added model `KeyStates` - key states enumeration.
  * Updated methods in `SoundTouchClient` class that send remote keypress commands, based upon 2019 SoundTouch API reference specifications.  For example, the client used to send both press and release keys when a preset was selected; this was actually issuing a set preset command (via key press) and then selecting the preset (via key release).

###### [ 1.0.24 ] - 2023/12/10

  * Added method `SoundTouchClient`.`SearchMusicLibrary` - Searches a specified music library container (e.g. STORED_MUSIC, etc).
  * Added model `AudioDspAudioModes` - media product cec hdmi modes enumeration.
  * Added model `KeyStates` - key states enumeration.
  * Added model `ProductCecHdmiModes` - media product cec hdmi modes enumeration.
  * Removed class `SoundTouchAudioModes` - replaced with AudioDspAudioModes model.
  * Removed class `SoundTouchHdmiCecModes` - replaced with NavigateMenuTypes model.
  * Updated methods in `SoundTouchClient` class that send remote keypress commands, based upon 2019 SoundTouch API reference specifications.  For example, the client used to send both press and release keys when a preset was selected; this was actually issuing a set preset command (via key press) and then selecting the preset (via key release).

###### [ 1.0.23 ] - 2023/12/09

  * Added method `SoundTouchClient`.`GetMusicLibraryItems` - Gets a list of music library data from the specified music library (e.g. STORED_MUSIC, etc).
  * Added method `SoundTouchClient`.`PowerStandbyLowPower` - Sets power to low-power standby, if the device is currently powered on.
  * Added model `MediaItemContainer` - media item container configuration.
  * Added model `NavigateMenuTypes` - navigate menu types enumeration.
  * Added model `NavigateSortTypes` - navigate sort types enumeration.
  * Added model `Search` - search configuration.
  * Added model `SearchFilterTypes` - search filter types enumeration.
  * Added model `SearchResponse` - search response configuration.
  * Added model `SearchSortTypes` - search sort types enumeration.
  * Added model `SearchTerm` - search terms configuration.
  * Removed class `SoundTouchMenuTypes` - replaced with NavigateMenuTypes model.
  * Removed class `SoundTouchSortOrders` - replaced with SearchSortTypes model.
  * Changed all sort references to account for lower-case values, so they are properly sorted.  Prior behavior was placing lower-case results after all upper-case results.
  * Removed quite a few unused import references (too many to list).

###### [ 1.0.22 ] - 2023/12/04

  * Updated rebuilt documentation index.

###### [ 1.0.21 ] - 2023/12/04

  * Added method `SoundTouchClient`.`GetMusicServiceStations` - Gets a list of your stored stations from the specified music service (e.g. PANDORA, etc).  This has only been tested with Pandora at this point, so not sure if it will work for Spotify, Amazon Music, etc.
  * Added method `SoundTouchClient`.`AddMusicServiceStation` - Adds a station to a music service (e.g. PANDORA, etc) collection of previously stored stations.  This has only been tested with Pandora at this point, so not sure if it will work for Spotify, Amazon Music, etc.
  * Added method `SoundTouchClient`.`RemoveMusicServiceStation` - Removes a station from a music service (e.g. PANDORA, etc) collection of previously stored stations.  This has only been tested with Pandora at this point, so not sure if it will work for Spotify, Amazon Music, etc.
  * Added method `SoundTouchClient`.`SearchMusicServiceStations` - Searches a music service (e.g. PANDORA, etc) for stations that can be added to a users collection of stations.  This has only been tested with Pandora at this point, so not sure if it will work for Spotify, Amazon Music, etc.
  * Added method `SoundTouchClient`.`GetTrackInfo` - Gets extended track information for the current playing music service media.
  * Added method `SoundTouchClient`.`Bookmark` - Bookmarks the current playing music service media.
  * Updated method `SoundTouchClient`.`RemoveAllPresets` to return a PresetList object that contains the updated list of presets.
  * Updated method `SoundTouchClient`.`RemovePreset` to return a PresetList object that contains the updated list of presets.
  * Updated method `SoundTouchClient`.`StorePreset` to return a PresetList object that contains the updated list of presets.
  * Added model `AddStation` - addStation configuration.
  * Added model `Navigate` - navigate configuration.
  * Added model `NavigateItem` - navigate item configuration.
  * Added model `NavigateResponse` - navigate response configuration.
  * Added model `SearchResult` - searchResult configuration.
  * Added model `RemoveStation` - removeStation configuration.
  * Added model `TrackInfo` - trackInfo configuration.
  * Added class `SoundTouchMenuTypes` - menu types enumeration.
  * Added class `SoundTouchSortOrders` - sort orders enumeration.
  * Updated model `ContentItem` - added new properties: IsNavigate, Offset.
  * Updated model `NowPlayingStatus` - added new properties: ArtistId, ArtImageStatus, DeviceId, IsAdvertisement, IsRatingEnabled, Rating, SessionId, SourceAccount, TrackId.
  * Updated model `NowPlayingStatus` - changed `Image` property name to `ArtUrl` to more closely match the SoundTouch API schema.

###### [ 1.0.20 ] - 2023/11/29

  *  SmartInspect SIConfigurationTimer changes to remove interval value.

###### [ 1.0.20 ] - 2023/11/25

  *  Added method to `SoundTouchClient`: `ClearBluetoothPaired` - Clears all bluetooth pairings from the device.
  *  Added method to `SoundTouchClient`: `EnterBluetoothPairing` - Enters bluetooth pairing mode, and waits for a compatible device to pair with.

###### [ 1.0.19 ] - 2023/11/21 

  *  Added VS test class `testVS_SoundTouchDiscovery.py` to test Zeroconf discovery scenarios.
  *  Updated VS test class `testVS_SoundTouchClient` with missing testing scenarios.

###### [ 1.0.19 ] - 2023/11/21

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