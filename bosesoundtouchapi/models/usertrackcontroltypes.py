# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class UserTrackControlTypes(Enum):
    """
    User Track Control Types enumeration.
    """
    
    Next = 'NEXT_TRACK'
    """ Play next track. """
    
    Previous = 'PREV_TRACK'
    """ 
    Play previous track if current track has been playing for less than 10 seconds;
    otherwise, restart play of the current track.
    """
    
    PreviousForce = 'PREV_TRACK_FORCE'
    """ Play previous track. """
    
    RepeatOne = 'REPEAT_ONE_TRACK'
    """ Repeat only the current track. """
    
    RepeatAll = 'REPEAT_ALL_TRACKS'
    """ Repeat all tracks in the playlist. """
    
    RepeatOff = 'REPEAT_TRACKS_OFF'
    """ Turn off repeat track setting. """
    
    ShuffleOn = 'SHUFFLE_TRACKS_ON'
    """ Shuffle all tracks in the playlist. """
    
    ShuffleOff = 'SHUFFLE_TRACKS_OFF'
    """ Turn off shuffle track setting. """
    
    SeekToTime = 'SEEK_TO_TIME'
    """ 
    Start playing the track at the designated time, if the NowPlaying media 
    supports seek functions. 
    """
    