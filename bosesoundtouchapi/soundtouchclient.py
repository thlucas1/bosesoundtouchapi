# external package imports.
from datetime import datetime
from functools import reduce
from io import BytesIO
import re
import time
from tinytag import TinyTag
import urllib.parse
from urllib3 import PoolManager, Timeout
from xml.etree.ElementTree import fromstring, tostring, Element
from xml.etree import ElementTree

# our package imports.
from .bstappmessages import BSTAppMessages
from .bstutils import export
from .models import *
from .soundtouchdevice import SoundTouchDevice
from .soundtoucherror import SoundTouchError
from .soundtouchkeys import SoundTouchKeys
from .soundtouchmessage import SoundTouchMessage
from .soundtouchmodelrequest import SoundTouchModelRequest
from .soundtouchsources import SoundTouchSources
from .uri import *

from .bstconst import (
    MSG_TRACE_ACTION_KEY,
    MSG_TRACE_DELAY_DEVICE,
    MSG_TRACE_DEVICE_COMMAND,
    MSG_TRACE_DEVICE_COMMAND_WITH_PARM,
    MSG_TRACE_FAVORITE_NOT_ENABLED,
    MSG_TRACE_GET_CONFIG_OBJECT,
    MSG_TRACE_RATING_NOT_ENABLED,
    MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE
)

# get smartinspect logger reference; create a new session for this module name.
from smartinspectpython.siauto import SIAuto, SILevel, SISession
import logging
_logsi:SISession = SIAuto.Si.GetSession(__name__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__name__, True)
_logsi.SystemLogger = logging.getLogger(__name__)

@export
class SoundTouchClient:
    """
    The SoundTouchClient uses the underlying Bose Web Socket api to communicate 
    with a specified Bose SoundTouch device. 
    
    This client communicates with a Bose device on port 8090 by default (the
    standard WebAPI port), but the port number can be changed.

    The client uses an urllib3.PoolManager instance to delegate the HTTP-requests.
    Set a custom manager with the manage_traffic() method.

    Like the BoseWebSocket, this client can be used in two ways: 1. create a
    client manually or 2. use the client within a _with_ statement. Additionally,
    this class implements a dict-like functionality. So, the loaded configuration
    can be accessed by typing: `config = client[<config_name>]`
    """

    def __init__(self, device:SoundTouchDevice, raiseErrors:bool=True, manager:PoolManager=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            device (SoundTouchDevice):
                The device to interace with. Some configuration data stored here will be
                updated if specific methods were called in this client.
            raiseErrors (bool):
                Specifies if the client should raise exceptions returned by the SoundTouch
                device. Use `ignore` to ignore the errors (they will be given as the
                response object in a SoundTouchMessage).
                Default = 'raise'.
            manager (urllib3.PoolManager):
                The manager for HTTP requests to the device.
        """
        self._ConfigurationCache:dict = {}
        self._Device:SoundTouchDevice = device
        self._Manager:PoolManager = PoolManager(num_pools=5, headers={'User-Agent': 'BoseSoundTouchApi/1.0.0'})
        self._RaiseErrors:bool = bool(raiseErrors)
        self._SnapshotSettings:dict = {}
        
        # cache configurations that we have already obtained.
        self._ConfigurationCache[SoundTouchNodes.info.Path] = device._Information
        self._ConfigurationCache[SoundTouchNodes.supportedURLs.Path] = device._SupportedUrls
        

    def __enter__(self) -> 'SoundTouchClient':
        # if called via a context manager (e.g. "with" statement).
        return self


    def __exit__(self, etype, value, traceback) -> None:
        # if called via a context manager (e.g. "with" statement).
        pass
    

    def __getitem__(self, key):
        if repr(key) in self._ConfigurationCache:
            return self._ConfigurationCache[repr(key)]


    def __setitem__(self, key, value):
        if not isinstance(key, str):
            key = repr(key)
        self._ConfigurationCache[key] = value


    def __iter__(self):
        return iter(self._ConfigurationCache)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ConfigurationCache(self) -> dict:
        """ 
        A dictionary of cached configuration objects that have been obtained from
        the SoundTouch device.  Use the objects in this cache whenever it is
        too expensive or time consuming to make a real-time request from the device.

        The configuration cache is updated for any "Get...()" methods that return
        device information.  All of the "Get...()" methods have a `refresh:bool`
        argument that controls where information is obtained from; if refresh=True,
        then the device is queried for real-time configuration information. If
        refresh=False, then the configuration information is pulled from the configuration
        cache dictionary; if the cache does not contain the object, then the device
        is queried for real-time configuration information.
        
        It is obviously MUCH faster to retrieve device configuration objects from the 
        cache than from real-time device queries.  This works very well for configuration
        objects that do not change very often (e.g. Capabilities, Language, SourceList,
        etc).  You will still want to make real-time queries for configuration objects
        that change frequently (e.g. Volume, NowPlayingStatus, Presets, etc).
        
        This property is read-only, and is set when the class is instantiated.  The
        dictionary entries can be changed, but not the dictionary itself.

        Returns:
            The `_ConfigurationCache` property value.
            
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/ConfigurationCache.py
        ```
        </details>
        """
        return self._ConfigurationCache
    

    @property
    def Device(self) -> SoundTouchDevice:
        """
        The SoundTouchDevice object used to connect to the SoundTouch device.
        
        This property is read-only, and is set when the class is instantiated.
        """
        return self._Device


    @property
    def Manager(self) -> PoolManager:
        """ 
        Sets the request PoolManager object to use for http requests
        to the device.
        
        Returns:
            The `_Manager' property value.
        """
        return self._Manager
    
    @Manager.setter
    def Manager(self, value:PoolManager):
        """ 
        Sets the Manager property value.
        """
        if value != None:
            if isinstance(value, PoolManager):
                self._Manager = value


    @property
    def SnapshotSettings(self) -> dict:
        """
        A dictionary of configuration objects that are used by the Snapshot
        processing methods.
        
        This property is read-only.
        """
        return self._SnapshotSettings


    def _CheckResponseForErrors(self, element:Element):
        """
        Checks a device response for errors.  If found, a `SoundTouchError`
        is raised to inform the user of the error.
        
        Args:
            element (xml.etree.ElementTree.Element): 
                The response element to inspect.
                
        Raises:
            SoundTouchError: 
                If the element argument represents an error element.
        """
        # if we are ignoring errors then we are done.
        if (not self._RaiseErrors):
            return

        # if it's an error response then process it.
        if (element.tag in ['errors', 'error', 'Error']):

            # find the error portion of the message and raise a SoundTouchError.
            error = element.find('error')
            if error != None:
                errValue:int = int(error.get('value', -1))
                errName:str =  error.get('name', 'NONE')
                errSeverity:str =  error.get('severity', 'NONE')
                errText:str = error.text
                if errText is None or len(errText.strip()) == 0: errText = errName
                errMessage = BSTAppMessages.BST_WEBSERVICES_API_ERROR % (self.Device.DeviceName, errText)
                raise SoundTouchError(errMessage, errName, errSeverity, errValue, _logsi)
            
            # sometimes an error is not returned in an <errors> collection:
            # status=200 - <Error value="401" name="HTTP_STATUS_UNAUTHORIZED" severity="Unknown">app_key not authorized</Error>
            # status=200 - <Error value="415" name="HTTP_STATUS_UNSUPPORTED_MEDIA_TYPE" severity="Unknown">media referenced by url is not supported by speaker</Error>
            if element.tag == 'Error':
                error = element
                errValue:int = int(error.get('value', -1))
                errName:str =  error.get('name', 'NONE')
                errSeverity:str =  error.get('severity', 'NONE')
                errText:str = error.text
                if errText is None or len(errText.strip()) == 0: errText = errName
                errMessage = BSTAppMessages.BST_WEBSERVICES_API_ERROR % (self.Device.DeviceName, errText)
                raise SoundTouchError(errMessage, errName, errSeverity, errValue, _logsi)
        return


    def _GetMetadataFromUrl_nBytes(self, url, size):

        headers={'Range': 'bytes=%s-%s' % (0, size-1)}
        response = self._Manager.request("GET", url, headers=headers, retries=False, timeout=Timeout(connect=0.1, read=0.1))

        # req = request.Request(url)
        # req.headers['Range'] = 'bytes=%s-%s' % (0, size-1)
        # response = request.urlopen(req)
        #return response.read()
        return response.data


    def _GetMetadataFromUrl(self, url:str) -> TinyTag:
        """
        Args:
            url (str):
                The url to play, which also contains ID3V2 header data.

        Returns:                                
            A `TinyTag` object with the retrieved metadata if found; otherwise, None.
        """
        try:
            
            # download the first 10 bytes of the mp3 file
            # if no ID3 header present then we are done.
            data = self._GetMetadataFromUrl_nBytes(url, 10)
            if data[0:3] != b'ID3':
                return None

            # extract the ID3v2 header and compute the size of the id3v2 header.
            size_encoded = bytearray(data[-4:])
            size = reduce(lambda a,b: a*128+b, size_encoded, 0)

            # download the ID3v2 header into memory; we will also include one full
            # frame in order to function. Add max frame size
            header = BytesIO()
            data = self._GetMetadataFromUrl_nBytes(url, size+2881)  # 2881 = max frame size
            header.write(data)
            header.seek(0)

            # use TinyTag package to retrieve metadata from ID3v2 header, including image if present
            metadata = TinyTag.get(file_obj=header, image=True)

            # return metadata to caller.
            return metadata
        
        except Exception:
        
            # ignore exceptions, no metadata available is acceptable.
            return None
        

    def _ValidateDelay(self, delay:int, default:int=5, maxDelay:int=10) -> int:
        """
        Validates a delay value
        
        Args:
            delay (int):
                The delay value to validate.
            default (int):
                The default delay value to set if the user-input delay is not valid.
            maxDelay (int):
                The maximum delay value allowed.  
                Default is 10.
        """
        if (not isinstance(delay,int)) or (delay < 0): 
            result = default
        elif (delay > maxDelay): 
            result = maxDelay
        else:
            result = delay
        return result


    def Action(self, keyName:SoundTouchKeys, keyState:KeyStates=KeyStates.Both) -> None:
        """
        Tries to imitate a pressed key.

        Args:
            keyName (SoundTouchKeys|str): 
                The specified key to press.
            keyState (KeyStates|str): 
                Key state to select (press, release, or both).

        This method can be used to invoke different actions by using the different
        keys defined in `bosesoundtouchapi.soundtouchkeys.SoundTouchKeys`.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/Action.py
        ```
        </details>
        """
        key:str = str(keyName)
        if isinstance(keyName, SoundTouchKeys):
            key = keyName.value
            
        state:str = str(keyState)
        if isinstance(keyState, KeyStates):
            state = keyState.value
            
        xmlRequest = f'<key state="%s" sender="Gabbo">{key}</key>'
        
        # send press or release or both based upon state argument.
        _logsi.LogVerbose(MSG_TRACE_ACTION_KEY % (key, state, self.Device.DeviceName))
        if state in ['press','both']:
            self.Put(SoundTouchNodes.key, xmlRequest % 'press')
        if state in ['release','both']:
            self.Put(SoundTouchNodes.key, xmlRequest % 'release')


    def AddFavorite(self) -> None:
        """ 
        Adds the currently playing media to the device favorites.

        This will first make a call to `GetNowPlayingStatus()` method to ensure
        favorites are enabled for the now playing media.  If not enabled, then
        the request is ignored and no exception is raised.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/AddFavorite.py
        ```
        </details>
        """
        # get current nowPlaying status.
        nowPlaying:NowPlayingStatus = self.GetNowPlayingStatus(True)

        # can the nowPlaying item be a favorite?
        if nowPlaying.IsFavoriteEnabled:
            self.Action(SoundTouchKeys.ADD_FAVORITE, KeyStates.Press)
        else:
            _logsi.LogVerbose(MSG_TRACE_FAVORITE_NOT_ENABLED % nowPlaying.ToString())


    def AddMusicServiceSources(self) -> list[str]:
        """
        Adds any servers in the `MediaServerList` to the sources list if they do not exist
        in the sources list as a "STORED_MUSIC" source.
        
        Returns:
            A list of descriptions (e.g. "Friendly Name (sourceAccount)") that were added
            to the source list.

        This method retrieves the list of available media servers, as well as the list of
        sources defined to the device.  It will then compare the two lists, adding any media
        server(s) to the source list if they are not present.
        
        UPnP media server music service (e.g. "STORED_MUSIC") sources can only be added if the
        device has detected the UPnP media server.  The detected UPnP media servers will appear
        in the `MediaServerList` of items obtained using a call to `GetMediaServerList` method.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/AddMusicServiceSources.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.setMusicServiceAccount.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        result:list[str] = []

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND % ("AddMusicServiceSources", self.Device.DeviceName))
        
        # get list of defined sources.
        sourceList:SourceList = self.GetSourceList()
    
        # get list of upnp media services detected by the device.
        mediaServerList:MediaServerList = self.GetMediaServerList()
    
        # add music service account sources for upnp media servers not in the source list.
        # remove all music service account sources for upnp media servers.
        mediaServer:MediaServer
        for mediaServer in mediaServerList:
            sourceAccount:str = "%s%s" % (mediaServer.ServerId, "/0")
            
            # see if media server is defined in the source list.
            found:bool = False
            sourceItem:SourceItem
            for sourceItem in sourceList:
                if sourceItem.SourceAccount == mediaServer.ServerId:
                    found = True
                    break
                elif sourceItem.SourceAccount == sourceAccount:
                    found = True
                    
            # is media server defined in the source list?  if not, then add it.
            if found == False:
                self.SetMusicServiceAccount("STORED_MUSIC", mediaServer.FriendlyName, sourceAccount, None)
                result.append("%s (%s)" % (mediaServer.FriendlyName, sourceAccount))
                
        return result   

    def AddMusicServiceStation(self, addStation:AddStation) -> SoundTouchMessage:
        """
        Adds a station to a music service (e.g. PANDORA, etc) collection of previously 
        stored stations.
        
        Args:
            addStation (AddStation):
                Criteria used to add the music service station.

        Returns:
            A `SoundTouchMessage` object that contains the response.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `addStation` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        The added station will be immediately selected for playing.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/AddMusicServiceStation.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.addStation.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("addStation", addStation.ToString(), self.Device.DeviceName))
        result:SoundTouchMessage = self.Put(SoundTouchNodes.addStation, addStation)
        return result


    def AddZoneMembers(self, members:list[ZoneMember], delay:int=3) -> SoundTouchMessage:
        """
        Adds the given zone members to the device's zone.
        
        Args:
            members (list):
                A list of `ZoneMember` objects to add to the master zone.
            delay (int):
                Time delay (in seconds) to wait AFTER adding zone members.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 3; value range is 0 - 10.
                
        Raises:
            SoundTouchError:
                Master zone status could not be retrieved.  
                Master zone does not exist; zone members cannot be added.  
                Members argument was not supplied, or has no members.  
                Members argument contained a list item that is not of type `ZoneMember`.  
        
        The SoundTouch master device cannot find zone members without their device id.  
        
        The SoundTouch device does not return errors if a zone member device id does not
        exist; it simply ignores the invalid member entry and moves on to the next.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/AddZoneMembers.py
        ```
        </details>
        """
        # validations.
        if not members or len(members) == 0:
            raise SoundTouchError('Members argument was not supplied, or has no members', logsi=_logsi)
        delay = self._ValidateDelay(delay, 3, 10)
        
        # get master zone status.
        # we do this to retrieve the master zone device id.
        masterZone:Zone = self.GetZoneStatus(refresh=True)
        if masterZone is None:
            raise SoundTouchError('Master zone status could not be retrieved', logsi=_logsi)
        if len(masterZone.Members) == 0:
            raise SoundTouchError('Master zone does not exist; zone members cannot be added', logsi=_logsi)
        
        # create a temporary Zone object (used to add zone members)
        # and add the zone members that we want to add.
        tempZone:Zone = Zone(masterZone.MasterDeviceId)
        for member in members:
            tempZone.AddMember(member, _logsi)

        _logsi.LogVerbose("Adding zone members from SoundTouch device: '%s' - %s" % (
            self.Device.DeviceName, tempZone.ToStringMemberSummary()))
        
        # add the member zones from the device.
        result = self.Put(SoundTouchNodes.addZoneSlave, tempZone.ToXmlString())
    
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)

        return result


    # def Bookmark(self) -> None:
    #     """ 
    #     Bookmarks the currently playing media.
        
    #     This function is only supported by the Pandora Music Service.

    #     <details>
    #       <summary>Sample Code</summary>
    #     ```python
    #     .. include:: ../docs/include/samplecode/SoundTouchClient/Bookmark.py
    #     ```
    #     </details>
    #     """
    #     self.Action(SoundTouchKeys.BOOKMARK, KeyStates.Press)


    def ClearBluetoothPaired(self) -> SoundTouchMessage:
        """
        Clears all existing bluetooth pairings from the device.
        
        Raises:
            SoundTouchError:
                If the device is not capable of supporting `enterBluetoothPairing` function,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        After the method completes, any existing bluetooth pairings from other devices will no 
        longer be able to connect; you will need to re-pair each device.
        
        Some SoundTouch devices will emit a descending tone when the pairing list is cleared.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/ClearBluetoothPaired.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.clearBluetoothPaired.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        return self.Get(SoundTouchNodes.clearBluetoothPaired)


    def CreateGroupStereoPair(self, group:Group) -> Group:
        """
        Creates a new left / right stereo pair speaker group.
        
        Args:
            group (Group):
                Speaker group configuration object that defines the group.  
                
        Raises:
            SoundTouchError:
                group argument was not supplied.  
                group argument is not of type Group.  
                group argument did not contain any roles.  The group must have at least 
                two group roles in order to create a group.  
                
        The device that issues the call to this method will be the master of the group.
        
        The group argument should contain 2 roles (LEFT and RIGHT) with the device
        information (ip address and device id).
        
        The device will generate a `groupUpdated` websocket event, which contains the 
        updated `Group` configuration.

        The ST-10 is the only SoundTouch product that supports stereo pair groups.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/CreateGroupStereoPair.py
        ```
        </details>
        """
        # validations.
        if group is None:
            raise SoundTouchError('group argument was not supplied', logsi=_logsi)
        if not isinstance(group, Group):
            raise SoundTouchError('group argument is not of type Group', logsi=_logsi)
        if len(group.Roles) != 2:
            raise SoundTouchError('group argument object did not contain 2 roles; the group must have 2 group roles', logsi=_logsi)
        if group.Roles[0].DeviceId != group.MasterDeviceId:
            raise SoundTouchError('group role at index zero must be the master device id', logsi=_logsi)

        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.addGroup.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        return self.Put(SoundTouchNodes.addGroup, group, Group)


    def CreateZone(self, zone:Zone, delay:int=3) -> SoundTouchMessage:
        """
        Creates a multiroom zone from a Zone object.
        
        Args:
            zone (Zone):
                Multiroom configuration (zone) object that will control the zone
                (e.g. the master).  This object also contains a list of all zone
                members that will be under its control (e.g. Members property).
            delay (int):
                Time delay (in seconds) to wait AFTER creating the zone.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 3; value range is 0 - 10.
                
        Raises:
            SoundTouchError:
                Zone argument was not supplied.  
                Zone argument is not of type Zone.  
                Zone argument did not contain any members.  The zone must have at least 
                one zone member in order to create a zone.  
                
        The master SoundTouch device cannot find zone members without their device id.
        
        The device that issues the call to this method will be the master of the zone.
        Multiple `ZoneMember` entries can be specified in the `Zone` object, to create
        a zone with ALL members in one call.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/CreateZone.py
        ```
        </details>
        """
        # validations.
        if zone is None:
            raise SoundTouchError('Zone argument was not supplied', logsi=_logsi)
        if not isinstance(zone, Zone):
            raise SoundTouchError('Zone argument is not of type Zone', logsi=_logsi)
        if len(zone.Members) == 0:
            raise SoundTouchError('Zone argument object did not contain any members; the zone must have at least one zone member', logsi=_logsi)
        delay = self._ValidateDelay(delay, 3, 10)
        
        # if first zone member is not the master, then insert the master in list position one.
        # this emulates the SoundTouch App behavior, in that it creates the zone member list
        # with the master device listed as the first member, followed by the other zone members:

        # <zone master="9070658C9D4A">
        #     <member ipaddress="192.168.1.131">9070658C9D4A</member>   <- master
        #     <member ipaddress="192.168.1.130">E8EB11B9B723</member>   <- member #1
        #     ... more zone members
        # </zone>
        if zone.Members[0].DeviceId != zone.MasterDeviceId:
            zone.Members.insert(0, ZoneMember(zone.MasterIpAddress, zone.MasterDeviceId))

        # create the zone.
        result = self.Put(SoundTouchNodes.setZone, zone.ToXmlString())
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)

        return result


    def CreateZoneFromDevices(self, master:SoundTouchDevice, members:list) -> Zone:
        """ 
        Creates a new multiroom zone with the given member devices. 

        Args:
            master (SoundTouchDevice):
                The device object that will control the zone (e.g. the master).
            members (list):
                A list of SoundTouchDevice objects that will be controlled by the
                master zone (e.g. the zone members).
                
        Raises:
            SoundTouchError:  
                Master argument was not supplied.  
                Master argument is not of type SoundTouchDevice.  
                Members argument is not of type list.  
                Members argument was not supplied, or has no members.  
                Members argument contained a list item that is not of type SoundTouchDevice.  

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/CreateZoneFromDevices.py
        ```
        </details>
        """
        if master is None:
            raise SoundTouchError('Master argument was not supplied', logsi=_logsi)
        if not isinstance(master, SoundTouchDevice):
            raise SoundTouchError('Master argument is not of type SoundTouchDevice', logsi=_logsi)
        if not isinstance(members, list):
            raise SoundTouchError('Members argument is not of type list', logsi=_logsi)
        if (members is None) or (len(members) == 0):
            raise SoundTouchError('Members argument was not supplied, or has no members', logsi=_logsi)

        # create new Zone master object.
        zone = Zone(master.DeviceId, master.Host, True)
        
        # validate members, and add zone members.
        member:SoundTouchDevice
        for member in members:
            if not isinstance(member, SoundTouchDevice):
                raise SoundTouchError('Member argument contained an entry in the list that is not of type SoundTouchDevice: %s' % str(member), logsi=_logsi)
            zone.AddMember(ZoneMember(member.Host, member.DeviceId), _logsi)

        # create the zone.
        self.CreateZone(zone)
        return zone


    def EnterBluetoothPairing(self) -> SoundTouchMessage:
        """
        Enters bluetooth pairing mode, and waits for a compatible device to pair with.
        
        Raises:
            SoundTouchError:
                If the device is not capable of supporting `enterBluetoothPairing` function,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        On the device you want to connect (e.g. phone, tablet, etc), turn on Bluetooth.  In the 
        Bluetooth settings menu of the device, the SoundTouch device name should appear within a 
        few seconds and allow your device to pair with it.  Some SoundTouch devices will have a 
        bluetooth indicator that turns blue when pairing mode is entered, as well as emit an 
        asccending tone when the pairing is complete.
        
        Once pairing is complete, the source is immediately switched to BLUETOOTH.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/EnterBluetoothPairing.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.enterBluetoothPairing.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        return self.Get(SoundTouchNodes.enterBluetoothPairing)
        

    def Get(self, uri:SoundTouchUri) -> SoundTouchMessage:
        """
        Makes a GET request to retrieve a stored value.

        Use this method when querying for specific nodes. All standard nodes
        are implemented by this class.

        Args:
            uri (SoundTouchUri):
                The node where the requested value is stored. DANGER: This request can also have
                a massive effect on your Bose device, for instance when calling
                `client.get(SoundTouchNodes.resetDefaults)`, it will wipe all data on the device and
                perform a factory reset.

        Returns:
            An object storing the request uri, optional a payload that has been sent and 
            the response as an `xml.etree.ElementTree.Element`.

        Raises:
            SoundTouchError:
                When errors should not be ignored on this client, they will raise a SoundTouchError
                exception with all information related to that error.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/Get.py
        ```
        </details>
        """
        message = SoundTouchMessage(uri)
        if uri and uri.UriType == SoundTouchUriTypes.OP_TYPE_EVENT:
            return message

        self.MakeRequest('GET', message)
        return message


    def GetAudioDspControls(self, refresh=True) -> AudioDspControls:
        """
        Gets the current audio DSP controls configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `AudioDspControls` object that contains audio dsp control
            configuration of the device IF the device supports it (e.g. ST-300, etc); 
            otherwise, None if the device does not support it.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `audiodspcontrols` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetAudioDspControls.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.audiodspcontrols.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("AudioDspControls", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.audiodspcontrols, AudioDspControls, refresh)


    def GetAudioProductLevelControls(self, refresh=True) -> AudioProductLevelControls:
        """
        Gets the current audio product level controls configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `AudioProductLevelControls` object that contains audio product level control
            configuration of the device IF the device supports it (e.g. ST-300, etc); 
            otherwise, None if the device does not support it.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `audioproductlevelcontrols` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetAudioProductLevelControls.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.audioproductlevelcontrols.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("AudioProductLevelControls", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.audioproductlevelcontrols, AudioProductLevelControls, refresh)


    def GetAudioProductToneControls(self, refresh=True) -> AudioProductToneControls:
        """
        Gets the current audio product tone controls configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `AudioProductToneControls` object that contains audio product tone control
            configuration of the device IF the device supports it (e.g. ST-300, etc); 
            otherwise, None if the device does not support it.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `audioproducttonecontrols` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetAudioProductToneControls.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.audioproducttonecontrols.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("AudioProductToneControls", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.audioproducttonecontrols, AudioProductToneControls, refresh)


    def GetAudioSpeakerAttributeAndSetting(self, refresh=True) -> AudioSpeakerAttributeAndSetting:
        """
        Gets the current audio speaker attrribute and setting configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `AudioSpeakerAttributeAndSetting` object that contains audio speaker attribute and setting
            configuration of the device IF the device supports it (e.g. ST-300, etc); 
            otherwise, None if the device does not support it.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `audiospeakerattributeandsetting` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetAudioSpeakerAttributeAndSetting.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.audiospeakerattributeandsetting.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("AudioSpeakerAttributeAndSetting", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.audiospeakerattributeandsetting, AudioSpeakerAttributeAndSetting, refresh)


    def GetBalance(self, refresh=True) -> Balance:
        """
        Gets the current balance configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `Balance` object that contains balance configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetBalance.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("Balance", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.balance, Balance, refresh)


    def GetBass(self, refresh=True) -> Bass:
        """
        Gets the current bass configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `Bass` object that contains bass configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetBass.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("Bass", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.bass, Bass, refresh)


    def GetBassCapabilities(self, refresh=True) -> BassCapabilities:
        """
        Gets the current bass capability configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `BassCapabilities` object that contains bass capabilities configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetBassCapabilities.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("BassCapabilities", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.bassCapabilities, BassCapabilities, refresh)


    def GetBlueToothInfo(self, refresh=True) -> BlueToothInfo:
        """
        Gets the current bluetooth configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `BlueToothInfo` object that contains bluetooth configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetBlueToothInfo.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("BlueToothInfo", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.bluetoothInfo, BlueToothInfo, refresh)


    def GetCapabilities(self, refresh=True) -> Capabilities:
        """
        Gets the current bass capability configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `Capabilities` object that contains capabilities configuration of the device.

        The returned object has a dict-like implementation; individual capabilities
        can be accessed by typing: `GetCapabilities_results['capability_name']`.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetCapabilities.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("Capabilities", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.capabilities, Capabilities, refresh)


    def GetClockConfig(self, refresh=True) -> ClockConfig:
        """
        Gets the current clock configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `ClockConfig` object that contains clock configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetClockConfig.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("ClockConfig", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.clockDisplay, ClockConfig, refresh)


    def GetClockTime(self, refresh=True) -> ClockTime:
        """
        Gets the current clock time configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `ClockTime` object that contains clock time configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetClockTime.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("ClockTime", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.clockTime, ClockTime, refresh)


    def GetDspMono(self, refresh=True) -> DSPMonoStereoItem:
        """
        Gets the current digital signal processor configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `DSPMonoStereoItem` object that contains DSP configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetDspMono.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("DSPMonoStereo", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.DSPMonoStereo, DSPMonoStereoItem, refresh)


    def GetGroupStereoPairStatus(self, refresh=True) -> Group:
        """
        Gets the current left / right stereo pair speaker group configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `Group` object that contains the result.

        The ST-10 is the only SoundTouch product that supports stereo pair groups.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetGroupStereoPairStatus.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.getGroup.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("Group", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.getGroup, Group, refresh)


    def GetInformation(self, refresh=True) -> Information:
        """
        Gets the information configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `Information` object that contains the results.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `info` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetInformation.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.info.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("info", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.info, Information, refresh)


    def GetIntrospectData(self, introspect:Introspect) -> str:
        """
        Gets introspect data for a specified source.

        Args:
            introspect (Introspect):
                Introspect object to retrieve introspect data for.

        Returns:
            A string that contains the introspect xml response.
            
        The introspect xml response returned can vary by source type, and if the source
        is currently in use (e.g. NowPlaying) or not.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetIntrospectData.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.introspect.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("introspect", "%s:%s" % (introspect.Source, introspect.SourceAccount or ""), self.Device.DeviceName))
        msg:SoundTouchMessage = self.Put(SoundTouchNodes.introspect, introspect)
        
        xmlResult:str = None
        if msg.Response is not None:
            ElementTree.indent(msg.Response)  
            xmlResult:str = ElementTree.tostring(msg.Response, encoding='unicode', xml_declaration=True)
        return xmlResult


    def GetLanguage(self, refresh=True) -> SimpleConfig:
        """
        Gets the current language configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `SimpleConfig` object that contains language configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetLanguage.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("Language", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.language, SimpleConfig, refresh)


    def GetMediaServerList(self, refresh=True) -> MediaServerList:
        """
        Gets the list of UPnP media servers found by the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `MediaServerList` object that contains media server configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetMediaServerList.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("MediaServerList", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.listMediaServers, MediaServerList, refresh)


    def GetMusicLibraryItems(self, navigate:Navigate) -> NavigateResponse:
        """
        Gets a list of music library data from the specified music library (e.g. STORED_MUSIC, etc).
        
        Args:
            navigate (Navigate):
                Navigate criteria used to search the music library.

        Returns:
            A `NavigateResponse` object that contains the navigation response.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `navigate` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Use the `GetSourceList` method to get the `source` and `sourceAccount` values for 
        the specific NAS Music Library you wish to navigate.
                
        A returned `NavigateResponse` item can be used to play the item's media content by 
        passing its `ContentItem` value to the `PlayContentItem` method.

        Music library containers can be traversed by issuing calls to a child container's 
        `ContentItem`, starting at the Root container.  

        Music library containers can also be traversed by issuing calls that start at a specific 
        container.  For example, lets say you like to listen to songs from your favorite album; 
        you could navigate the container directly if you know the source, sourceAccount, and 
        location values.
        
        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetMusicLibraryItems.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.navigate.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("navigate", navigate.ContainerTitle, self.Device.DeviceName))
        result:NavigateResponse = self.Put(SoundTouchNodes.navigate, navigate, NavigateResponse)
        return result


    def GetMusicServiceStations(self, navigate:Navigate) -> NavigateResponse:
        """
        Gets a list of your stored stations from the specified music service (e.g. PANDORA, etc).
        
        Args:
            navigate (Navigate):
                Navigate criteria used to search the music service.

        Returns:
            A `NavigateResponse` object that contains the navigation response.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `navigate` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetMusicServiceStations.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.navigate.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("navigate", navigate.ContainerTitle, self.Device.DeviceName))
        result:NavigateResponse = self.Put(SoundTouchNodes.navigate, navigate, NavigateResponse)
        return result


    def GetName(self, refresh=True) -> SimpleConfig:
        """
        Gets the current name configuration of the device, and updates the SoundTouchDevice 
        class device name if possible.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `SimpleConfig` object that contains name configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetName.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("Name", self.Device.DeviceName))
        name = self.GetProperty(SoundTouchNodes.name, SimpleConfig, refresh)
        
        if name.Value != self.Device.DeviceName:
            self.Device.DeviceName = name.Value
            
        return name


    def GetNetworkInfo(self, refresh=True) -> NetworkInfo:
        """
        Gets the current network information configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `NetworkInfo` object that contains network information configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python 
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetNetworkInfo.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("NetworkInfo", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.networkInfo, NetworkInfo, refresh)


    def GetNetworkStatus(self, refresh=True) -> NetworkStatus:
        """
        Gets the current network status configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `NetworkStatus` object that contains network status configuration of the device.
            
        This method can be used to retrieve the network status of the device for each
        network interface that has established a connection.  This includes details like
        the interface name (e.g. 'eth0'), the network SSID, MAC Address, and more.

        <details>
          <summary>Sample Code</summary>
        ```python 
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetNetworkStatus.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("NetworkStatus", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.netStats, NetworkStatus, refresh)


    def GetNowPlayingStatus(self, refresh=True) -> NowPlayingStatus:
        """
        Gets the now playing status configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `NowPlayingStatus` object that contains now playing status configuration of the device.
            
            
        This method can be used to retrieve the status of media that is currently playing
        on the device.  This includes the media source, ContentItem, track, artist,
        album, preview image, duration, position, play status, shuffle and repeat setting,
        stream type, track ID, station description and the location of the station.
        
        Some special nodes of interest:
        - `<isAdvertisement />` node will be present if the currently playing media content is an advertidement.  
        - `<isFavorite />` node will be present if the currently playing media content is marked as a favorite.   
        - `<favoriteEnabled />` node will be present if the currently playing media content can be marked as a favorite.   
        - `<rateEnabled />` node will be present if the currently playing media content can be rated (e.g. thumbs up, down).   
        - `<skipEnabled />` node will be present if the currently playing media content supports skip control.  
        - `<shuffleSetting>` node will be present if the currently playing media supports shuffle mode.  
        - `<repeatSetting>` node will be present if the currently playing media supports repeat mode.  

        <details>
          <summary>Sample Code</summary>
        ```python 
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetNowPlayingStatus.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("NowPlayingStatus", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.nowPlaying, NowPlayingStatus, refresh)


    def GetOptions(self, uri:SoundTouchUri) -> list:
        """
        Makes an OPTIONS request and returns the list of available HTTP-Methods.

        Use this method when testing whether a node can be accessed.

        Args:
            uri (SoundTouchUri):
                The node where the requested value is stored.

        Returns:
            A list of strings storing all available HTTP-Methods.

        Raises:
            SoundTouchError:
                When errors should not be ignored on this client, they will raise a SoundTouchError
                exception with all information related to that error.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetOptions.py
        ```
        </details>
        """
        message = SoundTouchMessage(uri)
        headers = self.MakeRequest('OPTIONS', message)
        if isinstance(headers, int):
            return []
        return headers['Allow'].split(', ')


    def GetPowerManagement(self, refresh=True) -> PowerManagement:
        """
        Gets the current power management status configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `PowerManagement` object that contains power management configuration of the device.
            
        <details>
          <summary>Sample Code</summary>
        ```python 
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetPowerManagement.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("PowerManagement", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.powerManagement, PowerManagement, refresh)


    def GetPresetList(self, refresh=True) -> PresetList:
        """
        Gets the current preset list configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `PresetList` object that contains preset list configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetPresetList.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("PresetList", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.presets, PresetList, refresh)
        

    def GetProductCecHdmiControl(self, refresh=True) -> ProductCecHdmiControl:
        """
        Gets the current product CEC HDMI control configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `ProductCecHdmiControl` object that contains product CEC HDMI control
            configuration of the device IF the device supports it (e.g. ST-300, etc); 
            otherwise, None if the device does not support it.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `productcechdmicontrol` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetProductCecHdmiControl.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.productcechdmicontrol.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("ProductCecHdmiControl", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.productcechdmicontrol, ProductCecHdmiControl, refresh)


    def GetProductHdmiAssignmentControls(self, refresh=True) -> ProductHdmiAssignmentControls:
        """
        Gets the current product HDMI assignment controls configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `ProductHdmiAssignmentControls` object that contains product HDMI assignment control
            configuration of the device IF the device supports it (e.g. ST-300, etc); 
            otherwise, None if the device does not support it.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `producthdmiassignmentcontrols` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetProductHdmiAssignmentControls.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.producthdmiassignmentcontrols.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("ProductHdmiAssignmentControls", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.producthdmiassignmentcontrols, ProductHdmiAssignmentControls, refresh)


    def GetProperty(self, uri:SoundTouchUri, classType, refresh=True):
        """
        Returns a cached property mapped to the given URI.
        
        Args:
            uri (SoundTouchUri):
                The property key (e.g. 'balance', 'volume', etc).
            classType (type):
                The configuration class type (e.g. Balance, Volume, etc).
            refresh (bool):
                True to refresh the property with real-time information from the device;
                otherwise, False to just return the cached value.
                
        Returns:
            A configuration instance of the provided classType argument.

        This method will refresh the property from the device if the property
        does not exist in the cache, regardless of the refresh argument value.
        """
        cacheDesc:str = 'cached'
        if repr(uri) not in self or refresh:
            self.RefreshConfiguration(uri, classType)
            cacheDesc = 'current'

        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogVerbose("SoundTouchClient configuration object (%s): '%s'" % (cacheDesc, str(self[uri])))

        return self[uri]


    def GetReBroadcastLatencyMode(self, refresh=True) -> RebroadcastLatencyMode:
        """
        Gets the current rebroadcast latency mode configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `RebroadcastLatencyMode` object that contains rebroadcast latency mode
            configuration of the device IF the device supports it; 
            otherwise, None if the device does not support it.
            
        Raises:
            SoundTouchError:
                If the device is not capable of supporting `rebroadcastlatencymode` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetReBroadcastLatencyMode.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.rebroadcastlatencymode.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("RebroadcastLatencyMode", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.rebroadcastlatencymode, RebroadcastLatencyMode, refresh)


    def GetRecentList(self, refresh=True) -> RecentList:
        """
        Gets the current recent list configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `RecentList` object that contains recent list configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetRecentList.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("RecentList", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.recents, RecentList, refresh)
        

    def GetRequestToken(self, refresh=True) -> SimpleConfig:
        """
        Gets a new bearer token generated by the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `SimpleConfig` object that contains the request token in the Attribute property.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetRequestToken.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("RequestToken", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.requestToken, SimpleConfig, refresh)


    def GetServiceAvailability(self, refresh=True) -> ServiceAvailability:
        """
        Gets the current service availability configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `ServiceAvailability` object that contains service availability configuration of the device.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `serviceAvailability` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        <details>
          <summary>Sample Code</summary>
        ```python 
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetServiceAvailability.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.serviceAvailability.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("ServiceAvailability", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.serviceAvailability, ServiceAvailability, refresh)


    def GetSoftwareUpdateStatus(self, refresh=True) -> SoftwareUpdateQueryResponse:
        """
        Gets the status of a SoundTouch software update for the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `SoftwareUpdateQueryResponse` object that contains software update status
            configuration of the device IF the device supports it; otherwise, None if the 
            device does not support it.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `swUpdateQuery` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetSoftwareUpdateStatus.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.swUpdateQuery.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("SoftwareUpdateQueryResponse", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.swUpdateQuery, SoftwareUpdateQueryResponse, refresh)


    def GetSoftwareUpdateCheckInfo(self, refresh=True) -> SoftwareUpdateCheckResponse:
        """
        Gets the latest available software update release version information for the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `SoftwareUpdateCheckResponse` object that contains software release information
            configuration of the device IF the device supports it; otherwise, None if the 
            device does not support it.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `swUpdateCheck` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetSoftwareUpdateCheckInfo.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.swUpdateCheck.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("SoftwareUpdateCheckResponse", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.swUpdateCheck, SoftwareUpdateCheckResponse, refresh)


    def GetSoundTouchConfigurationStatus(self, refresh=True) -> SoundTouchConfigurationStatus:
        """
        Gets the current SoundTouch configuration status configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `SoundTouchConfigurationStatus` object that contains SoundTouch configuration status of the device.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `soundTouchConfigurationStatus` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetSoundTouchConfigurationStatus.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.soundTouchConfigurationStatus.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("SoundTouchConfigurationStatus", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.soundTouchConfigurationStatus, SoundTouchConfigurationStatus, refresh)


    def GetSourceList(self, refresh=True) -> SourceList:
        """
        Gets the current source list configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `SourceList` object that contains source list configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetSourceList.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("SourceList", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.sources, SourceList, refresh)


    def GetSupportedUrls(self, refresh=True) -> SupportedUrls:
        """
        Gets the supported urls configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `SupportedUrls` object that contains the results.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `info` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetSupportedUrls.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.supportedURLs.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("supportedURLs", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.supportedURLs, SupportedUrls, refresh)


    def GetSystemTimeout(self, refresh=True) -> SystemTimeout:
        """
        Gets the current system timeout configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `SystemTimeout` object that contains system timeout configuration of the device.

        Use this method to determine whether power saving is enabled or not.
            
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetSystemTimeout.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("SystemTimeout", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.systemtimeout, SystemTimeout, refresh)


    def GetTrackInfo(self, refresh=True) -> TrackInfo:
        """
        Gets extended track information for the current playing music service media.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `TrackInfo` object that contains track information.
            
        Raises:
            SoundTouchError:
                If the device is not capable of supporting `trackInfo` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  
                
        This method only returns information if the currently playing content is from 
        a music service source (e.g. PANDORA, SPOTIFY, etc).  If currently playing media is 
        NOT from a music service source (e.g. AIRPLAY, STORED_MUSIC, etc) then the 
        SoundTouch webservice will become unresponsive (e.g. hangs) for about 30
        seconds until it times out with an error status.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetTrackInfo.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.trackInfo.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("TrackInfo", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.trackInfo, TrackInfo, refresh)


    def GetVolume(self, refresh=True) -> Volume:
        """
        Gets the current volume configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `Volume` object that contains volume configuration of the device.
            
        The `Target` and `Actual` returned values will only be different when the 
        volume is changing.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetVolume.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("Volume", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.volume, Volume, refresh)


    def GetWirelessProfile(self, refresh=True) -> WirelessProfile:
        """
        Gets the current wireless profile configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `WirelessProfile` object that contains wireless profile configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetWirelessProfile.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("WirelessProfile", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.getActiveWirelessProfile, WirelessProfile, refresh)


    def GetWirelessSiteSurvey(self, refresh=True) -> PerformWirelessSiteSurveyResponse:
        """
        Gets a list of wireless networks that can be detected by the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `PerformWirelessSiteSurveyResponse` object that contains wireless survey
            configuration of the device IF the device supports it (e.g. ST-300, etc); 
            otherwise, None if the device does not support it.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `performWirelessSiteSurvey` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetWirelessSiteSurvey.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.performWirelessSiteSurvey.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("PerformWirelessSiteSurveyResponse", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.performWirelessSiteSurvey, PerformWirelessSiteSurveyResponse, refresh)


    def GetZoneStatus(self, refresh=True) -> Zone:
        """
        Gets the current wireless zone status configuration of the device.

        Args:
            refresh (bool):
                True to query the device for realtime information and refresh the cache;
                otherwise, False to just return the cached information.

        Returns:
            A `Zone` object that contains zone configuration of the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/GetZoneStatus.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_GET_CONFIG_OBJECT % ("Zone", self.Device.DeviceName))
        return self.GetProperty(SoundTouchNodes.getZone, Zone, refresh)


    def MakeRequest(self, method:str, msg:SoundTouchMessage) -> int:
        """
        Performs a generic request by converting the response into the message object.
        
        Args:
            method (str): 
                The preferred HTTP method (e.g. "GET", "POST", etc).
            msg (SoundTouchMessage): 
                The altered message object.
                
        Returns:
            The status code (integer) or allowed methods (list).

        Raises:
            SoundTouchError: 
                If an error occurs while requesting content.
                
        A 400 status code is immediately returned for the following scenarios:  
        - The method argument is not supplied.  
        - The msg argument is not supplied.  
        - The msg.Uri is not in the device list of supported URI's.  

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MakeRequest.py
        ```
        </details>
        """
        if not method or not msg:
            return 400 # bad request

        if msg.Uri not in self.Device.SupportedUris:
            return 400

        url = f'http://{self.Device.Host}:{self.Device.Port}/{msg.Uri}'
        
        try:
            if msg.HasXmlMessage:
                reqbody:str = msg.XmlMessage
                reqbodyencoded:bytes = reqbody.encode('utf-8')
                _logsi.LogXml(SILevel.Verbose, "SoundTouchClient http request: '%s' (with body)" % (url), reqbody, prettyPrint=True)
                response = self._Manager.request(method, url, body=reqbodyencoded)
            else:
                _logsi.LogVerbose("SoundTouchClient http request: '%s'" % (url))
                response = self._Manager.request(method, url)

            _logsi.LogXml(SILevel.Verbose, "SoundTouchClient http response: (%s) %s" % (response.status, url), response.data.decode("utf-8"), prettyPrint=True)
            if _logsi.IsOn(SILevel.Debug):
                if (response.headers):
                    _logsi.LogCollection(SILevel.Debug, "SoundTouchClient http response headers", response.headers.items())

            if response.status == 200:
                if response.data:
                    msg.Response = fromstring(response.data)
                    self._CheckResponseForErrors(msg.Response)
            else:
                # soundtouch server can also issue errors response for http status codes other than 200 (e.g. 500, etc)
                # example - select AUX source with no sourceAccount specified.
                # request: <ContentItem source="AUX" />
                # result:  <errors deviceID="9070658C9D4A"><error value="1005" name="UNKNOWN_SOURCE_ERROR" severity="Unknown">1005</error></errors>
                if response.data:
                    msg.Response = fromstring(response.data)
                    self._CheckResponseForErrors(msg.Response)

            response.close()
            return response.headers
        
        except SoundTouchError: raise  # pass handled exceptions on thru
        except Exception as ex:
            
            # format unhandled exception.
            raise SoundTouchError(BSTAppMessages.UNHANDLED_EXCEPTION.format("MakeRequest", str(ex)), logsi=_logsi)


    def MediaNextTrack(self) -> None:
        """ 
        Move to the next track in the current media playlist.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaNextTrack.py
        ```
        </details>
        """
        self.SetUserTrackControl(UserTrackControlTypes.Next)


    def MediaPause(self) -> None:
        """ 
        Pause the current media playing.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaPause.py
        ```
        </details>
        """
        self.SetUserPlayControl(UserPlayControlTypes.Pause)


    def MediaPlay(self) -> None:
        """ 
        Play the currently paused media.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaPlay.py
        ```
        </details>
        """
        self.SetUserPlayControl(UserPlayControlTypes.Play)


    def MediaPlayPause(self) -> None:
        """ 
        Toggle the Play / Pause state of the current media playing.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaPlayPause.py
        ```
        </details>
        """
        self.SetUserPlayControl(UserPlayControlTypes.PlayPause)


    def MediaPreviousTrack(self, force:bool=False) -> None:
        """ 
        Play previous track if current track has been playing for less than 10 seconds;
        otherwise, restart play of the current track.
        
        Args:
            force (bool):
                If True, force the previous track to be played regardless of how much
                play time has passed for the current track; otherwise, False to restart
                the current track if more than 10 seconds have passed.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaPreviousTrack.py
        ```
        </details>
        """
        if force is not None and force == True:
            self.SetUserTrackControl(UserTrackControlTypes.PreviousForce)
        else:
            self.SetUserTrackControl(UserTrackControlTypes.Previous)
            

    def MediaRepeatAll(self) -> None:
        """ 
        Enables repeat all processing for the current media playlist.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaRepeatAll.py
        ```
        </details>
        """
        self.SetUserTrackControl(UserTrackControlTypes.RepeatAll)


    def MediaRepeatOff(self) -> None:
        """ 
        Turns off repeat (all / one) processing for the current media playlist.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaRepeatOff.py
        ```
        </details>
        """
        self.SetUserTrackControl(UserTrackControlTypes.RepeatOff)


    def MediaRepeatOne(self) -> None:
        """ 
        Enables repeat single track processing for the current media playlist.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaRepeatOne.py
        ```
        </details>
        """
        self.SetUserTrackControl(UserTrackControlTypes.RepeatOne)


    def MediaResume(self) -> None:
        """ 
        Resume the current media playing. 

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaResume.py
        ```
        </details>
        """
        self.SetUserPlayControl(UserPlayControlTypes.Play)


    def MediaShuffleOff(self) -> None:
        """ 
        Disables shuffling of the current media playlist. 

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaShuffleOff.py
        ```
        </details>
        """
        self.SetUserTrackControl(UserTrackControlTypes.ShuffleOff)


    def MediaShuffleOn(self) -> None:
        """ 
        Enables shuffling of the current media playlist. 

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaShuffleOn.py
        ```
        </details>
        """
        self.SetUserTrackControl(UserTrackControlTypes.ShuffleOn)


    def MediaStop(self) -> None:
        """ 
        Stop the current media playing. 

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MediaStop.py
        ```
        </details>
        """
        self.SetUserPlayControl(UserPlayControlTypes.Stop)


    def Mute(self) -> None:
        """
        Toggle mute / unmute.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/Mute.py
        ```
        </details>
        """
        self.Action(SoundTouchKeys.MUTE, KeyStates.Press)


    def MuteOff(self, refresh: bool=True) -> None:
        """
        Unmutes the device, if the device is currently muted.
        
        Args:
            refresh (bool):
                True to check the real-time status of the device; otherwise, False
                to check the cached status of the device.  
                Default = True.
            
        This will first issue a `GetVolume()` method call to query the current volume of the
        device.  If the refresh argument is True, then the volume status is refreshed with real-time
        data; otherwise the cached volume status is used.
        
        If the volume IsMuted property is true, then the MUTE key will be sent to unmute the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MuteOff.py
        ```
        </details>
        """
        volume:Volume = self.GetVolume(refresh)
        if (volume):
            if (volume.IsMuted):
                self.Action(SoundTouchKeys.MUTE, KeyStates.Press)


    def MuteOn(self, refresh: bool=True) -> None:
        """
        Mutes the device, if the device is currently not muted.
        
        Args:
            refresh (bool):
                True to check the real-time status of the device; otherwise, False
                to check the cached status of the device.  
                Default = True.
            
        This will first issue a `GetVolume()` method call to query the current volume of the
        device.  If the refresh argument is True, then the volume status is refreshed with real-time
        data; otherwise the cached volume status is used.
        
        If the volume IsMuted property is false, then the MUTE key will be sent to mute the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/MuteOn.py
        ```
        </details>
        """
        volume:Volume = self.GetVolume(refresh)
        if (volume):
            if (not volume.IsMuted):
                self.Action(SoundTouchKeys.MUTE, KeyStates.Press)
                

    def PlayContentItem(self, item:ContentItem, delay:int=5) -> SoundTouchMessage:
        """
        Plays the given ContentItem.

        Args:
            item (ContentItem):
                Content item to play.
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the content item.  
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 5; value range is 0 - 10.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/PlayContentItem.py
        ```
        </details>
        """
        return self.SelectContentItem(item, delay)


    def PlayNotificationBeep(self) -> SoundTouchMessage:
        """
        Plays a notification beep on the device.  This will cause device to pause the 
        currently playing media, emit a double beep sound, and then resume the media play.
        
        Raises:
            SoundTouchError:
                If the device is not capable of supporting `playNotification` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-10 will support this, but the ST-300 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/PlayNotificationBeep.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.playNotification.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        return self.Get(SoundTouchNodes.playNotification)
        

    def PlayNotificationTTS(self, sayText:str, ttsUrl:str=None, 
                            artist:str=None, album:str=None, track:str=None,  
                            volumeLevel:int=0, appKey:str=None
                            ) -> SoundTouchMessage:
        """
        Plays a notification message via Google TTS (Text-To-Speech) processing.
        
        Args:
            sayText (str):
                The message that will be converted from text to speech and played
                on the device.
            ttsUrl (str):
                The Text-To-Speech url used to translate the message.  
                The value should contain a "{saytext}" format parameter, that will be used
                to insert the encoded sayText value.
                Default value is:  
                "http://translate.google.com/translate_tts?ie=UTF-8&tl=EN&client=tw-ob&q={saytext}"
            artist (str):
                The message text that will appear in the NowPlaying Artist node.  
                Default is "TTS Notification"
            album (str):
                The message text that will appear in the NowPlaying Album node.  
                Default is "Google TTS"
            track (str):
                The message text that will appear in the NowPlaying Track node.  
                Default is the sayText argument value.
            volumeLevel (int):
                The temporary volume level that will be used when the message is played.  
                Specify a value of zero to play at the current volume.  
                Per Bose limitations, max level cannot be more than 70.
                Default is zero.
            appKey (str):
                Bose Developer API application key.
        
        Raises:
            SoundTouchError:
                ttsUrl argument value does not start with 'http://'.
                ttsUrl argument was not a string; ignoring PlayNotificationTTS request.
                
        Note that SoundTouch devices do not support playing content from HTTPS (secure 
        socket layer) url's.  A `SoundTouchError` will be raised if a non `http://` url 
        is supplied for the ttsUrl argument.
        
        There are models of Bose SoundTouch speakers that do not support notifications. Only the 
        Bose SoundTouch 10 in the III series support notifications, as far as I know.
        I could not get this to work on my SoundTouch 300, and another user reported that the
        ST-20 did not support it either.

        The notification message is played at the level specified by the volumeLevel argument.
        Specify a volumeLevel of zero to play the notification at the current volume level.
        The volume level is restored to the level it was before the notification message was 
        played after the notification is complete; e.g. if you made changes to the volume while
        the notification is playing then they are changed back to the volume level that was in
        effect prior to playing the notification.  The SoundTouch device automatically takes 
        care of the volume level switching; there are no calls in the method to change the 
        volume or currently playing content status.  The SoundTouch device also limits the
        volume range between 10 (min) and 70 (max); this is a Bose limitation, and is not
        imposed by this API.
        
        The currently playing content (if any) is paused while the notification message
        content is played, and then resumed once the notification ends.
        
        The `<service>` node content will appear in the NowPlaying status `<artist>` node.  
        The `<message>` node content will appear in the NowPlaying status `<album>` node.  
        The `<reason>` node content will appear in the NowPlaying status `<track>` node.  
        
        If the device is the master controller of a zone, then the notification message will 
        be played on all devices that are members of the zone.
        
        A small delay can be inserted at the start of the message by prefixing the `sayText`
        argument value with "a!".  Example: "a!This is a test message".  It's not a perfect
        solution, but works for me since my SoundTouch speaker takes a second or two to switch
        into active mode, and the first second of the played message is lost.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/PlayNotificationTTS.py
        ```
        </details>
        """
        if sayText is None or len(sayText) == 0:
            _logsi.LogWarning("sayText argument was not supplied to PlayNotificationTTS method; ignoring request")
            return
        
        if ttsUrl is None:
            ttsUrl:str = "http://translate.google.com/translate_tts?ie=UTF-8&tl=EN&client=tw-ob&q={saytext}"
        if not isinstance(ttsUrl, str):
            raise SoundTouchError("ttsUrl argument was not a string; ignoring PlayNotificationTTS request", logsi=_logsi)
        ttsUrl = ttsUrl.lstrip()
        if not re.match(r'http://', ttsUrl):
            raise SoundTouchError("ttsUrl argument value does not start with 'http://'", logsi=_logsi)

        if artist is None:
            artist = "TTS Notification"
        if album is None:
            album = "Google TTS"
        if track is None:
            track = sayText
        if volumeLevel is None or volumeLevel < 0 or volumeLevel > 100:
            volumeLevel = 30
            
        # SoundTouch will fail the request if volume level is less than 10 or greater than 70.
        if volumeLevel > 0 and volumeLevel < 10:
            volumeLevel = 10  
        if volumeLevel > 70:
            volumeLevel = 70
        
        # replace sayText in the TTS url.
        ttsUrl = ttsUrl.format(saytext=urllib.parse.quote(sayText))
        
        # build playinfo configuration and the message to send.
        playInfo:PlayInfo = PlayInfo(ttsUrl, artist, album, track, volumeLevel, appKey)
        message = SoundTouchMessage(SoundTouchNodes.speaker, playInfo.ToXmlRequestBody())
        
        self.MakeRequest('POST', message)
        return message


    def PlayUrl(self, url:str, artist:str=None, album:str=None, track:str=None, 
                volumeLevel:int=0, appKey:str=None, getMetaDataFromUrlFile:bool=False
                ) -> SoundTouchMessage:
        """
        Plays media from the given URL.

        Args:
            url (str):
                The url to play.
            artist (str):
                The message text that will appear in the NowPlaying Artist node.  
                Default is "Unknown Artist"
            album (str):
                The message text that will appear in the NowPlaying Album node.  
                Default is "Unknown Album"
            track (str):
                The message text that will appear in the NowPlaying Track node.  
                Default is "Unknown Track"
            volumeLevel (int):
                The temporary volume level that will be used when the media is played.  
                Specify a value of zero to play at the current volume.  
                Default is zero.
            appKey (str):
                Bose Developer API application key.
            getMetaDataFromUrlFile (bool):
                If true, the artist, album, and song title metadata details will be retrieved
                from the ID3 header of the url content (if available); otherwise, False to
                use the artist, album, and song title arguments specified.

        Returns:                                
            A `SoundTouchMessage` object storing the request uri, a payload that has been 
            sent (optional), and the response as an `xml.etree.ElementTree.Element`.
            
        Raises:
            SoundTouchError:
                Url argument value does not start with 'http://' or 'https://'.  
                If the SoundTouch device encounters an error while trying to play the url
                media content.
                
        The given url content is played at the level specified by the volumeLevel argument.
        Specify a volumeLevel of zero to play the given url content at the current volume level.
        The volume level is restored to the level it was before the given url content was 
        played after play is complete; e.g. if you made changes to the volume while
        the given url content is playing then they are changed back to the volume level that was in
        effect prior to playing the given url content.  The SoundTouch device automatically takes 
        care of the volume level switching; there are no calls in the method to change the 
        volume or currently playing content status.
        
        The currently playing content (if any) is paused while the given url content
        is played, and then resumed once the given url content ends.  If the currently
        playing content is a url (or other "notification" source type), then the `MediaNextTrack`
        method will be called to stop the current play and the new source will be played.
        
        If the device is the master controller of a zone, then the given url content will 
        be played on all devices that are members of the zone.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/PlayUrl.py
        ```
        </details>
        """
        if (url is None) or (not isinstance(url, str)):
            _logsi.LogVerbose("A string url argument was not supplied; ignoring PlayUrl request")
            return
        url = url.lstrip()
        
        # only support http or https url's at this time.
        if not re.match(r'http[s]?://', url):
           raise SoundTouchError("url argument value does not start with 'http://' or 'https://'", logsi=_logsi)
       
        if artist is None:
            artist = "Unknown Artist"
        if album is None:
            album = "Unknown Album"
        if track is None:
            track = "Unknown Track"
        if volumeLevel is None or volumeLevel < 0 or volumeLevel > 100:
            volumeLevel = 30
            
        # retrieve nowPlaying status; if source is notification, then we must first
        # call MediaNextTrack command before trying to play the specified url; failure to
        # do so will result in the following error:
        # id=409, name="HTTP_STATUS_CONFLICT", cause="request not supported while speaker resource is in use"
        nowPlaying:NowPlayingStatus = self.GetNowPlayingStatus(True)
        if nowPlaying is not None:
            if nowPlaying.Source == SoundTouchSources.NOTIFICATION.value:
                self.MediaNextTrack()

        # do we need to retrieve metadata from the url file itself?
        if getMetaDataFromUrlFile == True:
            # try to retrieve the metadata; if found, then use it.
            metadata:TinyTag = self._GetMetadataFromUrl(url)
            if metadata is not None:
                artist = metadata.artist
                album = metadata.album
                track = metadata.title
                
                # retrieve cover art (if embedded).
                #coverArt = metadata.get_image()

        # build playinfo configuration and the message to send.
        playInfo:PlayInfo = PlayInfo(url, artist, album, track, volumeLevel, appKey)
        message = SoundTouchMessage(SoundTouchNodes.speaker, playInfo.ToXmlRequestBody())
        
        # make the request.
        self.MakeRequest('POST', message)
        return message
    
    
    def Power(self) -> None:
        """
        Toggle power on / off.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/Power.py
        ```
        </details>
        """
        self.Action(SoundTouchKeys.POWER, KeyStates.Both)


    def PowerOff(self, refresh: bool=True) -> None:
        """
        Set power off, if the device is currently powered on and not in standby mode.
        This will place the device into STANDBY power mode.
        
        Args:
            refresh (bool):
                True to check the real-time status of the device; otherwise, False
                to check the cached status of the device.  
                Default = True.
            
        This will first issue a `GetNowPlayingStatus()` method call to query the current status of the
        device.  If the refresh argument is True, then the status is refreshed with real-time
        data; otherwise the cached status is used.
        
        If the nowPlaying source is not "STANDBY", then the POWER key will be sent to power off
        the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/PowerOff.py
        ```
        </details>
        """
        stat:NowPlayingStatus = self.GetNowPlayingStatus(refresh)
        if (stat):
            if (stat.Source not in ["STANDBY", None]):
                self.Action(SoundTouchKeys.POWER, KeyStates.Both)


    def PowerOn(self, refresh: bool=True) -> None:
        """
        Set power on, if the device is currently in standby mode.
        
        Args:
            refresh (bool):
                True to check the real-time status of the device; otherwise, False
                to check the cached status of the device.  
                Default = True.
            
        This will first issue a `GetNowPlayingStatus()` method call to query the current status of the
        device.  If the refresh argument is True, then the status is refreshed with real-time
        data; otherwise the cached status is used.
        
        If the nowPlaying source is "STANDBY", then the POWER key will be sent to power on the device.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/PowerOn.py
        ```
        </details>
        """
        stat:NowPlayingStatus = self.GetNowPlayingStatus(refresh)
        if (stat):
            if (stat.Source in ["STANDBY", None]):
                self.Action(SoundTouchKeys.POWER, KeyStates.Both)


    def PowerStandby(self) -> None:
        """
        Set power to standby, if the device is currently powered on.
        
        This method does not update a configuration, as there is no object to
        configure - it simply places the device in STANDBY mode.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/PowerStandby.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.standby.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND % ("standby", self.Device.DeviceName))
        self.Get(SoundTouchNodes.standby)
        return
        

    def PowerStandbyLowPower(self) -> None:
        """
        Set power to low-power standby, if the device is currently powered on.
        
        This method does not update a configuration, as there is no object to
        configure - it simply places the device in low-power standby mode.
        
        Upon completion, the device will no longer respond to remote control commands
        nor to webservices api commands, as it is low-power mode.  You must physically
        hold down the power button on the device to turn it back on.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/PowerStandbyLowPower.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.lowPowerStandby.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND % ("lowPowerStandby", self.Device.DeviceName))
        self.Get(SoundTouchNodes.lowPowerStandby)
        return
        

    def Put(self, uri:SoundTouchUri, body:str, returnClassType=None) -> SoundTouchMessage:
        """
        Makes a POST request to apply a new value for the given node.

        Use this method when setting some configuration related data. All standard operations
        where a POST request is necessary are implemented by this class.

        Args:
            uri (SoundTouchUri):
                The node where the requested value is stored.
            body (SoundTouchModelRequest | str):
                The request body xml, or a class that inherits from `SoundTouchModelRequest`
                that implements the `ToXmlRequestBody` method.
            returnClassType (type):
                The configuration class type (e.g. NavigateResponse, etc) to return.
                Default is None; do not return a class type.

        Returns: 
            If the returnClassType argument is specified, then a new instance of the class
            type is returned with the parsed message response.  
            
            Otherwise, a `SoundTouchMessage` object storing the request uri, a payload that 
            has been sent (optional), and the response as an `xml.etree.ElementTree.Element`.

        Raises:
            SoundTouchError:
                When errors should not be ignored on this client, they will raise a SoundTouchError
                exception with all information related to that error.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/Put.py
        ```
        </details>
        """
        # if body implements SoundTouchModelRequest then call it's ToXmlRequestBody()
        # method to get the request body; otherwise, just assume it's xml already.
        reqBody:str = body
        if isinstance(body, SoundTouchModelRequest):
            reqBody = body.ToXmlRequestBody()

        # formulate the message, and make the request.
        msg = SoundTouchMessage(uri, reqBody)
        self.MakeRequest('POST', msg)
        
        # do we need to parse the response?  if so (and there is a response), then 
        # parse the response and return a new instance of the specified class type.
        if returnClassType is not None:
            if msg.Response is not None:
                return returnClassType(root=msg.Response)
            
        # otherwise, just return the message.
        return msg


    def RefreshConfiguration(self, uri:SoundTouchUri, classType) -> object:
        """        
        Refreshes the cached configuration for the given URI.
        
        Args:
            uri (SoundTouchUri):
                The configuration uri key.
            classType (type):
                The configuration class type (e.g. Balance, Volume, etc) to return.
            refresh (bool):
                True to refresh the property with real-time information from the device;
                otherwise, False to just return the cached value.
                
        Returns:
            A configuration instance of the provided classType argument.

        This method will call the `Get()` method to refresh the configuration with
        real-time information from the device, and store the results in the cache.
        """
        if _logsi.IsOn(SILevel.Verbose):
            _logsi.LogVerbose("Refreshing '%s' configuration from the SoundTouch device" % (str(uri)))
        
        msg = self.Get(uri)
        if msg.Response is not None:
            self[uri] = classType(root=msg.Response)
            
        return self[uri]


    def RemoveAllPresets(self) -> PresetList:
        """
        Removes all presets from the device's list of presets.
        
        Returns:
            A `PresetList` object that contains the updated preset list configuration of the device.
            
        Raises:
            Exception:
                If the command fails for any reason.
        
        A `GetPresetList()` method call is made to retrieve the current list of presets.
        The returned list of presets are deleted one by one.  

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/RemoveAllPresets.py
        ```
        </details>
        """
        _logsi.LogVerbose("Removing all presets from SoundTouch device: '%s'" % self.Device.DeviceName)

        # get current list of presets.
        presets:PresetList = self.GetPresetList(True)
        
        # remove them all.
        presetList:PresetList = PresetList()
        preset:Preset
        for preset in presets:
            presetList = self.Put(SoundTouchNodes.removePreset, preset, PresetList)

        # update configuration cache with the updated list.
        if isinstance(presetList, PresetList):
            self[SoundTouchNodes.presets] = presetList
            
        return presetList


    def RemoveFavorite(self) -> None:
        """ 
        Removes the currently playing media from the device favorites.
        
        This will first make a call to `GetNowPlayingStatus()` method to ensure
        favorites are enabled for the now playing media.  If not enabled, then
        the request is ignored and no exception is raised.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/RemoveFavorite.py
        ```
        </details>
        """
        # get current nowPlaying status.
        nowPlaying:NowPlayingStatus = self.GetNowPlayingStatus(True)

        # can the nowPlaying item be a favorite?
        if nowPlaying.IsFavoriteEnabled:
            self.Action(SoundTouchKeys.REMOVE_FAVORITE, KeyStates.Press)
        else:
            _logsi.LogVerbose(MSG_TRACE_FAVORITE_NOT_ENABLED % nowPlaying.ToString())


    def RemoveGroupStereoPair(self) -> SoundTouchMessage:
        """
        Removes an existing left / right stereo pair speaker group.
        
        Args:
            group (Group):
                Speaker group configuration object that defines the group.  
                
        Raises:
            SoundTouchError:
                If SoundTouch WebService call fails for any reason.
                
        The device that issues the call to this method has to be the master of the group,
        or the service will fail.
        
        The device will generate a `groupUpdated` websocket event, which contains the 
        updated `Group` configuration.

        The ST-10 is the only SoundTouch product that supports stereo pair groups.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/RemoveGroupStereoPair.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.removeGroup.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        return self.Get(SoundTouchNodes.removeGroup)


    def RemoveMusicServiceAccount(self, source:str, displayName:str, userAccount:str, password:str=None
                                 ) -> SoundTouchMessage:
        """
        Removes an existing music service account from the sources list.

        Args:
            source (str):
                Account source value (e.g. "STORED_MUSIC", "SPOTIFY", "AMAZON", etc).
            displayName (str):
                Account display name that appears in UI's.
            userAccount (str):
                User account value used to authenticate to the service.
            password (str):
                Password value used to authenticate to the service.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/RemoveMusicServiceAccount.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.removeMusicServiceAccount.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("removeMusicServiceAccount", userAccount, self.Device.DeviceName))
        request:MusicServiceAccount = MusicServiceAccount(source, displayName, userAccount, password)
        _logsi.LogVerbose("'%s': Account details - %s" % (self.Device.DeviceName, request.ToString()))
        msg:SoundTouchMessage = self.Put(SoundTouchNodes.removeMusicServiceAccount, request)
        return msg


    def RemoveMusicServiceStation(self, removeStation:RemoveStation) -> SoundTouchMessage:
        """
        Removes a station from a music service (e.g. PANDORA, etc) collection of previously 
        stored stations.
        
        Args:
            removeStation (RemoveStation):
                Criteria used to remove the music service station.

        Returns:
            A `SoundTouchMessage` object that contains the response.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `removeStation` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Playing will be stopped and the NowPlaying status will be updated with source="INVALID_SOURCE"
        if the station being removed is currently playing; otherwise, currently playing content
        is not changed.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/RemoveMusicServiceStation.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.removeStation.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("removeStation", removeStation.ToString(), self.Device.DeviceName))
        result:SoundTouchMessage = self.Put(SoundTouchNodes.removeStation, removeStation)
        return result


    def RemovePreset(self, presetId: int) -> PresetList:
        """
        Removes the specified Preset id from the device's list of presets.
        
        Args:
            presetId (int):
                The preset id to remove; valid values are 1 thru 6.
                
        Returns:
            A `PresetList` object that contains the updated preset list configuration of the device.
            
        Raises:
            Exception:
                If the command fails for any reason.
        
        The preset with the specified id is removed.  
        No exception is raised if the preset id does not exist.
        
        Presets and favorites in the SoundTouch app are not reordered once the
        preset is removed; it simply creates an open / empty slot in the list.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/RemovePreset.py
        ```
        </details>
        """
        _logsi.LogVerbose("Removing preset from SoundTouch device: '%s'" % self.Device.DeviceName)
        item:Preset = Preset(presetId)
        presetList:PresetList = self.Put(SoundTouchNodes.removePreset, item, PresetList)
        
        # update configuration cache with the updated list.
        if isinstance(presetList, PresetList):
            self[SoundTouchNodes.presets] = presetList
        return presetList


    def RemoveZone(self, delay:int=1) -> SoundTouchMessage:
        """
        Removes the given zone.
        
        Args:
            delay (int):
                Time delay (in seconds) to wait AFTER removing zone members.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 1; value range is 0 - 10.
                
        Raises:
            SoundTouchError:
                Master zone status could not be retrieved.  
                Master zone does not exist; zone members cannot be removed.  
        
        This method retrieves the current master zone status, and issues a call to
        `RemoveZoneMembers` to remove all members from the zone.  
        
        Note that the master zone itself is also removed; you will need to 
        reissue a call to the `CreateZone()` method to re-create the master zone.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/RemoveZone.py
        ```
        </details>
        """
        # validations.
        delay = self._ValidateDelay(delay, 1, 10)
        
        # get master zone status.
        # we do this to retrieve the master zone device id and its zone members.
        masterZone:Zone = self.GetZoneStatus(refresh=True)
        if masterZone is None:
            raise SoundTouchError('Master zone status could not be retrieved', logsi=_logsi)
        if len(masterZone.Members) == 0:
            raise SoundTouchError('Master zone does not exist; zone members cannot be removed', logsi=_logsi)
        
        _logsi.LogVerbose("Removing zone members from SoundTouch device: '%s' - %s" % (
            self.Device.DeviceName, masterZone.ToStringMemberSummary()))
        
        # remove the member zones from the device.
        result = self.Put(SoundTouchNodes.removeZoneSlave, masterZone.ToXmlString())

        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)

        return result


    def RemoveZoneMembers(self, members:list, delay:int=3) -> SoundTouchMessage:
        """
        Removes the given zone members from the device's zone.
        
        Args:
            members (list):
                A list of `ZoneMember` objects to remove from the master zone.
            delay (int):
                Time delay (in seconds) to wait AFTER removing zone members.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 3; value range is 0 - 10.
                
        Raises:
            SoundTouchError:
                Master zone status could not be retrieved.  
                Master zone does not exist; zone members cannot be removed.  
                Members argument was not supplied, or has no members.  
                Members argument contained a list item that is not of type `ZoneMember`.  
        
        This method must be called by the master device of an existing zone; only the
        master can remove zone members.

        Note that the master zone itself is also removed if there are no zone members
        left after the remove request is complete.  In this case, you will need to 
        reissue a call to the `CreateZone()` method to re-create the master zone.
        
        The SoundTouch device does not return errors if a zone member device id does not
        exist; it simply ignores the invalid member entry and moves on to the next.
               
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/RemoveZoneMembers.py
        ```
        </details>
        """
        # validations.
        if not members or len(members) == 0:
            raise SoundTouchError('Members argument contained no zone members to remove', logsi=_logsi)
        delay = self._ValidateDelay(delay, 5, 10)
        
        # get master zone status.
        # we do this to retrieve the master zone device id.
        masterZone:Zone = self.GetZoneStatus(refresh=True)
        if masterZone is None:
            raise SoundTouchError('Master zone status could not be retrieved', logsi=_logsi)
        if len(masterZone.Members) == 0:
            raise SoundTouchError('Master zone does not exist; zone members cannot be removed', logsi=_logsi)
        
        # create a temporary Zone object (used to remove zone members)
        # and add the zone members that we want to remove.
        tempZone:Zone = Zone(masterZone.MasterDeviceId)
        for member in members:
            tempZone.AddMember(member, _logsi)

        _logsi.LogVerbose("Removing zone members from SoundTouch device: '%s' - %s" % (
            self.Device.DeviceName, tempZone.ToStringMemberSummary()))

        # remove the member zones from the device.
        result = self.Put(SoundTouchNodes.removeZoneSlave, tempZone.ToXmlString())

        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)

        return result


    def RestoreSnapshot(self, delay:int = 5) -> None:
        """
        Restores selected portions of the configuration from a snapshot that was
        previously taken with the `StoreSnapshot` method.
        
        Args:
            delay (int):
                Time delay (in seconds) to wait for the playing content to change.  
                Default is 5 seconds.
        
        The following settings will be restored from the snapshot dictionary by default:
        - `SoundTouchNodes.nowPlaying.Path` - playing content.  
        - `SoundTouchNodes.volume.Path` - volume level and mute status.
        
        No restore actions will be taken if snapshot settings do not exist.
        
        You can restore your own custom settings from the snapshot dictionary; note
        that these custom settings are NOT restored by default.
        
        You may remove default items from the snapshot dictionary prior to calling
        the `RestoreSnapshot` method.  Let's say you did not want to restore the
        volume level - simply remove the volume item from the snapshot dictionary.
        See the sample code below for an example.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/StoreSnapshot.py
        ```
        </details>
        """
        if len(self._SnapshotSettings) == 0:
            _logsi.LogMessage("No snapshot has been taken yet; nothing to do")
            return
        
        if SoundTouchNodes.nowPlaying.Path in self._SnapshotSettings.keys():
            currentStatus:NowPlayingStatus = self.GetNowPlayingStatus(True)
            status:NowPlayingStatus = self._SnapshotSettings[SoundTouchNodes.nowPlaying.Path]
            # switch the input source if need be, waiting 2 seconds for the change to process.
            if currentStatus.Source != status.Source:
                self.SelectSource(status.Source, status.ContentItem.SourceAccount, 2)
            self.SelectContentItem(status.ContentItem, delay)
        
        if SoundTouchNodes.volume.Path in self._SnapshotSettings.keys():
            # set volume level also restores mute / unmute status.
            volume:Volume = self._SnapshotSettings[SoundTouchNodes.volume.Path]
            self.SetVolumeLevel(volume.Actual)
            
        return


    def SearchMusicLibrary(self, search:Search) -> SearchResponse:
        """
        Searches a specified music library container (e.g. STORED_MUSIC, etc).
        
        Args:
            search (Navigate):
                Criteria used to search the music library.

        Returns:
            A `SearchResponse` object that contains the response.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `search` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Use the `GetSourceList` method to get the `source` and `sourceAccount` values for 
        the specific NAS Music Library you wish to navigate.
                
        A returned `SearchResponse` item can be used to play the item's media content by 
        passing its `ContentItem` value to the `PlayContentItem` method.

        You must pay close attention to the `filter` attribute on the `SearchTerm` node, 
        as the SoundTouch webservices API is very picky on what filter types are allowed 
        for a container.  

        The `StartItem` node is required; otherwise, the search fails.

        Music library containers can found using the `GetMusicLibraryItems` method.  Use 
        a returned `NavigateResponse` item's `ContentItem` node in the request.

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SearchMusicLibrary.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.search.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("search", search.ContainerTitle, self.Device.DeviceName))
        result:SearchResponse = self.Put(SoundTouchNodes.search, search, SearchResponse)
        return result


    def SearchMusicServiceStations(self, searchStation:SearchStation) -> SearchStationResults:
        """
        Searches a music service (e.g. PANDORA, etc) for stations that can be added to
        a users collection of stations.
        
        Args:
            searchStation (SearchStation):
                Criteria used to search a music service for available stations.

        Returns:
            A `SoundTouchMessage` object that contains the response.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `searchStation` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        The `AddMusicServiceStation` method can be used to add a result item (song or artist)
        from the results of this method.
        
        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SearchMusicServiceStations.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.searchStation.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("searchStation", searchStation.ToString(), self.Device.DeviceName))
        result:SoundTouchMessage = self.Put(SoundTouchNodes.searchStation, searchStation, SearchStationResults)
        return result


    def SelectContentItem(self, item:ContentItem, delay:int=5) -> SoundTouchMessage:
        """
        Selects the given ContentItem.

        Args:
            item (ContentItem):
                Content item to select.
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the content item.  
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 5; value range is 0 - 10.
                
        Note that playing of "https://" content is not supported by SoundTouch devices.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectContentItem.py
        ```
        </details>
        """
        _logsi.LogObject(SILevel.Verbose, "Select content item", item)
        delay = self._ValidateDelay(delay, 5, 10)
            
        result = self.Put(SoundTouchNodes.select, item)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)
            
        return result


    def SelectLastSoundTouchSource(self, delay:int=3) -> SoundTouchMessage:
        """
        Selects the last SoundTouch source that was selected.
        
        Args:
            delay (int):
                time delay (in seconds) to wait AFTER selecting the source.  This delay
                will give the SoundTouch device time to process the change before another 
                command is accepted.  
                Default is 3 seconds, and value range is 0 - 10.
                
        Returns:
            A SoundTouchMessage response that indicates success or failure of the command.
            
        Raises:
            SoundTouchError:
                If the device is not capable of supporting `selectLastSoundTouchSource` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectLastSoundTouchSource.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.selectLocalSource.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND % ("selectLastSoundTouchSource", self.Device.DeviceName))
        delay = self._ValidateDelay(delay, 5, 10)
        msg = self.Get(SoundTouchNodes.selectLastSoundTouchSource)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)
            
        return msg


    def SelectLastSource(self, delay:int=3) -> SoundTouchMessage:
        """
        Selects the last source that was selected.
        
        Args:
            delay (int):
                time delay (in seconds) to wait AFTER selecting the source.  This delay
                will give the SoundTouch device time to process the change before another 
                command is accepted.  
                Default is 3 seconds, and value range is 0 - 10.
                
        Returns:
            A SoundTouchMessage response that indicates success or failure of the command.
            
        Raises:
            SoundTouchError:
                If the device is not capable of supporting `selectLastSource` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectLastSource.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.selectLocalSource.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND % ("selectLastSource", self.Device.DeviceName))
        delay = self._ValidateDelay(delay, 5, 10)
        msg = self.Get(SoundTouchNodes.selectLastSource)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)
            
        return msg


    def SelectLastWifiSource(self, delay:int=3) -> SoundTouchMessage:
        """
        Selects the last wifi source that was selected.
        
        Args:
            delay (int):
                time delay (in seconds) to wait AFTER selecting the source.  This delay
                will give the SoundTouch device time to process the change before another 
                command is accepted.  
                Default is 3 seconds, and value range is 0 - 10.
                
        Returns:
            A SoundTouchMessage response that indicates success or failure of the command.
            
        Raises:
            SoundTouchError:
                If the device is not capable of supporting `selectLastWiFiSource` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectLastWifiSource.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.selectLastWiFiSource.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND % ("selectLastWiFiSource", self.Device.DeviceName))
        delay = self._ValidateDelay(delay, 5, 10)
        msg = self.Get(SoundTouchNodes.selectLastWiFiSource)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)
            
        return msg


    def SelectLocalSource(self, delay:int=3) -> SoundTouchMessage:
        """
        Selects the LOCAL source;  for some SoundTouch devices, this is the only way 
        that the LOCAL source can be selected.
        
        Args:
            delay (int):
                time delay (in seconds) to wait AFTER selecting the source.  This delay
                will give the SoundTouch device time to process the change before another 
                command is accepted.  
                Default is 3 seconds, and value range is 0 - 10.
                
        Returns:
            A SoundTouchMessage response that indicates success or failure of the command.
            
        Raises:
            SoundTouchError:
                If the device is not capable of supporting `selectLocalSource` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  

        Note that some SoundTouch devices do not support this functionality.  This method will 
        first query the device supportedUris to determine if it supports the function; if so, 
        then the request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectLocalSource.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.selectLocalSource.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND % ("selectLocalSource", self.Device.DeviceName))
        delay = self._ValidateDelay(delay, 5, 10)
        msg = self.Get(SoundTouchNodes.selectLocalSource)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)
            
        return msg


    def SelectPreset(self, preset:Preset, delay:int=5) -> SoundTouchMessage:
        """
        Selects the given preset.

        Args:
            item (Preset):
                Preset item to select.
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the preset.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 5; value range is 0 - 10.

        Raises:
            SoundTouchError:
                Preset argument was not supplied.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectPreset.py
        ```
        </details>
        """
        _logsi.LogVerbose("Selecting preset on SoundTouch device: '%s'" % self.Device.DeviceName)
        
        if not preset:
            raise SoundTouchError('Preset argument was not supplied', logsi=_logsi)
        delay = self._ValidateDelay(delay, 5, 10)
        
        result = self.Put(SoundTouchNodes.select, preset.ContentItem)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)
            
        return result


    def SelectPreset1(self, delay:int=3) -> None:
        """ 
        Selects pre-defined preset number 1 on the device.
        
        Args:
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the preset.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 3; value range is 0 - 10.

        This method does nothing if there is no preset at the specified preset index.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectPreset1.py
        ```
        </details>
        """
        delay = self._ValidateDelay(delay, 3, 10)
        self.Action(SoundTouchKeys.PRESET_1, KeyStates.Release)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)


    def SelectPreset2(self, delay:int=3) -> None:
        """ 
        Selects pre-defined preset number 2 on the device.
        
        Args:
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the preset.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 3; value range is 0 - 10.

        This method does nothing if there is no preset at the specified preset index.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectPreset2.py
        ```
        </details>
        """
        delay = self._ValidateDelay(delay, 3, 10)
        self.Action(SoundTouchKeys.PRESET_2, KeyStates.Release)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)


    def SelectPreset3(self, delay:int=3) -> None:
        """ 
        Selects pre-defined preset number 3 on the device.
        
        Args:
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the preset.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 3; value range is 0 - 10.

        This method does nothing if there is no preset at the specified preset index.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectPreset3.py
        ```
        </details>
        """
        delay = self._ValidateDelay(delay, 3, 10)
        self.Action(SoundTouchKeys.PRESET_3, KeyStates.Release)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)


    def SelectPreset4(self, delay:int=3) -> None:
        """ 
        Selects pre-defined preset number 4 on the device.
        
        Args:
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the preset.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 3; value range is 0 - 10.

        This method does nothing if there is no preset at the specified preset index.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectPreset4.py
        ```
        </details>
        """
        delay = self._ValidateDelay(delay, 3, 10)
        self.Action(SoundTouchKeys.PRESET_4, KeyStates.Release)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)


    def SelectPreset5(self, delay:int=3) -> None:
        """ 
        Selects pre-defined preset number 5 on the device.
        
        Args:
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the preset.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 3; value range is 0 - 10.

        This method does nothing if there is no preset at the specified preset index.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectPreset5.py
        ```
        </details>
        """
        delay = self._ValidateDelay(delay, 3, 10)
        self.Action(SoundTouchKeys.PRESET_5, KeyStates.Release)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)


    def SelectPreset6(self, delay:int=3) -> None:
        """ 
        Selects pre-defined preset number 6 on the device.
        
        Args:
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the preset.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 3; value range is 0 - 10.

        This method does nothing if there is no preset at the specified preset index.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectPreset6.py
        ```
        </details>
        """
        delay = self._ValidateDelay(delay, 3, 10)
        self.Action(SoundTouchKeys.PRESET_6, KeyStates.Release)
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)


    def SelectRecent(self, recent:Recent, delay:int=5) -> SoundTouchMessage:
        """
        Selects the given recent.

        Args:
            item (Recent):
                Recent item to select.
            delay (int):
                Time delay (in seconds) to wait AFTER selecting the recent.
                This delay will give the device time to process the change before another 
                command is accepted.  
                Default is 5; value range is 0 - 10.

        Raises:
            SoundTouchError:
                Recent argument was not supplied.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectRecent.py
        ```
        </details>
        """
        _logsi.LogVerbose("Selecting recent on SoundTouch device: '%s'" % self.Device.DeviceName)
        
        if not recent:
            raise SoundTouchError('Recent argument was not supplied', logsi=_logsi)
        delay = self._ValidateDelay(delay, 5, 10)
        
        result = self.Put(SoundTouchNodes.select, recent.ContentItem.ToXmlRequestBody())
        
        if delay > 0:
            _logsi.LogVerbose(MSG_TRACE_DELAY_DEVICE % (delay, self.Device.DeviceName))
            time.sleep(delay)
            
        return result


    def SelectSource(self, source:SoundTouchSources, sourceAccount:str=None, delay:int=3) -> SoundTouchMessage:
        """
        Selects a new input source.
        
        Args:
            source (SoundTouchSources | str):
                Input source value; this can either be a `SoundTouchSources` enum value or a string.
                If specifying a string value, then it should be in upper-case.
            sourceAccount (str):
                Source account value; some sources require one when changing the input 
                source (e.g. "AUX").
            delay (int):
                time delay (in seconds) to wait AFTER selecting the source.  This delay
                will give the SoundTouch device time to process the change before another 
                command is accepted.
                default is 3 seconds, and value range is 0 - 10.
                
        Returns:
            A SoundTouchMessage response that indicates success or failure of the command.
            
        Raises:
            SoundTouchError:
                Source argument was not supplied.  

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SelectSource.py
        ```
        </details>
        """
        if not source:
            raise SoundTouchError('Source argument was not supplied', logsi=_logsi)
        if isinstance(source, SoundTouchSources):
            source = source.value
        return self.SelectContentItem(ContentItem(source=source, sourceAccount=sourceAccount), delay)


    def SetAudioDspControls(self, controls:AudioDspControls) -> SoundTouchMessage:
        """
        Sets the current audio dsp controls configuration of the device.
        
        Args:
            controls (AudioDspControls):
                A `AudioDspControls` object that contains audio dsp control
                values to set.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `audiodspcontrols` functions,
                as determined by a query to the cached `supportedURLs` web-services api.  
                
        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetAudioDspControls.py
        ```
        </details>
        """
        # validations.
        if (controls is None) or (not isinstance(controls, AudioDspControls)):
            raise SoundTouchError('controls argument was not supplied, or is not of type AudioDspControls', logsi=_logsi)
            
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.audiodspcontrols.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE % ("audio dsp controls", controls.ToString(), self.Device.DeviceName))
        request:AudioDspControls = controls
        return self.Put(SoundTouchNodes.audiodspcontrols, request)


    def SetAudioProductLevelControls(self, controls:AudioProductLevelControls) -> SoundTouchMessage:
        """
        Sets the current audio product tone controls configuration of the device.

        Args:
            controls (AudioProductLevelControls):
                A `AudioProductLevelControls` object that contains audio product tone control
                values to set.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `audioproductlevelcontrols` functions,
                as determined by a query to the cached `supportedURLs` web-services api.    
                If the controls argument is None, or not of type `AudioProductLevelControls`.
                
        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetAudioProductLevelControls.py
        ```
        </details>
        """
        # validations.
        if (controls is None) or (not isinstance(controls, AudioProductLevelControls)):
            raise SoundTouchError('controls argument was not supplied, or is not of type AudioProductLevelControls', logsi=_logsi)
            
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.audioproductlevelcontrols.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE % ("audio product level controls", controls.ToString(), self.Device.DeviceName))
        request:AudioProductLevelControls = controls
        return self.Put(SoundTouchNodes.audioproductlevelcontrols, request)


    def SetAudioProductToneControls(self, controls:AudioProductToneControls) -> SoundTouchMessage:
        """
        Sets the current audio product tone controls configuration of the device.

        Args:
            controls (AudioProductToneControls):
                A `AudioProductToneControls` object that contains audio product tone control
                values to set.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `audioproducttonecontrols` functions,
                as determined by a query to the cached `supportedURLs` web-services api.    
                If the controls argument is None, or not of type `AudioProductToneControls`.
                
        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetAudioProductToneControls.py
        ```
        </details>
        """
        # validations.
        if (controls is None) or (not isinstance(controls, AudioProductToneControls)):
            raise SoundTouchError('controls argument was not supplied, or is not of type AudioProductToneControls', logsi=_logsi)
            
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.audioproducttonecontrols.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE % ("audio product tone controls", controls.ToString(), self.Device.DeviceName))
        request:AudioProductToneControls = controls
        return self.Put(SoundTouchNodes.audioproducttonecontrols, request)


    def SetBalanceLevel(self, level:int) -> SoundTouchMessage:
        """
        Sets the device balance level to the given level.  
        
        Args:
            level (int):
                Balance level to set, usually in the range of -7 (left) to 7 (right).

        This method only works if the device is configured as part of a stereo pair.
        
        The argument level range can vary by device; use the `GetBalance` method to
        determine if the device has the capability to adjust the balance, as well as
        the allowable range (minimum, maximum, default) levels.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetBalanceLevel.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.balance.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE % ("balance level", str(level), self.Device.DeviceName))
        request:Balance = Balance(level)
        return self.Put(SoundTouchNodes.balance, request)


    def SetBassLevel(self, level:int) -> SoundTouchMessage:
        """
        Sets the device bass level to the given level.
        
        Args:
            level (int):
                Bass level to set, usually in the range of -9 (no bass) to 0 (full bass).

        The argument level range can vary by device; use the `GetBassCapabilities()` method to
        retrieve the allowable range for a device.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetBassLevel.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.bass.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE % ("bass level", str(level), self.Device.DeviceName))
        request:Bass = Bass(level)
        return self.Put(SoundTouchNodes.bass, request)


    def SetMusicServiceAccount(self, source:str, displayName:str, userAccount:str, password:str=None
                               ) -> SoundTouchMessage:
        """
        Adds a music service account to the sources list.

        Args:
            source (str):
                Account source value (e.g. "STORED_MUSIC", "SPOTIFY", "AMAZON", etc).
            displayName (str):
                Account display name that appears in UI's.
            userAccount (str):
                User account value used to authenticate to the service.  This value must exactly
                match (case-sensitive) the media server id in the `MediaServer` instance.
            password (str):
                Password value used to authenticate to the service.

        UPnP media server music service (e.g. "STORED_MUSIC") sources can only be set if the
        device has detected the UPnP media server.  The detected UPnP media servers will appear
        in the `MediaServerList` of items obtained using a call to `GetMediaServerList` method.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetMusicServiceAccount.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.setMusicServiceAccount.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("setMusicServiceAccount", userAccount, self.Device.DeviceName))
        request:MusicServiceAccount = MusicServiceAccount(source, displayName, userAccount, password)
        _logsi.LogVerbose("'%s': Account details - %s" % (self.Device.DeviceName, request.ToString()))
        msg:SoundTouchMessage = self.Put(SoundTouchNodes.setMusicServiceAccount, request)
        return msg


    def SetName(self, name:str) -> SoundTouchMessage:
        """
        Sets a new device name.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetName.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE % ("device name", name, self.Device.DeviceName))
        
        # update the device configuration.
        request:SimpleConfig = SimpleConfig('name', name)
        result:SoundTouchMessage = self.Put(SoundTouchNodes.name, request)
    
        # update the SoundTouchDevice info configuration device name to match.
        self.Device._Information._DeviceName = name
        return result


    def SetProductCecHdmiControl(self, control:ProductCecHdmiControl) -> SoundTouchMessage:
        """
        Sets the current product cec hdmi control configuration of the device.

        Args:
            control (ProductCecHdmiControl):
                A `ProductCecHdmiControl` object that contains product cec hdmi control
                values to set.

        Raises:
            SoundTouchError:
                If the device is not capable of supporting `productcechdmicontrol` functions,
                as determined by a query to the cached `supportedURLs` web-services api.    
                If the control argument is None, or not of type `ProductCecHdmiControl`.
                
        Note that some SoundTouch devices do not support this functionality.  For example,
        the ST-300 will support this, but the ST-10 will not.  This method will first query
        the device supportedUris to determine if it supports the function; if so, then the
        request is made to the device; if not, then a `SoundTouchError` is raised.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetProductCecHdmiControl.py
        ```
        </details>
        """
        # validations.
        if (control is None) or (not isinstance(control, ProductCecHdmiControl)):
            raise SoundTouchError('control argument was not supplied, or is not of type ProductCecHdmiControl', logsi=_logsi)
            
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.productcechdmicontrol.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE % ("product cec hdmi control", control.ToString(), self.Device.DeviceName))
        request:ProductCecHdmiControl = control
        return self.Put(SoundTouchNodes.productcechdmicontrol, request)


    def SetUserPlayControl(self, userPlayControlType:UserPlayControlTypes) -> SoundTouchMessage:
        """
        Sends a user play control type command to stop / pause / play / resume media content playback.
        
        Args:
            userPlayControlType (UserPlayControlTypes):
                User play control type to send.

        Raises:
            SoundTouchError:  
                userPlayControlType argument was not supplied, or not of type UserPlayControlTypes.  
                
        No exception is raised if the device is currently in standby mode.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetUserPlayControl.py
        ```
        </details>
        """
        # validations.
        if (userPlayControlType is None) or (not isinstance(userPlayControlType, UserPlayControlTypes)):
            raise SoundTouchError('userPlayControlType argument was not supplied, or is not of type UserPlayControlTypes', logsi=_logsi)
            
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.userPlayControl.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)
        
        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("userPlayControl", userPlayControlType.value, self.Device.DeviceName))
        userPlayControl:UserPlayControl = UserPlayControl(userPlayControlType)
        return self.Put(SoundTouchNodes.userPlayControl, userPlayControl)


    def SetUserRating(self, ratingType:UserRatingTypes) -> SoundTouchMessage:
        """
        Rates the currently playing media, if ratings are supported.
        
        Args:
            ratingType (UserRatingTypes):
                Rating to assign.

        Raises:
            SoundTouchError:  
                rating argument was not supplied, or not of type UserRatingTypes.  
                
        No exception is raised if the device is currently in standby mode.
                
        No exception is raised if the NowPlaying content does not support ratings.
        Check the `NowPlayingStatus.IsRatingEnabled` property to determine if the
        content supports ratings or not.
                
        PANDORA is currently the only source that supports ratings.  Ratings are stored 
        in the artist profile under "My Collection" settings.  If a ThumbsDown rating is 
        assigned, then the current track play will stop and advance to the next track.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetUserRating.py
        ```
        </details>
        """
        # validations.
        if (ratingType is None) or (not isinstance(ratingType, UserRatingTypes)):
            raise SoundTouchError('ratingType argument was not supplied, or is not of type UserRatingTypes', logsi=_logsi)
            
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.userRating.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)
        
        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("userRating", ratingType.value, self.Device.DeviceName))
        userRating:UserRating = UserRating(ratingType)
        return self.Put(SoundTouchNodes.userRating, userRating)


    def SetUserTrackControl(self, userTrackControlType:UserTrackControlTypes) -> SoundTouchMessage:
        """
        Sends a user track control type command to control track playback (next, previous, repeat, 
        shuffle, etc).
        
        Args:
            userTrackControlType (UserTrackControlTypes):
                User track control type to send.

        Raises:
            SoundTouchError:  
                userTrackControlType argument was not supplied, or not of type UserTrackControlTypes.  
                
        No exception is raised if the device is currently in standby mode.
                
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetUserTrackControl.py
        ```
        </details>
        """
        # validations.
        if (userTrackControlType is None) or (not isinstance(userTrackControlType, UserTrackControlTypes)):
            raise SoundTouchError('userTrackControlType argument was not supplied, or is not of type UserTrackControlTypes', logsi=_logsi)
            
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.userTrackControl.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)
        
        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("userTrackControl", userTrackControlType.value, self.Device.DeviceName))
        userTrackControl:UserTrackControl = UserTrackControl(userTrackControlType)
        return self.Put(SoundTouchNodes.userTrackControl, userTrackControl)


    def SetVolumeLevel(self, level:int) -> SoundTouchMessage:
        """
        Sets the device volume level to the given level.
        
        Args:
            level (int):
                Volume level to set, in the range of 0 (mute) to 100 (full volume).

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/SetVolumeLevel.py
        ```
        </details>
        """
        _logsi.LogVerbose(MSG_TRACE_SET_PROPERTY_VALUE_SIMPLE % ("volume level", str(level), self.Device.DeviceName))
        request:Volume = Volume(level, level)
        return self.Put(SoundTouchNodes.volume, request)


    def StorePreset(self, item:Preset) -> PresetList:
        """
        Stores the given Preset to the device's list of presets.
        
        Args:
            item (Preset):
                The Preset object to store.
                
        Returns:
            A `PresetList` object that contains the updated preset list configuration of the device.
            
        Raises:
            Exception:
                If the command fails for any reason.
                
        Most SoundTouch devices can only store 6 presets in their internal memory.
        The Preset.preset_id property controls what slot the stored preset gets
        placed in.  If a preset already exists in a slot, then it is over-written
        with the newly stored preset.  If a preset with the same details exists in
        another slot, then the duplicate preset is removed and its slot is emptied.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/StorePreset.py
        ```
        </details>
        """
        if isinstance(item, Preset):
            # if create or update date not set then set it.
            if item.CreatedOn is None or item.CreatedOn == 0:
                item.CreatedOn = int(round(datetime.now().timestamp()))
            if item.UpdatedOn is None or item.UpdatedOn == 0:
                item.UpdatedOn = int(round(datetime.now().timestamp()))
                
        _logsi.LogVerbose("Storing preset to SoundTouch device: '%s'" % self.Device.DeviceName)
        presetList:PresetList = self.Put(SoundTouchNodes.storePreset, item, PresetList)
        
        # update configuration cache with the updated list.
        if isinstance(presetList, PresetList):
            self[SoundTouchNodes.presets] = presetList
        return presetList


    def StoreSnapshot(self) -> None:
        """
        Stores selected portions of the configuration so that they can be easily
        restored with the `RestoreSnapshot` method.
        
        The following settings will be stored to the snapshot dictionary by default:
        - `SoundTouchNodes.nowPlaying.Path` - playing content.  
        - `SoundTouchNodes.volume.Path` - volume level and mute status.
        
        The `SnapshotSettings` dictionary is cleared prior to storing any settings.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/StoreSnapshot.py
        ```
        </details>
        """
        self._SnapshotSettings.clear()
               
        status:NowPlayingStatus = self.GetNowPlayingStatus(True)
        self._SnapshotSettings[SoundTouchNodes.nowPlaying.Path] = status
        
        volume:Volume = self.GetVolume(True)
        self._SnapshotSettings[SoundTouchNodes.volume.Path] = volume
        return


    def ThumbsDown(self) -> None:
        """ 
        Sets a thumbs down rating for the currently playing media.
        
        This will first make a call to `GetNowPlayingStatus()` method to ensure
        ratings are enabled for the now playing media.  If not enabled, then
        the request is ignored and no exception is raised.
        
        Note that this method should only be used with source music services
        that support ratings (e.g. PANDORA, SPOTIFY, etc). The rating value is
        actually stored with the music service, and is not located on the SoundTouch
        device itself.
        
        Note that for some music services (e.g. PANDORA), the now playing
        selection will change immediately once this method processing completes;
        there is no code in this API that forces the change.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/ThumbsDown.py
        ```
        </details>
        """
        # get current nowPlaying status.
        nowPlaying:NowPlayingStatus = self.GetNowPlayingStatus(True)

        # can the nowPlaying item be rated?
        if nowPlaying.IsRatingEnabled:
            self.Action(SoundTouchKeys.THUMBS_DOWN, KeyStates.Press)
        else:
            _logsi.LogVerbose(MSG_TRACE_RATING_NOT_ENABLED % nowPlaying.ToString())


    def ThumbsUp(self) -> None:
        """ 
        Sets a thumbs up rating for the currently playing media.

        This will first make a call to `GetNowPlayingStatus()` method to ensure
        ratings are enabled for the now playing media.  If not enabled, then
        the request is ignored and no exception is raised.
        
        Note that this method should only be used with source music services
        that support ratings (e.g. PANDORA, SPOTIFY, etc). The rating value is
        actually stored with the music service, and is not located on the SoundTouch
        device itself.
        
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/ThumbsUp.py
        ```
        </details>
        """
        # get current nowPlaying status.
        nowPlaying:NowPlayingStatus = self.GetNowPlayingStatus(True)

        # can the nowPlaying item be rated?
        if nowPlaying.IsRatingEnabled:
            self.Action(SoundTouchKeys.THUMBS_UP, KeyStates.Press)
        else:
            _logsi.LogVerbose(MSG_TRACE_RATING_NOT_ENABLED % nowPlaying.ToString())


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchClient:'
        if self._Device is not None:
            msg = "%s DeviceName='%s'" % (msg, self.Device.DeviceName)
            msg = "%s DeviceId='%s'" % (msg, self.Device.DeviceId)
            msg = "%s Host='%s'" % (msg, self.Device.Host)
            msg = "%s Port='%s'" % (msg, self.Device.Port)
        return msg


    def UpdateGroupStereoPairName(self, name:str) -> Group:
        """
        Updates the name of the current left / right stereo pair speaker group configuration 
        for the device.

        Args:
            name (str):
                New name to assign to the group.

        Returns:
            A `Group` object that contains the result.

        The ST-10 is the only SoundTouch product that supports stereo pair groups.
        
        An existing left / right stereo pair speaker group must exist prior to calling
        this method.

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/UpdateGroupStereoPairName.py
        ```
        </details>
        """
        # check if device supports this uri function; if not then we are done.
        uriPath:str = SoundTouchNodes.updateGroup.Path
        if not uriPath in self.Device.SupportedUris:
            raise SoundTouchError(BSTAppMessages.BST_DEVICE_NOT_CAPABLE_FUNCTION % (self.Device.DeviceName, uriPath), logsi=_logsi)

        # get current group status, and change the name.
        group:Group = self.GetGroupStereoPairStatus(True)
        group.Name = name

        # device is capable - process the request.
        _logsi.LogVerbose(MSG_TRACE_DEVICE_COMMAND_WITH_PARM % ("updateGroup", name, self.Device.DeviceName))
        result:Group = self.Put(SoundTouchNodes.updateGroup, group, Group)
        return result


    def VolumeDown(self) -> None:
        """ 
        Decrease the volume of the device by one. 

        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/VolumeDown.py
        ```
        </details>
        """
        self.Action(SoundTouchKeys.VOLUME_DOWN, KeyStates.Both)


    def VolumeUp(self) -> None:
        """ 
        Increase the volume of the device by one. 
       
        <details>
          <summary>Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode/SoundTouchClient/VolumeUp.py
        ```
        </details>
        """
        self.Action(SoundTouchKeys.VOLUME_UP, KeyStates.Both)
