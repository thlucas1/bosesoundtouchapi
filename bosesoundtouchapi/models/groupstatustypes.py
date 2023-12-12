# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class GroupStatusTypes(Enum):
    """
    Group Status Types enumeration.
    """
    
    Unknown = 'GROUP_UNKNOWN'
    """ Status is not known at this time. """

    Connecting = 'GROUP_CONNECTING'
    """ Group is currently connecting. """

    Ok = 'GROUP_OK'
    """ Group is functioning as expected. """

    OkMargeOnly = 'GROUP_OK_MARGE_ONLY'

    MargeRequestFailed = 'GROUP_MARGE_REQUEST_FAILED'

    PeerRequestFailed = 'GROUP_PEER_REQUEST_FAILED'

    Error = 'GROUP_ERROR'
    """ An error occured. """
