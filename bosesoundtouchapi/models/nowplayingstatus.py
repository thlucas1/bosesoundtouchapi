# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr
from .contentitem import ContentItem

@export
class NowPlayingStatus:
    """
    SoundTouch device Now Playing Status configuration object.
       
    This class contains the attributes and sub-items that represent the
    status of currently playing media of the device.
    
    Some items are not relevant for certain types of media.  For example,
    the `ConnectionStatus` property applies only to BLUETOOTH sources. 
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        if (root is None):

            # the following do not appear in all types of media, so they need to be
            # initialized in case they are not set.
            self._Source = None
            self._ContentItem:ContentItem = None
            
            self._Album:str = None
            self._Artist:str = None
            self._Image:str = None
            self._Track:str = None
            
            self._ConnectionDeviceName:str = None
            self._ConnectionStatus:str = None
            self._Description:str = None
            self._Duration:str = None
            self._Position:int = 0
            self._Genre:str = None
            self._IsFavorite:bool = False
            self._IsFavoriteEnabled:bool = False
            self._IsSkipEnabled:bool = False
            self._IsSkipPreviousEnabled:bool = False
            self._IsSkipPreviousSupported:bool = False
            self._IsSeekSupported:bool = False
            self._PlayStatus:str = None
            self._RepeatSetting:str = None
            self._ShuffleSetting = None
            self._StationLocation:str = None
            self._StationName:str = None
            self._StreamType:str = None
            self._TrackId:str = None

        else:

            self._Source = _xmlFindAttr(root, 'nowPlaying', 'source')

            self._ContentItem:ContentItem = None
            content_item = root.find("ContentItem")
            if content_item != None: 
                self._ContentItem = ContentItem(root=content_item)

            self._Album:str = _xmlFind(root, "album")
            self._Artist:str = _xmlFind(root, "artist")
            image_status:str = _xmlFindAttr(root, "art", "artImageStatus")
            if image_status == "IMAGE_PRESENT": self._Image:str = _xmlFind(root, "art")
            else: self._Image:str = None
            self._Track:str = _xmlFind(root, "track")

            self._ConnectionDeviceName:str = _xmlFindAttr(root, "connectionStatusInfo", "deviceName")
            self._ConnectionStatus:str = _xmlFindAttr(root, "connectionStatusInfo", "status")
            self._Description:str = _xmlFind(root, "description")
            self._Duration:str = int(_xmlFindAttr(root, "time", "total", default='0'))
            self._Position:int = int(_xmlFind(root, "time", default='0'))
            self._Genre:str = _xmlFind(root, "genre")
            self._IsFavorite:bool = _xmlFind(root, "isFavorite", default=False, defaultNoText=True)
            self._IsFavoriteEnabled:bool = _xmlFind(root, "favoriteEnabled", default=False, defaultNoText=True)
            self._IsSkipEnabled:bool = _xmlFind(root, "skipEnabled", default=False, defaultNoText=True)
            self._IsSkipPreviousEnabled:bool = _xmlFind(root, "skipPreviousEnabled", default=False, defaultNoText=True)
            self._IsSkipPreviousSupported:bool = _xmlFind(root, "skipPreviousSupported", default=False, defaultNoText=True)
            self._IsSeekSupported:bool = _xmlFind(root, "seekSupported", default=False, defaultNoText=True)
            self._PlayStatus:str = _xmlFind(root, "playStatus")
            self._RepeatSetting:str = _xmlFind(root, "repeatSetting")
            self._ShuffleSetting = _xmlFind(root, "shuffleSetting")
            self._StationLocation:str = _xmlFind(root, "stationLocation")
            self._StationName:str = _xmlFind(root, "stationName")
            self._StreamType:str = _xmlFind(root, "streamType")
            self._TrackId:str = _xmlFind(root, "trackID")
            

    def __repr__(self) -> str:
        return self.ToString()


    @property
    def Album(self) -> str:
        """ 
        The album of the playing track (if present). 
        
        Sources supporting: AIRPLAY
        """
        return self._Album


    @property
    def Artist(self) -> str:
        """ 
        The creator of the track (if present). 
        
        Sources supporting: AIRPLAY
        """
        return self._Artist


    @property
    def ConnectionDeviceName(self) -> str:
        """ 
        The staus of the bluetooth connection (if present). 
        
        Sources supporting: BLUETOOTH
        """
        return self._ConnectionDeviceName


    @property
    def ConnectionStatus(self) -> str:
        """ 
        The staus of the bluetooth connection (if present). 
        
        Sources supporting: BLUETOOTH
        """
        return self._ConnectionStatus


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
    def Duration(self) -> int:
        """ 
        The track's duration. 
            
        Sources supporting: AIRPLAY
        """
        return self._Duration


    @property
    def Genre(self) -> str:
        """ 
        The genre of the track (if present). 
        """
        return self._Artist


    @property
    def Image(self) -> str:
        """ 
        A url link to the cover image of the track (if present). 
            
        Sources supporting: AIRPLAY
        """
        return self._Image


    @property
    def IsFavorite(self) -> bool:
        """ 
        True if the track has been marked as a favorite; otherwise, False.
        """
        return self._IsFavorite


    @property
    def IsFavoriteEnabled(self) -> bool:
        """ 
        True if the track can be saved as a favorite; otherwise, False.
        """
        return self._IsFavoriteEnabled


    @property
    def IsRepeatEnabled(self) -> bool:
        """ 
        True if repeat play (one or all) is enabled; otherwise, False. 
        
        The `RepeatSetting` property contains the actual repeat setting.
        """
        if self._RepeatSetting in ["REPEAT_ALL", "REPEAT_ONE"]: 
            return True
        return False


    @property
    def IsSeekSupported(self) -> bool:
        """ 
        True if the currently playing media supports seek functions; otherwise, False.
        
        Sources supporting: AIRPLAY
        """
        return self._IsSeekSupported


    @property
    def IsShuffleEnabled(self) -> bool:
        """ 
        True if shuffle play is enabled; otherwise, False. 
        """
        if self._ShuffleSetting in ["SHUFFLE_ON"]:
            return True
        return False


    @property
    def IsSkipEnabled(self) -> bool:
        """ 
        True if the currently playing media supports skip functions; otherwise, False.
        
        Sources supporting: AIRPLAY
        """
        return self._IsSkipEnabled


    @property
    def IsSkipPreviousEnabled(self) -> bool:
        """ 
        True if the currently playing media skip previous functions are enabled; otherwise, False.
        
        Sources supporting: AIRPLAY
        """
        return self._IsSkipPreviousEnabled


    @property
    def IsSkipPreviousSupported(self) -> bool:
        """ 
        True if the currently playing media supports skip previous functions; otherwise, False.
        
        Sources supporting: AIRPLAY
        """
        return self._IsSkipPreviousSupported


    @property
    def PlayStatus(self) -> str:
        """ 
        Indicates whether the device is currently playing the embedded track. 
        """
        return self._PlayStatus


    @property
    def Position(self) -> int:
        """ 
        The current position of the playing media (if present). 
            
        Sources supporting: AIRPLAY
        """
        return self._Position


    @property
    def RepeatSetting(self) -> str:
        """ 
        Repeat setting value (e.g. "REPEAT_ALL", "REPEAT_ONE", "REPEAT_OFF", etc). 
        """
        return self._RepeatSetting


    @property
    def ShuffleSetting(self) -> str:
        """ 
        Shuffle setting value (e.g. "SHUFFLE_ON", "SHUFFLE_OFF", etc). 
        """
        return self._ShuffleSetting


    @property
    def Source(self) -> str:
        """ 
        The media source.
        This should be one of the sources defined in `bosesoundtouchapi.soundtouchsource.SoundTouchSources`. 
        """
        return self._Source


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
            
        Sources supporting: AIRPLAY
        """
        return self._StationName


    @property
    def StreamType(self) -> str:
        """ 
        The stream type of the current track (TRACK_ONDEMAND when playing from
        an external resource).
        """
        return self._StreamType


    @property
    def Track(self) -> str:
        """ 
        The current media file name (if present). 
            
        Sources supporting: AIRPLAY
        """
        return self._Track


    @property
    def TrackId(self) -> str:
        """ 
        The track's id. 
        """
        return self._TrackId


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'NowPlayingStatus:'
        if self._Source and len(self._Source) > 0: msg = '%s source="%s"' % (msg, str(self._Source))
        if self._PlayStatus and len(self._PlayStatus) > 0: msg = '%s playStatus="%s"' % (msg, str(self._PlayStatus))
        if self._ContentItem: msg = '%s %s' % (msg, self._ContentItem.ToString())
        if self._RepeatSetting and len(self._RepeatSetting) > 0: msg = '%s repeat="%s"' % (msg, str(self._RepeatSetting))
        if self._ShuffleSetting and len(self._ShuffleSetting) > 0: msg = '%s shuffle="%s"' % (msg, str(self._ShuffleSetting))
        msg = '%s favoriteEnabled="%s"' % (msg, str(self._IsFavoriteEnabled).lower())
        if self._IsFavorite: msg = '%s favorite="%s"' % (msg, str(self._IsFavorite).lower())
        return msg 
    