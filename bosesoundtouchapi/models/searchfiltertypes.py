# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class SearchFilterTypes(Enum):
    """
    Search Filter Types enumeration.
    """
    
    Album = "album"

    Artist = "artist"

    AutoComplete = "autocomplete"

    Genre = "genre"

    Language = "language"

    Library = "library"

    Location = "location"

    NameStation = "namestation"

    Track = "track"
