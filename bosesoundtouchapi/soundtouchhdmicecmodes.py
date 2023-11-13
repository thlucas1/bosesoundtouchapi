# external package imports.
from enum import Enum

# our package imports.
from .bstutils import export

@export
class SoundTouchHdmiCecModes(Enum):
    """
    SoundTouch HDMI CEC Modes.
    """
    
    ALTERNATE = 'CEC_MODE_ALTERNATE'
    """
    HDMI CEC mode is alternate.
    """

    FINE = 'CEC_MODE_FINE'
    """
    HDMI CEC mode is fine.
    """

    OFF = 'CEC_MODE_OFF'
    """
    HDMI CEC mode is off.
    """

    ON = 'CEC_MODE_ON'
    """
    HDMI CEC mode is on.
    """


    @staticmethod    
    def ToString(value) -> str:
        """ Returns the enum.value (instead of classname.value) as a string. """
        if isinstance(value, SoundTouchHdmiCecModes):
            return value.value
        return str(value)
