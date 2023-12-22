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
    def GetNameByValue(value:str) -> str:
        """
        Returns a name for the given audioMode value.
        No exception will be thrown by this method if the value is not found.
        
        Args:
            value (str):
                The audio mode value (e.g. "AUDIO_MODE_NORMAL", etc).
                Value is case-sensitive, and must match exactly.
                
        Returns:
            A name if the value argument was found; otherwise, None.
        """
        if value is None:
            return None
        
        item:str
        for item in AudioDspAudioModes:
            if value == item.value:
                return item.name
        return None
        

    @staticmethod    
    def GetValueByName(name:str) -> str:
        """
        Returns a value for the given audioMode name.
        No exception will be thrown by this method if the name is not found.
        
        Args:
            name (str):
                The audio mode name (e.g. "Normal", "Dialog", etc).
                Value is case-sensitive, and must match exactly.
                
        Returns:
            A value if the name argument was found; otherwise, None.
        """
        if name is None:
            return None
        
        item:str
        for item in AudioDspAudioModes:
            if name == item.name:
                return item.value
        return None
        

    @staticmethod    
    def ToString(value) -> str:
        """ Returns the enum.value (instead of classname.value) as a string. """
        if isinstance(value, AudioDspAudioModes):
            return value.value
        return str(value)
