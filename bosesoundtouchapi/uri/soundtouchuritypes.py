# external package imports.
from enum import Enum

# our package imports.
from bosesoundtouchapi.bstutils import export


@export
class SoundTouchUriTypes(Enum):
    """ 
    SoundTouch URI types.
    """

    OP_TYPE_EVENT = 0x04
    """
    URIs that are used to capture events can not be queried with a client.
    Therefore, the BoseWebSocket should be used.
    """

    OP_TYPE_REQUEST = 0x08
    """
    Standard URI type.
    """
