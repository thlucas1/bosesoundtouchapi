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
    """ 
    Adds the currently playing media to the device favorites. 
    
    Note that this key is reserved for source music services that
    support favorites (e.g. PANDORA, SPOTIFY, etc).   

    This key requires a press key state action only.
    """
    
    AUX_INPUT = 'AUX_INPUT'
    """ 
    Switches the device source to AUX input. 

    This key requires both press AND release key state actions.
    """

    BOOKMARK = 'BOOKMARK'
    """ 
    For Pandora only, bookmark the currently playing song. 

    This key requires a press key state action only.
    """

    MUTE = 'MUTE'
    """ 
    Mutes the volume on the device. 

    This key requires a press key state action only.
    """

    NEXT_TRACK = 'NEXT_TRACK'
    """ 
    Skip to the next track.  
    This may not be available for all content types. 

    This key requires a press key state action only.
    """

    PAUSE = 'PAUSE'
    """ 
    Pause the current media playing. 

    This key requires a press key state action only.
    """

    PLAY = 'PLAY'
    """ 
    Play currently selected media. 

    This key requires a press key state action only.
    """

    PLAY_PAUSE = 'PLAY_PAUSE'
    """ 
    Toggles between play and pause for the currently playing media. 

    This key requires a press key state action only.
    """

    POWER = 'POWER'
    """ 
    Toggle product on/off; on/off refers to waking a product from, or putting a 
    product into its standby state. Products in standby maintain network connections. 
    
    This key requires both press AND release key state actions.
    """

    PRESET_1 = 'PRESET_1'
    """ 
    Play or set Preset 1 (depending on key state).  

    This key requires a press key state action to set the preset, 
    or a release key state action to play the preset.
    """

    PRESET_2 = 'PRESET_2'
    """ 
    Play or set Preset 2 (depending on key state).  

    This key requires a press key state action to set the preset, 
    or a release key state action to play the preset.
    """

    PRESET_3 = 'PRESET_3'
    """ 
    Play or set Preset 3 (depending on key state).  

    This key requires a press key state action to set the preset, 
    or a release key state action to play the preset.
    """

    PRESET_4 = 'PRESET_4'
    """ 
    Play or set Preset 4 (depending on key state).  

    This key requires a press key state action to set the preset, 
    or a release key state action to play the preset.
    """

    PRESET_5 = 'PRESET_5'
    """ 
    Play or set Preset 5 (depending on key state).  

    This key requires a press key state action to set the preset, 
    or a release key state action to play the preset.
    """

    PRESET_6 = 'PRESET_6'
    """ 
    Play or set Preset 6 (depending on key state).  

    This key requires a press key state action to set the preset, 
    or a release key state action to play the preset.
    """

    PREV_TRACK = 'PREV_TRACK'
    """ 
    Skip to the previous track.  
    This may not be available for all content types. 

    This key requires a press key state action only.
    """
    
    REMOVE_FAVORITE = 'REMOVE_FAVORITE'
    """ 
    Removes the currently playing media from the device favorites. 
    
    Note that this key is reserved for source music services that
    support favorites (e.g. PANDORA, SPOTIFY, etc).   

    This key requires a press key state action only.
    """
    
    REPEAT_ALL = 'REPEAT_ALL'
    """ 
    Repeat all the tracks in the list.  
    This may not be available for all content types.

    This key requires a press key state action only.
    """

    REPEAT_OFF = 'REPEAT_OFF'
    """ 
    Turn repeat off.
    This may not be available for all content types.

    This key requires a press key state action only.
    """

    REPEAT_ONE = 'REPEAT_ONE'
    """ 
    Repeat the current track.
    This may not be available for all content types.

    This key requires a press key state action only.
    """

    SHUFFLE_OFF = 'SHUFFLE_OFF'
    """ 
    Turn shuffle off.  
    This may not be available for all content types.

    This key requires a press key state action only.
    """

    SHUFFLE_ON = 'SHUFFLE_ON'
    """ 
    Turn shuffle on.  
    This may not be available for all content types.

    This key requires a press key state action only.
    """

    STOP = 'STOP'
    """ 
    Stop the current media playing. 

    This key requires both press AND release key state actions.
    """

    THUMBS_DOWN = 'THUMBS_DOWN'
    """
    Sets a thumbs down rating for the currently playing media.

    Note that this key is reserved for source music services that
    support ratings (e.g. PANDORA, SPOTIFY, etc).

    This key requires a press key state action only.
    """

    THUMBS_UP = 'THUMBS_UP'
    """
    Sets a thumbs up rating for the currently playing media.
        
    Note that this key is reserved for source music services that
    support ratings (e.g. PANDORA, SPOTIFY, etc).

    This key requires a press key state action only.
    """

    VOLUME_DOWN = 'VOLUME_DOWN'
    """ 
    Decrease the volume of the device by one.  

    This key requires both press AND release key state actions.
    
    The volume is adjusted 1 tick if press and release actions are performed within
    a few milliseconds of each other.  If the press key state action is called, then the
    volume change is repeated until the release key state action is called or until
    minimum volume is reached.
    """

    VOLUME_UP = 'VOLUME_UP'
    """ 
    Increase the volume of the device by one. 

    This key requires both press AND release key state actions.  
    
    The volume is adjusted 1 tick if press and release actions are performed within
    a few milliseconds of each other.  If the press key state action is called, then the
    volume change is repeated until the release key state action is called or until
    maximum volume is reached.
    """
