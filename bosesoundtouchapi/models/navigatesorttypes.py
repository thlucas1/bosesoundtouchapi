# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class NavigateSortTypes(Enum):
    """
    Navigate Sort Types enumeration.
    """
    
    DateCreated = "dateCreated"
    """ Sort by date created. """
    
    StationName = "stationName"
    """ Sort by station name. """
