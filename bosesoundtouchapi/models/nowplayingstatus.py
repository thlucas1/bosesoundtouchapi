# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind, _xmlGetAttrInt, _xmlFindBool, _xmlGetAttrBool
from .contentitem import ContentItem
from .shufflesettingtypes import ShuffleSettingTypes
from .repeatsettingtypes import RepeatSettingTypes

@export
class NowPlayingStatus:
    """
    SoundTouch device Now Playing Status configuration object.
       
    This class contains the attributes and sub-items that represent the
    status of currently playing media of the device.
    
    Some items are not relevant for certain types of media.  For example,
    the `ConnectionStatus` property applies only to BLUETOOTH sources. 
    """

    def __init__(self, source:str=None, sourceAccount:str=None,
                 album:str=None, artist:str=None, artistId:str=None, artUrl:str=None,
                 description:str=None, duration:int=None, genre:str=None, playStatus:str=None, position:int=None, 
                 sessionId:str=None, stationLocation:str=None, stationName:str=None,
                 track:str=None, trackId:str=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (SoundTouchSources|str):
                Source input.
            sourceAccount (str):
                Source account this content item is played with.
            album (str):
                The album of the playing track (if present). 
            artist (str):
                The creator of the track (if present). 
            artistId (str):
                Unique identifier of the artist, as provided by the source music service (if present). 
            artUrl (str):
                A url link to the art image of the station (if present). 
            description (str):
                A brief description that was added to the track (if present). 
            duration (int):
                The track's duration (if present).
            genre (str):
                The genre of the track (if present). 
            playStatus (str):
                Indicates whether the device is currently playing the embedded track. 
            position (int):
                The current position of the playing media (if present). 
            sessionId (str):
                Unique identifier of the session, as provided by the source music service (if present). 
            stationLocation (str):
                The station's location.
            stationName (str):
                The station's name (if present). 
            track (str):
                The current media track name (if present). 
            trackId (str):
                Unique identifier of the track, as provided by the source music service (if present). 
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._DeviceId:str = None
        self._Source:str = None
        self._SourceAccount:str = None
        self._ContentItem:ContentItem = None
                              
        self._Album:str = None
        self._Artist:str = None
        self._ArtistId:str = None
        self._ArtImageStatus:str = None
        self._ArtUrl:str = None
        self._ConnectionDeviceName:str = None
        self._ConnectionStatus:str = None
        self._Description:str = None
        self._Duration:int = 0
        self._Position:int = 0
        self._Genre:str = None
        self._IsAdvertisement:bool = False
        self._IsFavorite:bool = False
        self._IsFavoriteEnabled:bool = False
        self._IsRatingEnabled:bool = False
        self._IsSkipEnabled:bool = False
        self._IsSkipPreviousEnabled:bool = False
        self._IsSkipPreviousSupported:bool = False
        self._IsSeekSupported:bool = False
        self._PlayStatus:str = None
        self._Rating:str = None
        self._RepeatSetting:str = None
        self._SessionId:str = None
        self._ShuffleSetting:str = None
        self._StationLocation:str = None
        self._StationName:str = None
        self._StreamType:str = None
        self._Track:str = None
        self._TrackId:str = None

        # other possibilities?
        # userAccountSuspended. 
        # inactivityTimeoutExpired. 

        if (root is None):
            
            if duration is not None and (not isinstance(duration, int)):
                duration = None
            if position is not None and (not isinstance(position, int)):
                position = None

            if album is not None: self._Album = str(album)
            if artist is not None: self._Artist = str(artist)
            if artistId is not None: self._ArtistId = str(artistId)
            if artUrl is not None: self._ArtUrl = str(artUrl)
            if description is not None: self._Description = str(description)
            if duration is not None: self._Duration = duration
            if genre is not None: self._Genre = str(genre)
            if playStatus is not None: self._PlayStatus = str(playStatus)
            if position is not None: self._Position = position
            if sessionId is not None: self._SessionId = str(sessionId)
            if source is not None: self._Source = str(source)
            if sourceAccount is not None: self._SourceAccount = str(sourceAccount)
            if stationLocation is not None: self._StationLocation = str(stationLocation)
            if stationName is not None: self._StationName = str(stationName)
            if track is not None: self._Track = str(track)
            if trackId is not None: self._TrackId = str(trackId)
            
            ci:ContentItem = ContentItem(source=source, sourceAccount=sourceAccount, isPresetable=False, containerArt=artUrl)
            self._ContentItem = ci
            
            self._IsAdvertisement = None
            self._IsFavorite = None
            self._IsFavoriteEnabled = None
            self._IsRatingEnabled = None
            self._IsSkipEnabled = None
            self._IsSkipPreviousEnabled = None
        
        else:

            self._DeviceId = root.get('deviceID')
            self._Source = root.get('source')
            self._SourceAccount = root.get('sourceAccount')

            elmContentItem = root.find("ContentItem")
            if elmContentItem is not None:
                self._ContentItem = ContentItem(root=elmContentItem)

            self._Album = _xmlFind(root, "album")
            self._Artist = _xmlFind(root, "artist")
            self._ArtistId = _xmlFind(root, "artistID")
            self._Description = _xmlFind(root, "description")
            self._Genre = _xmlFind(root, "genre")
            self._IsAdvertisement = _xmlFindBool(root, "isAdvertisement")
            self._IsFavorite = _xmlFindBool(root, "isFavorite")
            self._IsFavoriteEnabled = _xmlFindBool(root, "favoriteEnabled")
            self._IsRatingEnabled = _xmlFindBool(root, "rateEnabled")
            self._IsSkipEnabled = _xmlFindBool(root, "skipEnabled")
            self._IsSkipPreviousEnabled = _xmlFindBool(root, "skipPreviousEnabled")
            self._PlayStatus = _xmlFind(root, "playStatus")
            self._Rating = _xmlFind(root, "rating")
            self._RepeatSetting = _xmlFind(root, "repeatSetting")
            self._SessionId = _xmlFind(root, "sessionID")
            self._ShuffleSetting = _xmlFind(root, "shuffleSetting")
            self._StationLocation = _xmlFind(root, "stationLocation")
            self._StationName = _xmlFind(root, "stationName")
            self._StreamType = _xmlFind(root, "streamType")
            self._Track = _xmlFind(root, "track")
            self._TrackId = _xmlFind(root, "trackID")

            # art node.
            elmNode = root.find('art')
            if (elmNode != None):
                self._ArtImageStatus = elmNode.get("artImageStatus")
                self._ArtUrl = elmNode.text

            # connectionStatusInfo node.
            elmNode = root.find('connectionStatusInfo')
            if (elmNode != None):
                self._ConnectionDeviceName = elmNode.get("deviceName")
                self._ConnectionStatus = elmNode.get("status")
            
            # time node (e.g. <time total="265">15</time>).
            elmNode = root.find('time')
            if (elmNode != None):
                self._Duration = _xmlGetAttrInt(elmNode, 'total')
                self._Position = int(elmNode.text)
                
            # skipPreviousSupported node (e.g. <skipPreviousSupported value="true" />).
            elmNode = root.find('skipPreviousSupported')
            if (elmNode != None):
                self._IsSkipPreviousSupported = _xmlGetAttrBool(elmNode, 'value')
                
            # seekSupported node (e.g. <seekSupported value="false" />)
            elmNode = root.find('seekSupported')
            if (elmNode != None):
                self._IsSeekSupported = _xmlGetAttrBool(elmNode, 'value')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Album(self) -> str:
        """ 
        The album of the playing track (if present). 
        """
        return self._Album


    @property
    def ArtImageStatus(self) -> str:
        """ 
        Contains "IMAGE_PRESENT" value if an art image url is present.
        """
        return self._ArtImageStatus


    @property
    def ArtUrl(self) -> str:
        """ 
        A url link to the art image of the station (if present). 
        
        Note that this art image could be different from the `ContentItem.ContainerArt` image.
        """
        return self._ArtUrl


    @property
    def Artist(self) -> str:
        """ 
        The creator of the track (if present). 
        """
        return self._Artist


    @property
    def ArtistId(self) -> str:
        """ 
        Unique identifier of the artist, as provided by the source music service (if present). 
        """
        return self._ArtistId


    @property
    def ConnectionDeviceName(self) -> str:
        """ 
        The staus of the bluetooth connection (if present). 
        
        This value only seems to be present for the "BLUETOOTH" source.
        """
        return self._ConnectionDeviceName


    @property
    def ConnectionStatus(self) -> str:
        """ 
        The staus of the bluetooth connection (if present). 
        
        This value only seems to be present for the "BLUETOOTH" source.
        """
        return self._ConnectionStatus


    @property
    def ContainerArtUrl(self) -> str:
        """ 
        A url link to the art image of the station or track that is playing.
        The following logic is implemented to return an image url:
        - the `ArtUrl` value is returned if present;  
        - the `ContentItem.ContainerArt` url is returned if present;  
        - if neither of the above, then null is returned.  
        
        This is a helper property, and not part of the SoundTouch Web Services specification.
        """
        if (self._ArtUrl is not None):
            return self._ArtUrl
        elif (self._ContentItem is not None) and (self._ContentItem.ContainerArt is not None):
            return self._ContentItem.ContainerArt
        return None


    @property
    def ContentItem(self) -> 'ContentItem':
        """ 
        The selected ContentItem. 
        """
        return self._ContentItem


    @property
    def Description(self) -> str:
        """ 
        A brief description that was added to the track (if present). 
        """
        return self._Description


    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId

    
    @property
    def Duration(self) -> int:
        """ 
        The track's duration (if present).
        """
        return self._Duration


    @property
    def Genre(self) -> str:
        """ 
        The genre of the track (if present). 
        """
        return self._Genre


    @property
    def IsAdvertisement(self) -> bool:
        """ 
        True if the currently playing track is an advertisement; otherwise, False.
        
        Note that not all sources track advertisements.
        - TuneIn source does not track advertisements; 
        - Pandora music service source tracks advertisements.
        """
        if self._IsAdvertisement is None:
            return False
        return self._IsAdvertisement


    @property
    def IsFavorite(self) -> bool:
        """ 
        True if the track has been marked as a favorite; otherwise, False.
        
        Note that not all sources track favorites.  
        """
        if self._IsFavorite is None:
            return False
        return self._IsFavorite


    @property
    def IsFavoriteEnabled(self) -> bool:
        """ 
        True if the track can be saved as a favorite; otherwise, False.
        """
        return self._IsFavoriteEnabled


    @property
    def IsPlaying(self) -> bool:
        """ 
        Returns true if the current `PlayStatus` is "PLAY_STATE", which indicates the content is
        fully playing (e.g. not buffered, etc); otherwise, False.
        """
        return (self._PlayStatus == "PLAY_STATE")


    @property
    def IsRatingEnabled(self) -> bool:
        """ 
        True if track rating is enabled; otherwise, False.
        
        If true, then the `SoundTouchClient.ThumbsUp` and 
        """
        return self._IsRatingEnabled


    @property
    def IsRepeatEnabled(self) -> bool:
        """ 
        True if repeat play (one or all) is enabled; otherwise, False. 
        
        The `RepeatSetting` property contains the actual repeat setting.
        """
        if self._RepeatSetting is None: 
            return False
        return True


    @property
    def IsSeekSupported(self) -> bool:
        """ 
        True if the currently playing media supports seek functions; otherwise, False (if present).
        """
        return self._IsSeekSupported


    @property
    def IsShuffleEnabled(self) -> bool:
        """ 
        True if shuffle play is enabled; otherwise, False. 
        """
        if self._ShuffleSetting is None or self._ShuffleSetting == ShuffleSettingTypes.Off.value:
            return False
        return True


    @property
    def IsSkipEnabled(self) -> bool:
        """ 
        True if the currently playing media supports skip functions; otherwise, False (if present).
        """
        return self._IsSkipEnabled


    @property
    def IsSkipPreviousEnabled(self) -> bool:
        """ 
        True if the currently playing media skip previous functions are enabled; otherwise, False (if present).
        """
        return self._IsSkipPreviousEnabled


    @property
    def IsSkipPreviousSupported(self) -> bool:
        """ 
        True if the currently playing media supports skip previous functions; otherwise, False (if present).
        """
        return self._IsSkipPreviousSupported


    @property
    def PlayStatus(self) -> str:
        """ 
        Indicates the current play status of the item (e.g. "PLAY_STATE", "BUFFERING_STATE", etc.)
        """
        return self._PlayStatus


    @property
    def Position(self) -> int:
        """ 
        The current position of the playing media (if present). 
        """
        return self._Position


    @property
    def Rating(self) -> str:
        """ 
        Rating value (e.g. "NONE", "DOWN", "UP", etc). 
        """
        return self._Rating


    @property
    def RepeatSetting(self) -> str:
        """ 
        Repeat setting value (e.g. "REPEAT_ALL", "REPEAT_ONE", "REPEAT_OFF", etc). 
        
        If null, then repeat functions are not enabled for the playing media.
        """
        return self._RepeatSetting


    @property
    def SessionId(self) -> str:
        """ 
        Unique identifier of the session, as provided by the source music service (if present). 
        """
        return self._SessionId


    @property
    def ShuffleSetting(self) -> str:
        """ 
        Shuffle setting value (e.g. "SHUFFLE_ON", "SHUFFLE_OFF", etc). 
        
        If null, then shuffle functions are not enabled for the playing media.
        """
        return self._ShuffleSetting


    @property
    def Source(self) -> str:
        """ 
        The media source.
        This should be one of the sources defined in `bosesoundtouchapi.soundtouchsources.SoundTouchSources`. 
        """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ The account associated with the Source. """
        return self._SourceAccount


    @property
    def StationLocation(self) -> str:
        """ 
        The station's location.
        """
        return self._StationLocation


    @property
    def StationName(self) -> str:
        """ 
        The station's name (if present). 
        """
        return self._StationName


    @property
    def StreamType(self) -> str:
        """ 
        The stream type of the current track (e.g. "RADIO_STREAMING", "TRACK_ONDEMAND" when playing from
        an external resource, etc).
        """
        return self._StreamType


    @property
    def Track(self) -> str:
        """ 
        The current media track name (if present). 
        """
        return self._Track


    @property
    def TrackId(self) -> str:
        """ 
        Unique identifier of the track, as provided by the source music service (if present). 
        """
        return self._TrackId


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'device_id': self._DeviceId,
            'source': self._Source,
            'source_account': self._SourceAccount,
            'content_item': self._ContentItem.ToDictionary(),
            'album': self._Album,
            'artist': self._Artist,
            'artist_id': self._ArtistId,
            'art_image_status': self._ArtImageStatus,
            'art_url': self._ArtUrl,
            'connection_device_name': self._ConnectionDeviceName,
            'connection_status': self._ConnectionStatus,
            'description': self._Description,
            'duration': self._Duration,
            'position': self._Position,
            'genre': self._Genre,
            'is_advertisement': self._IsAdvertisement,
            'is_favorite': self._IsFavorite,
            'is_favorite_enabled': self._IsFavoriteEnabled,
            'is_rating_enabled': self._IsRatingEnabled,
            'is_skip_enabled': self._IsSkipEnabled,
            'is_skip-previous_enabled': self._IsSkipPreviousEnabled,
            'is_skip_previous_supported': self._IsSkipPreviousSupported,
            'is_seek_supported': self._IsSeekSupported,
            'play_status': self._PlayStatus,
            'rating': self._Rating,
            'repeat_setting': self._RepeatSetting,
            'session_id': self._SessionId,
            'shuffle_setting': self._ShuffleSetting,
            'station_location': self._StationLocation,
            'station_name': self._StationName,
            'stream_type': self._StreamType,
            'track': self._Track,
            'track_id': self._TrackId,
        }
        return result
        

    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'NowPlayingStatus:'
        if self._Source is not None and len(self._Source) > 0: msg = '%s\n Source="%s"' % (msg, str(self._Source))
        if self._SourceAccount is not None and len(self._SourceAccount) > 0: msg = '%s\n SourceAccount="%s"' % (msg, str(self._SourceAccount))
        if self._ContentItem is not None: msg = '%s\n %s' % (msg, self._ContentItem.ToString())
        if self._Album is not None and len(self._Album) > 0: msg = '%s\n Album="%s"' % (msg, str(self._Album))
        if self._Artist is not None and len(self._Artist) > 0: msg = '%s\n Artist="%s"' % (msg, str(self._Artist))
        if self._ArtistId is not None and len(self._ArtistId) > 0: msg = '%s\n ArtistId="%s"' % (msg, str(self._ArtistId))
        if self._ArtImageStatus is not None and len(self._ArtImageStatus) > 0: msg = '%s\n ArtImageStatus="%s"' % (msg, str(self._ArtImageStatus))
        if self._ArtUrl is not None and len(self._ArtUrl) > 0: msg = '%s\n ArtUrl="%s"' % (msg, str(self._ArtUrl))
        if self._ConnectionDeviceName is not None and len(self._ConnectionDeviceName) > 0: msg = '%s\n ConnectionDeviceName="%s"' % (msg, str(self._ConnectionDeviceName))
        if self._ConnectionStatus is not None and len(self._ConnectionStatus) > 0: msg = '%s\n ConnectionStatus="%s"' % (msg, str(self._ConnectionStatus))
        if self.ContainerArtUrl is not None: msg = '%s\n ContainerArtUrl="%s"' % (msg, str(self.ContainerArtUrl))
        if self._Description is not None and len(self._Description) > 0: msg = '%s\n Description="%s"' % (msg, str(self._Description))
        if self._DeviceId is not None and len(self._DeviceId) > 0: msg = '%s\n DeviceId="%s"' % (msg, str(self._DeviceId))
        if self._Duration is not None and self._Duration > 0: msg = '%s\n Duration="%s"' % (msg, str(self._Duration))
        if self._Genre is not None and len(self._Genre) > 0: msg = '%s\n Genre="%s"' % (msg, str(self._Genre))
        if self.IsAdvertisement is not None: msg = '%s\n IsAdvertisement="%s"' % (msg, str(self.IsAdvertisement).lower())
        if self.IsFavorite is not None: msg = '%s\n IsFavorite="%s"' % (msg, str(self.IsFavorite).lower())
        if self._IsFavoriteEnabled is not None: msg = '%s\n IsFavoriteEnabled="%s"' % (msg, str(self._IsFavoriteEnabled).lower())
        if self._IsRatingEnabled is not None: msg = '%s\n IsRateEnabled="%s"' % (msg, str(self._IsRatingEnabled).lower())
        if self.IsRepeatEnabled is not None: msg = '%s\n IsRepeatEnabled="%s"' % (msg, str(self.IsRepeatEnabled).lower())
        if self._IsSeekSupported is not None: msg = '%s\n IsSeekSupported="%s"' % (msg, str(self._IsSeekSupported).lower())
        if self.IsShuffleEnabled is not None: msg = '%s\n IsShuffleEnabled="%s"' % (msg, str(self.IsShuffleEnabled).lower())
        if self._IsSkipEnabled is not None: msg = '%s\n IsSkipEnabled="%s"' % (msg, str(self._IsSkipEnabled).lower())
        if self._IsSkipPreviousEnabled is not None: msg = '%s\n IsSkipPreviousEnabled="%s"' % (msg, str(self._IsSkipPreviousEnabled).lower())
        if self._IsSkipPreviousSupported is not None: msg = '%s\n IsSkipPreviousSupported="%s"' % (msg, str(self._IsSkipPreviousSupported).lower())
        if self._PlayStatus is not None and len(self._PlayStatus) > 0: msg = '%s\n PlayStatus="%s"' % (msg, str(self._PlayStatus))
        if self._Position is not None and self._Position > 0: msg = '%s\n Position="%s"' % (msg, str(self._Position))
        if self._Rating is not None and len(self._Rating) > 0: msg = '%s\n Rating="%s"' % (msg, str(self._Rating))
        if self._RepeatSetting is not None and len(self._RepeatSetting) > 0: msg = '%s\n RepeatSetting="%s"' % (msg, str(self._RepeatSetting))
        if self._SessionId is not None and len(self._SessionId) > 0: msg = '%s\n SessionId="%s"' % (msg, str(self._SessionId))
        if self._ShuffleSetting is not None and len(self._ShuffleSetting) > 0: msg = '%s\n ShuffleSetting="%s"' % (msg, str(self._ShuffleSetting))
        if self._StationLocation is not None and len(self._StationLocation) > 0: msg = '%s\n StationLocation="%s"' % (msg, str(self._StationLocation))
        if self._StationName is not None and len(self._StationName) > 0: msg = '%s\n StationName="%s"' % (msg, str(self._StationName))
        if self._StreamType is not None and len(self._StreamType) > 0: msg = '%s\n StreamType="%s"' % (msg, str(self._StreamType))
        if self._Track is not None and len(self._Track) > 0: msg = '%s\n Track="%s"' % (msg, str(self._Track))
        if self._TrackId is not None and len(self._TrackId) > 0: msg = '%s\n TrackId="%s"' % (msg, str(self._TrackId))
        return msg 
