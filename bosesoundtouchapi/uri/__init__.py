# import all classes from the namespace.
from .soundtouchnodes import SoundTouchNodes
from .soundtouchuri import SoundTouchUri
from .soundtouchuriscopes import SoundTouchUriScopes
from .soundtouchuritypes import SoundTouchUriTypes

# all classes to import when "import *" is specified.
__all__ = [
    'SoundTouchNodes',
    'SoundTouchUri',
    'SoundTouchUriScopes',
    'SoundTouchUriTypes'
]
