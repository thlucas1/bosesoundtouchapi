# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class ShuffleSettingTypes(Enum):
    """
    Shuffle Setting Types enumeration.
    """
    
    Off = 'SHUFFLE_OFF'
    """ Shuffle mode is off. """
    
    On = 'SHUFFLE_ON'
    """ Shuffle mode is on. """
