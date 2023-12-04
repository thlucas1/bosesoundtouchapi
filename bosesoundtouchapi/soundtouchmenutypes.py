# external package imports.
from enum import Enum

# our package imports.
from .bstutils import export

@export
class SoundTouchMenuTypes(Enum):
    """
    Menu Types enumeration.
    """
    
    charts = "charts"
    
    cities = "cities"
    
    createStation = "createStation"
    
    customStations = "customStations"
    
    favAlbums = "favAlbums"
    
    favArtists = "favArtists"
    
    favoriteStations = "favoriteStations"
    
    favPlaylists = "favPlaylists"
    
    favTracks = "favTracks"
    
    forYou = "forYou"
    
    genres = "genres"
    
    international = "international"
    
    liveStations = "liveStations"
    
    local = "local"
    
    locales = "locales"
    
    mixVariety = "mixVariety"
    
    newsTalk = "newsTalk"
    
    perfectFor = "perfectFor"
    
    publicRadio = "publicRadio"
    
    radioStations = "radioStations"
    
    recents = "recents"
    
    recentStations = "recentStations"
    
    recommendations = "recommendations"
    
    sportsRadio = "sportsRadio"
    
    states = "states"
    
    talk = "talk"
    