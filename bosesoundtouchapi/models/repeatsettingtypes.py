# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class RepeatSettingTypes(Enum):
    """
    Repeat Setting Types enumeration.
    """
    
    All = 'REPEAT_ALL'
    """ Repeat all tracks. """
    
    Off = 'REPEAT_OFF'
    """ Repeat is off. """
    
    One = 'REPEAT_ONE'
    """ Repeat one track. """
    