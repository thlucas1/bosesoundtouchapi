# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class KeyStates(Enum):
    """
    Key States enumeration.
    """
    
    Both = 'both'
    """
    Indicates a key is to be pressed and released.
    """

    Press = 'press'
    """
    Indicates a key is to be pressed.
    """

    Release = 'release'
    """
    Indicates a key is to be released.
    """


    @staticmethod    
    def ToString(value) -> str:
        """ Returns the enum.value (instead of classname.value) as a string. """
        if isinstance(value, KeyStates):
            return value.value
        return str(value)
