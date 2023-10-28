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
    AUX_INPUT = 'AUX_INPUT'
    BOOKMARK = 'BOOKMARK'
    MUTE = 'MUTE'
    NEXT_TRACK = 'NEXT_TRACK'
    PAUSE = 'PAUSE'
    PLAY = 'PLAY'
    PLAY_PAUSE = 'PLAY_PAUSE'
    POWER = 'POWER'
    PRESET_1 = 'PRESET_1'
    PRESET_2 = 'PRESET_2'
    PRESET_3 = 'PRESET_3'
    PRESET_4 = 'PRESET_4'
    PRESET_5 = 'PRESET_5'
    PRESET_6 = 'PRESET_6'
    PREV_TRACK = 'PREV_TRACK'
    REMOVE_FAVORITE = 'REMOVE_FAVORITE'
    REPEAT_ALL = 'REPEAT_ALL'
    REPEAT_OFF = 'REPEAT_OFF'
    REPEAT_ONE = 'REPEAT_ONE'
    SHUFFLE_OFF = 'SHUFFLE_OFF'
    SHUFFLE_ON = 'SHUFFLE_ON'
    STOP = 'STOP'
    THUMBS_DOWN = 'THUMBS_DOWN'
    THUMBS_UP = 'THUMBS_UP'
    VOLUME_DOWN = 'VOLUME_DOWN'
    VOLUME_UP = 'VOLUME_UP'

