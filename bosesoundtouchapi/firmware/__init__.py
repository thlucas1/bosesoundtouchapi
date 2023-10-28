# import all classes from the namespace.
from .soundtouchfirmware import SoundTouchFirmware
from .soundtouchfirmwareproduct import SoundTouchFirmwareProduct
from .soundtouchfirmwarerelease import SoundTouchFirmwareRelease

# all classes to import when "import *" is specified.
__all__ = [
    'SoundTouchFirmware',
    'SoundTouchFirmwareProduct',
    'SoundTouchFirmwareRelease',
]
