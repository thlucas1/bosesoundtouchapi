# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class UserPlayControlTypes(Enum):
    """
    User Play Control Types enumeration.
    """
    
    Pause = 'PAUSE_CONTROL'
    """ Pause currently playing content. """
    
    Play = 'PLAY_CONTROL'
    """ Play content that is currently paused or stopped. """
    
    PlayPause = 'PLAY_PAUSE_CONTROL'
    """ Pause currently playing content, or Play currently paused content. """

    Stop = 'STOP_CONTROL'
    """ Stop currently playing content. """
        