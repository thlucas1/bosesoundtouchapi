# external package imports.
from enum import Enum

# our package imports.
from .bstutils import export

@export
class SoundTouchItemTypes(Enum):
    """
    Item Types enumeration.
    """
    
    Activity = "activity"

    Album = "album"

    AllTracks = "allTracks"

    Artist = "artist"

    ArtistHeader = "artistHeader"

    ArtistRadio = "artistRadio"

    ArtistStation = "artistStation"

    Chart = "chart"

    Composer = ""

    Directory = "dir"

    Display = "display"

    Episode = "episode"

    Genre = "genre"

    Locale = "locale"

    Playall = "playall"

    Playlist = "playlist"

    Podcast = "podcast"

    Previous = "previous"

    Radio = "radio"

    Recommendation = "recommendation"

    Station = "station"

    StationUrl = "stationurl"

    ThemedRadio = "themedRadio"

    TopAlbum = "topAlbum"

    TopArtist = "topArtist"

    TopTrack = "topTrack"

    Track = "track"

    Tracklist = "tracklist"

    TracklistRadio = "tracklistRadio"

    TracklistUrl = "tracklisturl"

    User = "user"
