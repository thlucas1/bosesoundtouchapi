# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFindAttr

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

            # base fields.
            self._UtcTime = int(root.get('utcTime', default='0'))
            self._CueMusic = int(root.get('cueMusic', default='0'))
            self._TimeFormat = root.get('timeFormat')
            self._Brightness = int(root.get('brightness', default='0'))
            self._ClockError = int(root.get('clockError', default='0'))
            self._UtcSyncTime = int(root.get('utcSyncTime', default='0'))

            # localtime node fields.
            self._Year = int(_xmlFindAttr(root, 'localTime', 'year', default='0'))
            self._Month = int(_xmlFindAttr(root, 'localTime', 'month', default='0'))
            self._Day = int(_xmlFindAttr(root, 'localTime', 'dayOfMonth', default='0'))
            self._DayOfWeek = int( _xmlFindAttr(root, 'localTime', 'dayOfWeek', default='0'))
            self._Hour = int(_xmlFindAttr(root, 'localTime', 'hour', default='0'))
            self._Minute = int(_xmlFindAttr(root, 'localTime', 'minute', default='0'))
            self._Second = int(_xmlFindAttr(root, 'localTime', 'second', default='0'))


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
        msg = '%s localTime="%02d/%02d/%02d %02d:%02d:%02d"' % (msg, self._Year, self._Month, self._Day, self._Hour, self._Minute, self._Second)
        if self._TimeFormat and len(self._TimeFormat) > 0: msg = '%s timeFormat="%s"' % (msg, str(self._TimeFormat))
        msg = '%s utcTime=%d' % (msg, self._UtcTime)
        msg = '%s cueMusic=%d' % (msg, self._CueMusic)
        msg = '%s brightness=%d' % (msg, self._Brightness)
        msg = '%s clockError=%d' % (msg, self._ClockError)
        msg = '%s utcSyncTime=%d' % (msg, self._UtcSyncTime)
        return msg 
