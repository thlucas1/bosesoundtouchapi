# external package imports.
from enum import Enum

# our package imports.
from .bstutils import export

@export
class SoundTouchAudioModes(Enum):
    """
    SoundTouch Audio Modes.
    """
    
    DIALOG = 'AUDIO_MODE_DIALOG'
    """
    Dialogue mode improves the clarity of dialogue and vocals in movies, 
    TV programs and podcasts by adjusting the tonal balance of the system.
    """

    DIRECT = 'AUDIO_MODE_DIRECT'
    """
    No optimizations made; the audio is directly from the source.
    """

    NIGHT = 'AUDIO_MODE_NIGHT'
    """
    Audio Mode for a nighttime environment.
    """

    NORMAL = 'AUDIO_MODE_NORMAL'
    """
    Audio Mode for a normal environment.
    """

    UNSPECIFIED = 'AUDIO_MODE_UNSPECIFIED'
    """
    Audio Mode is not specified.
    """


    @staticmethod    
    def ToString(value) -> str:
        """ Returns the enum.value (instead of classname.value) as a string. """
        if isinstance(value, SoundTouchAudioModes):
            return value.value
        return str(value)
