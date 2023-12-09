# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlGetAttrInt

@export
class ClockTime:
    """
    SoundTouch device ClockTime configuration object.
       
    This class contains the attributes and sub-items that represent the 
    clock time configuration of the device.
    """
    
    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        # base fields.
        self._UtcTime:int = None
        self._CueMusic:int = None
        self._TimeFormat:str = None
        self._Brightness:int = None
        self._ClockError:int = None
        self._UtcSyncTime:int = None

        # localtime node fields.
        self._Year:int = None
        self._Month:int = None
        self._Day:int = None
        self._DayOfWeek:int = None
        self._Hour:int = None
        self._Minute:int = None
        self._Second:int = None

        if (root is None):

            pass

        else:

            self._UtcTime = _xmlGetAttrInt(root, 'utcTime')
            self._CueMusic = _xmlGetAttrInt(root, 'cueMusic')
            self._TimeFormat = root.get('timeFormat')
            self._Brightness = _xmlGetAttrInt(root, 'brightness')
            self._ClockError = _xmlGetAttrInt(root, 'clockError')
            self._UtcSyncTime = _xmlGetAttrInt(root, 'utcSyncTime')

            # localtime node fields.
            elmNode = root.find('localTime')
            if (elmNode != None):
                self._Year = _xmlGetAttrInt(elmNode, 'year')
                self._Month = _xmlGetAttrInt(elmNode, 'month')
                self._Day = _xmlGetAttrInt(elmNode, 'dayOfMonth')
                self._DayOfWeek = _xmlGetAttrInt(elmNode, 'dayOfWeek')
                self._Hour = _xmlGetAttrInt(elmNode, 'hour')
                self._Minute = _xmlGetAttrInt(elmNode, 'minute')
                self._Second = _xmlGetAttrInt(elmNode, 'second')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Brightness(self) -> int:
        """ Brightness level of the clock display. """
        return self._Brightness


    @property
    def ClockError(self) -> int:
        """ TODO - document this property. """
        return self._ClockError


    @property
    def CueMusic(self) -> int:
        """ TODO - document this property. """
        return self._CueMusic


    @property
    def Day(self) -> int:
        """ Day (of month) portion of the local time value. """
        return self._Day


    @property
    def DayOfWeek(self) -> int:
        """ Day of week portion of the local time value. """
        return self._DayOfWeek


    @property
    def Hour(self) -> int:
        """ Hour portion of the local time value. """
        return self._Hour


    @property
    def Minute(self) -> int:
        """ Minute portion of the local time value. """
        return self._Minute


    @property
    def Month(self) -> int:
        """ Month portion of the local time value. """
        return self._Month


    @property
    def Second(self) -> int:
        """ Second portion of the local time value. """
        return self._Second


    @property
    def TimeFormat(self) -> str:
        """ 
        Time format with the following form: `TIME_FORMAT_xxHOUR_ID` (e.g.  
        "TIME_FORMAT_12HOUR_ID", "TIME_FORMAT_24HOUR_ID", etc).
        """       
        return self._TimeFormat


    @property
    def UtcSyncTime(self) -> int:
        """ Date and time (in epoch format) of when the device last syncronized its datetime. """
        return self._UtcSyncTime


    @property
    def UtcTime(self) -> int:
        """ Current UTC Date and time (in epoch format) of the device. """
        return self._UtcTime


    @property
    def Year(self) -> int:
        """ Year portion of the local time value. """
        return self._Year


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'ClockTime:'
        if self._Year is not None: msg = '%s LocalTime="%02d/%02d/%02d %02d:%02d:%02d"' % (msg, self._Year, self._Month, self._Day, self._Hour, self._Minute, self._Second)
        if self._DayOfWeek is not None: msg = '%s DayOfWeek=%d' % (msg, self._DayOfWeek)
        if self._TimeFormat is not None and len(self._TimeFormat) > 0: msg = '%s TimeFormat="%s"' % (msg, str(self._TimeFormat))
        if self._UtcTime is not None: msg = '%s UtcTime=%d' % (msg, self._UtcTime)
        if self._CueMusic is not None: msg = '%s CueMusic=%d' % (msg, self._CueMusic)
        if self._Brightness is not None: msg = '%s Brightness=%d' % (msg, self._Brightness)
        if self._ClockError is not None: msg = '%s ClockError=%d' % (msg, self._ClockError)
        if self._UtcSyncTime is not None: msg = '%s UtcSyncTime=%d' % (msg, self._UtcSyncTime)
        return msg 
