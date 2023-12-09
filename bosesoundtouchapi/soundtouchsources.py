# external package imports.
from enum import Enum

# our package imports.
from .bstutils import export

@export
class SoundTouchSources(Enum):
    """
    Defines the Source of a ContentItem.
    """
    
    DEFAULT = ""
    """ Source is not set (default). """
    
    AIRPLAY = "AIRPLAY"
    """ Apple AirPlay source. """
    
    AMAZON = "AMAZON"
    """ Amazon Music Service source. """
    
    AUX = "AUX"
    """ Auxilliary input source. """
    
    BLUETOOTH = "BLUETOOTH"
    """ BlueTooth connection source. """
    
    DEEZER = "DEEZER"
    """ Deezer Music Service source. """
    
    IHEART = "IHEART"
    """ iHeart Radio Music Service source. """
    
    INTERNET_RADIO = "INTERNET_RADIO"
    """ INTERNET_RADIO (custom URL) Music Service source. """
    
    INVALID = "INVALID_SOURCE"
    """ Source is not recognized as an existing source. """
    
    LOCAL_MUSIC = "LOCAL_MUSIC"
    """ Local Computer Library Music Service source. """
    
    NOTIFICATION = "NOTIFICATION"
    """ NOTIFICATION source. """
    
    PANDORA = "PANDORA"
    """ Pandora Music Service source. """
    
    PRODUCT = "PRODUCT"
    """ PRODUCT source. """
    
    QPLAY = "QPLAY"
    """ QQMusic (QPlay) Music Service source. """
    
    SIRIUSXM = "SIRIUSXM"
    """ SiriusXM Music Service source. """
    
    SPOTIFY = "SPOTIFY"
    """ Spotify Music Service source. """
    
    STANDBY = "STANDBY"
    """ STANDBY source, which indicates the device is in standby mode. """
    
    STORED_MUSIC = "STORED_MUSIC"
    """ NAS Library Music Service source. """
    
    TUNEIN = "TUNEIN"
    """ TuneIn Music Service source. """
    
    UPDATE = "UPDATE"
    """ UPDATE source. """
