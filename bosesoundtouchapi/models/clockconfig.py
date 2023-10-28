# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr

@export
class ClockConfig:
    """
    SoundTouch device ClockConfig configuration object.
       
    This class contains the attributes and sub-items that represent the 
    clock configuration of the device.      
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        if (root is None):
            pass  # no other parms to process.
        else:

            # base fields.
            self._BrightnessLevel:int = int(_xmlFindAttr(root, 'clockConfig', 'brightnessLevel', default='0'))
            self._TimeFormat:str = _xmlFindAttr(root, 'clockConfig', 'timeFormat')
            self._TimeZoneInfo:str = _xmlFindAttr(root, 'clockConfig', 'timezoneInfo')
            self._UserEnable:bool = _xmlFindAttr(root, 'clockConfig', 'userEnable', default='false') == True
            self._UserOffsetMinute:int = int(_xmlFindAttr(root, 'clockConfig', 'userOffsetMinute', default='0'))
            self._UserUtcTime:int = int(_xmlFindAttr(root, 'clockConfig', 'userUtcTime', default='0'))


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def BrightnessLevel(self) -> int:
        """ The brightness level of the clock display. """
        return self._BrightnessLevel


    @property
    def TimeFormat(self) -> str:
        """ 
        The time format with the following form: `TIME_FORMAT_xxHOUR_ID` (e.g.  
        "TIME_FORMAT_12HOUR_ID", "TIME_FORMAT_24HOUR_ID", etc).
        """
        return self._TimeFormat


    @property
    def TimeZoneInfo(self) -> str:
        """ The device's timezone. """
        return self._TimeZoneInfo


    @property
    def UserEnable(self) -> bool:
        """ A value indicating whether the timezone can be altered by a user. """
        return self._UserEnable


    @property
    def UserOffsetMinute(self) -> int:
        """ The offset in relation to the utc time. """
        return self._UserOffsetMinute


    @property
    def UserUtcTime(self) -> int:
        """ The current utc time. """
        return self._UserUtcTime


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'ClockConfig:'
        if self._TimeZoneInfo and len(self._TimeZoneInfo) > 0: msg = '%s timezoneInfo="%s"' % (msg, str(self._TimeZoneInfo))
        msg = '%s userEnable=%s' % (msg, str(self._UserEnable).lower())
        if self._TimeFormat and len(self._TimeFormat) > 0: msg = '%s timeFormat="%s"' % (msg, str(self._TimeFormat))
        msg = '%s userOffsetMinute=%d' % (msg, self._UserOffsetMinute)
        msg = '%s brightnessLevel=%d' % (msg, self._BrightnessLevel)
        msg = '%s userUtcTime=%d' % (msg, self._UserUtcTime)
        return msg 
