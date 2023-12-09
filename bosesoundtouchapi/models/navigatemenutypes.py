# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class NavigateMenuTypes(Enum):
    """
    Menu Types enumeration.
    """
    
    Charts = "charts"
    
    Cities = "cities"
    
    CreateStation = "createStation"
    
    CustomStations = "customStations"
    
    FavoriteAlbums = "favAlbums"
    
    FavoriteArtists = "favArtists"
    
    FavoriteStations = "favoriteStations"
    
    FavoritePlaylists = "favPlaylists"
    
    FavoriteTracks = "favTracks"
    
    ForYou = "forYou"
    
    Genres = "genres"
    
    International = "international"
    
    LiveStations = "liveStations"
    
    Local = "local"
    
    Locales = "locales"
    
    MixVariety = "mixVariety"
    
    NewsTalk = "newsTalk"
    
    PerfectFor = "perfectFor"
    
    PublicRadio = "publicRadio"
    
    RadioStations = "radioStations"
    
    Recents = "recents"
    
    RecentStations = "recentStations"
    
    Recommendations = "recommendations"
    
    SportsRadio = "sportsRadio"
    
    States = "states"
    
    Talk = "talk"
    