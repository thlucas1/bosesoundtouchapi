# include the README.md file for pdoc documentation generation.
"""
.. include:: ../README.md

_________________

<details>
  <summary>View Change Log</summary>
.. include:: ../CHANGELOG.md
</details>
"""

# our package imports.
from bosesoundtouchapi.soundtouchaudiomodes import SoundTouchAudioModes
from bosesoundtouchapi.soundtouchclient import SoundTouchClient
from bosesoundtouchapi.soundtouchdevice import SoundTouchDevice
from bosesoundtouchapi.soundtouchdiscovery import SoundTouchDiscovery
from bosesoundtouchapi.soundtoucherror import SoundTouchError
from bosesoundtouchapi.soundtouchexception import SoundTouchException
from bosesoundtouchapi.soundtouchhdmicecmodes import SoundTouchHdmiCecModes
from bosesoundtouchapi.soundtouchkeys import SoundTouchKeys
from bosesoundtouchapi.soundtouchmessage import SoundTouchMessage
from bosesoundtouchapi.soundtouchnotifycategorys import SoundTouchNotifyCategorys
from bosesoundtouchapi.soundtouchsources import SoundTouchSources
from bosesoundtouchapi.soundtouchwarning import SoundTouchWarning

# all classes to import when "import *" is specified.
__all__ = [
    'SoundTouchAudioModes',
    'SoundTouchClient',
    'SoundTouchDevice',
    'SoundTouchDiscovery',
    'SoundTouchError',
    'SoundTouchException',
    'SoundTouchHdmiCecModes',
    'SoundTouchKeys',
    'SoundTouchMessage',
    'SoundTouchNotifyCategorys',
    'SoundTouchSources',
    'SoundTouchWarning'
]
