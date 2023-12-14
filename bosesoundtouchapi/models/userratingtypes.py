# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class UserRatingTypes(Enum):
    """
    User Rating Types enumeration.
    """
    
    NotRated = "NONE"
    """ No rating given. """
    
    ThumbsDown = "DOWN"
    """ Thumbs down rating. """
    
    ThumbsUp = "UP"
    """ Thumbs up rating. """
