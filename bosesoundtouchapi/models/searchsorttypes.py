# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class SearchSortTypes(Enum):
    """
    Search Sort Types enumeration.
    """
    
    Album = "album"
    """ Sort by album name. """
    
    Artist = "artist"
    """ Sort by artist name. """
    
    Composer = "composer"
    """ Sort by composer name. """
    
    DateCreated = "dateCreated"
    """ Sort by date created. """
    
    Genre = "genre"
    """ Sort by genre name. """
    
    Playlist = "playlist"
    """ Sort by playlist name. """
    
    StationName = "stationName"
    """ Sort by station name. """
    
    Track = "track"
    """ Sort by track name. """
