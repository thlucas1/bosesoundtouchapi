# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class PlayStatusTypes(Enum):
    """
    Play Status Types enumeration.
    """
    
    Buffering = 'BUFFERING_STATE'
    """ Content is being loaded to a buffer. """
    
    Invalid = 'INVALID_PLAY_STATUS'
    """ Unknow or invalid. """

    Paused = 'PAUSE_STATE'
    """ Content is paused. """

    Playing = 'PLAY_STATE'
    """ Content is playing. """
    
    Stopped = 'STOP_STATE'
    """ Content is stopped. """
