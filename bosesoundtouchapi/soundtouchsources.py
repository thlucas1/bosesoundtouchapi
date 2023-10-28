# external package imports.
from enum import Enum

# our package imports.
from .bstutils import export

@export
class SoundTouchSources(Enum):
    """
    Defines the Source of a ContentItem.
    """
    
    DEFAULT = "INVALID_SOURCE"
    
    AIRPLAY = "AIRPLAY"
    
    AMAZON = "AMAZON"
    
    AUX = "AUX"
    
    BLUETOOTH = "BLUETOOTH"
    """ Content will be played over a Bluetooth connection. """
    
    DEEZER = "DEEZER"
    
    IHEART = "IHEART"
    
    INTERNET_RADIO = "INTERNET_RADIO"
    
    INVALID = "INVALID_SOURCE"
    
    LOCAL_MUSIC = "LOCAL_MUSIC"
    
    NOTIFICATION = "NOTIFICATION"
    
    PANDORA = "PANDORA"
    
    PRODUCT = "PRODUCT"
    
    QPLAY = "QPLAY"
    
    SIRIUSXM = "SIRIUSXM"
    
    SPOTIFY = "SPOTIFY"
    
    STANDBY = "STANDBY"
    
    STORED_MUSIC = "STORED_MUSIC"
    
    UPDATE = "UPDATE"
