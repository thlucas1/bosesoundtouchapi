# external package imports.
from enum import Enum

# our package imports.
from bosesoundtouchapi.bstutils import export


@export
class SoundTouchUriScopes(Enum):
    """ 
    SoundTouch URI scopes.
    """

    OP_SCOPE_PUBLIC = 0x00
    """
    URIs that are public and can be accessed by everyone will be declared
    with OP_SCOPE_PUBLIC.
    """

    OP_SCOPE_PRIVATE = 0x01
    """
    URIs that are private and can not be accessed by everyone.
    """
