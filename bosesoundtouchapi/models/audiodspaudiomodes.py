# external package imports.
from enum import Enum

# our package imports.
from ..bstutils import export

@export
class AudioDspAudioModes(Enum):
    """
    Audio DSP Audio Modes enumeration.
    """
    
    Dialog = 'AUDIO_MODE_DIALOG'
    """
    Dialogue mode improves the clarity of dialogue and vocals in movies, 
    TV programs and podcasts by adjusting the tonal balance of the system.
    """

    Direct = 'AUDIO_MODE_DIRECT'
    """
    No optimizations made; the audio is directly from the source.
    """

    Night = 'AUDIO_MODE_NIGHT'
    """
    Audio Mode for a nighttime environment.
    """

    Normal = 'AUDIO_MODE_NORMAL'
    """
    Audio Mode for a normal environment.
    """

    Unspecified = 'AUDIO_MODE_UNSPECIFIED'
    """
    Audio Mode is not specified.
    """


    @staticmethod    
    def ToString(value) -> str:
        """ Returns the enum.value (instead of classname.value) as a string. """
        if isinstance(value, AudioDspAudioModes):
            return value.value
        return str(value)
