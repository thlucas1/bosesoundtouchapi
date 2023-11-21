# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindAttr

@export
class DSPMonoStereoItem:
    """
    SoundTouch device DSPMonoStereoItem configuration object.
       
    This class contains the attributes and sub-items that represent the 
    DSP mono / stereo configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._DeviceId:str = None
        self._IsMonoEnabled:bool = None
        
        if (root is None):

            pass

        else:

            self._DeviceId = root.get('deviceID')
            self._IsMonoEnabled = bool(_xmlFindAttr(root, 'mono', 'enable', default='false') == 'true')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ Device identifier. """
        return self._DeviceId

    
    @property
    def IsMonoEnabled(self) -> bool:
        """ 
        True if monophonic audio (audio from one single source) is enabled; otherwise, False
        to indicate stereophonic audio is enabled, which present the image of a 'left' and 
        'right' in the audio feed. 
        """
        return self._IsMonoEnabled

    
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'DSPMonoStereoItem:'
        if self._DeviceId and len(self._DeviceId) > 0: msg = '%s deviceId="%s"' % (msg, str(self._DeviceId))
        msg = '%s mono=%s' % (msg, str(self._IsMonoEnabled).lower())
        return msg
