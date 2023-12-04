# external package imports.
from enum import Enum

# our package imports.
from .bstutils import export

@export
class SoundTouchSortOrders(Enum):
    """
    Sort Orders enumeration.
    """
    
    album = "album"
    """ Sort by album name. """
    
    artist = "artist"
    """ Sort by artist name. """
    
    composer = "composer"
    """ Sort by composer name. """
    
    dateCreated = "dateCreated"
    """ Sort by date created. """
    
    genre = "genre"
    """ Sort by genre name. """
    
    playlist = "playlist"
    """ Sort by playlist name. """
    
    stationName = "stationName"
    """ Sort by station name. """
    
    track = "track"
    """ Sort by track name. """
