# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class GroupRoleTypes(Enum):
    """
    Group Role Types enumeration.
    """
    
    Left = 'LEFT'
    """ Group role is the left speaker. """
    
    Normal = 'NORMAL'
    """ Group role is a single speaker. """
    
    Right = 'RIGHT'
    """ Group role is the right speaker. """
    