# import all classes from the namespace.
from .soundtouchfirmware import SoundTouchFirmware, BOSE_SOUNDTOUCH_UPDATE_INDEX_URL
from .soundtouchfirmwareproduct import SoundTouchFirmwareProduct
from .soundtouchfirmwarerelease import SoundTouchFirmwareRelease

# all classes to import when "import *" is specified.
__all__ = [
    'BOSE_SOUNDTOUCH_UPDATE_INDEX_URL',
    'SoundTouchFirmware',
    'SoundTouchFirmwareProduct',
    'SoundTouchFirmwareRelease',
]
