# external package imports.
from enum import Enum

# our package imports.
from .bstutils import export

@export
class SoundTouchKeys(Enum):
    """
    SoundTouch Keys enumeration.
    
    All usable keys that can be 'pressed' on a SoundTouch device. 
    """

    ADD_FAVORITE = 'ADD_FAVORITE'
    """ Adds the currently playing media to the device favorites. """
    
    AUX_INPUT = 'AUX_INPUT'
    """ Switches the device source to AUX input. """

    BOOKMARK = 'BOOKMARK'
    """ Mutes the volume of the device. """

    MUTE = 'MUTE'
    """ Mutes the volume on the device. """

    NEXT_TRACK = 'NEXT_TRACK'
    """ Move to the next track in the current media playlist. """

    PAUSE = 'PAUSE'
    """ Pause the current media playing. """

    PLAY = 'PLAY'
    """ Play currently selected media. """

    PLAY_PAUSE = 'PLAY_PAUSE'
    """ Toggles between play and pause for the currently playing media. """

    POWER = 'POWER'
    """ Toggle the power on or off on the device. """

    PRESET_1 = 'PRESET_1'
    """ Selects pre-defined preset number 1 on the device. """

    PRESET_2 = 'PRESET_2'
    """ Selects pre-defined preset number 2 on the device. """

    PRESET_3 = 'PRESET_3'
    """ Selects pre-defined preset number 3 on the device. """

    PRESET_4 = 'PRESET_4'
    """ Selects pre-defined preset number 4 on the device. """

    PRESET_5 = 'PRESET_5'
    """ Selects pre-defined preset number 5 on the device. """

    PRESET_6 = 'PRESET_6'
    """ Selects pre-defined preset number 6 on the device. """

    PREV_TRACK = 'PREV_TRACK'
    """ Move to the previous track in the current media playlist. """
    
    REMOVE_FAVORITE = 'REMOVE_FAVORITE'
    """ Removes the currently playing media from the device favorites. """
    
    REPEAT_ALL = 'REPEAT_ALL'
    """ Enables the repeat all setting for a playlist. """

    REPEAT_OFF = 'REPEAT_OFF'
    """ Disables the repeat setting for a playlist. """

    REPEAT_ONE = 'REPEAT_ONE'
    """ Enables the repeat one setting for a playlist. """

    SHUFFLE_OFF = 'SHUFFLE_OFF'
    """ Disables shuffle mode for a playlist. """

    SHUFFLE_ON = 'SHUFFLE_ON'
    """ Enables shuffle mode for a playlist. """

    STOP = 'STOP'
    """ Stop the current media playing. """

    THUMBS_DOWN = 'THUMBS_DOWN'
    """
    Sets a thumbs down rating for the currently playing media.
        
    Note that the THUMBS_DOWN key is reserved for source music services
    that support ratings (e.g. PANDORA, SPOTIFY, etc).
    """

    THUMBS_UP = 'THUMBS_UP'
    """
    Sets a thumbs up rating for the currently playing media.
        
    Note that the THUMBS_UP key is reserved for source music services
    that support ratings (e.g. PANDORA, SPOTIFY, etc).
    """

    VOLUME_DOWN = 'VOLUME_DOWN'
    """ Decrease the volume of the device by one. """

    VOLUME_UP = 'VOLUME_UP'
    """ Increase the volume of the device by one. """
