# external package imports.
from enum import Enum

# our package imports.
from .bstutils import export

@export
class SoundTouchItemTypes(Enum):
    """
    Item Types enumeration.
    """
    
    activity = "activity"

    album = "album"

    allTracks = "allTracks"

    artist = "artist"

    artistHeader = "artistHeader"

    artistRadio = "artistRadio"

    artistStation = "artistStation"

    chart = "chart"

    composer = ""

    directory = "dir"

    display = "display"

    episode = "episode"

    genre = "genre"

    locale = "locale"

    playall = "playall"

    playlist = "playlist"

    podcast = "podcast"

    previous = "previous"

    radio = "radio"

    recommendation = "recommendation"

    station = "station"

    stationurl = "stationurl"

    themedRadio = "themedRadio"

    topAlbum = "topAlbum"

    topArtist = "topArtist"

    topTrack = "topTrack"

    track = "track"

    tracklist = "tracklist"

    tracklistRadio = "tracklistRadio"

    tracklisturl = "tracklisturl"

    user = "user"
