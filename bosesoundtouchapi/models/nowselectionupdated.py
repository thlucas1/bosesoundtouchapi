# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export
from ..bstconst import EVENT_DATEUTC, EVENT_DEVICE_ID
from .preset import Preset

@export
class NowSelectionUpdated:
    """
    SoundTouch device Now Selection Updated configuration object.
       
    This class contains the attributes and sub-items that represent the
    status of a selection update (usually a preset select) of the device.
    """

    def __init__(
        self, 
        root:Element=None
        ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
        """
        self._EventDeviceId:str = None
        self._EventDateUtc:int = 0
        self._Preset:Preset = None
                              
        if (root is None):
            
            pass
        
        else:

            # base node attribubtes.
            self._EventDeviceId = root.get(EVENT_DEVICE_ID)
            self._EventDateUtc = root.get(EVENT_DATEUTC, "0")

            # preset node.
            elmPreset = root.find("preset")
            if elmPreset is not None:
                self._Preset = Preset(root=elmPreset)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def EventDateUtc(self) -> str:
        """ 
        Date and time (in epoch format) of when the event took place.
        
        This is a helper property, and not part of the SoundTouch Web Services specification.
        """
        return self._EventDateUtc

    @EventDateUtc.setter
    def EventDateUtc(self, value:int):
        """ 
        Sets the EventDateUtc property value.
        """
        if isinstance(value, int) and value > -1:
            # convert it to a string value, so that it serializes correctly.
            self._EventDateUtc = str(value)

    
    @property
    def EventDeviceId(self) -> str:
        """ 
        Device identifier the configuration information was obtained from. 
        
        This is a helper property, and not part of the SoundTouch Web Services specification.
        """
        return self._EventDeviceId

    
    @property
    def PresetId(self) -> str:
        """ 
        The Preset Id that was selected if a preset node exists, otherwise null.

        This value will be zero if a non-preset source was selected (e.g. BLUETOOTH, AUXIN, etc).
        
        This is a helper property, and not part of the SoundTouch Web Services specification.
        """
        if (self._Preset is not None):
            return self._Preset.PresetId
        return None


    @property
    def Preset(self) -> 'Preset':
        """ 
        The selected Preset. 
        """
        return self._Preset


    @property
    def Source(self) -> str:
        """ 
        The ContentItem source that was selected.

        This is a helper property, and not part of the SoundTouch Web Services specification.
        """
        if (self._Preset is not None) and (self._Preset.ContentItem is not None):
            return self._Preset.ContentItem.Source
        return None


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'event_date_utc': self._EventDateUtc,
            'event_device_id': self._EventDeviceId,
            'preset': self._Preset.ToDictionary(),
        }
        return result
        

    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'NowSelectionUpdated:'
        if self._EventDateUtc is not None: msg = '%s EventDateUtc="%s"' % (msg, str(self._EventDateUtc))
        if self._EventDeviceId is not None and len(self._EventDeviceId) > 0: msg = '%s EventDeviceId="%s"' % (msg, str(self._EventDeviceId))
        if self._Preset is not None: msg = '%s\n %s' % (msg, self._Preset.ToString())
        return msg 
