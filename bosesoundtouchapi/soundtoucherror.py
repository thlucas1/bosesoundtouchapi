# external package imports.
from smartinspectpython.sisession import SISession

# our package imports.
from .bstutils import export


@export
class SoundTouchError(Exception):
    """
    Exception thrown when a SoundTouch device returns an error status for a command.
    """
    def __init__(self, message:str, name:str=None, severity:str=None, errorCode:int=0, logsi:SISession=None) -> None:
        """
        Initializes a new class instance using specified message text.

        Args:
            message (str):
                Message text, as reported by the element text of the error xml response.
            name (str):
                Name value, as reported by the "name" attribute of the error xml response.
            severity (str):
                Severity value, as reported by the "severity" attribute of the error xml response.
            errorCode (int):
                Error code value, as reported by the "value" attribute of the error xml response.
            logsi (SISession):
                Trace session object that this exception will be logged to, or null to bypass trace logging.  
                Default is None.
        """
        
        # initialize base class.
        super().__init__(message)

        # initialize class instance.
        self._ErrorCode:int = errorCode
        self._Message:str = message
        self._Name:str = name
        self._Severity:str = severity

        # trace.
        if logsi is not None:
            if (isinstance(logsi, SISession)):
                logsi.LogError(self.ToString())


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ErrorCode(self) -> int:
        """ 
        Error code value, as reported by the "value" attribute of the error xml response.
        
        Examples: "401", "415", etc.
        """
        return self._ErrorCode


    @property
    def Message(self) -> str:
        """ 
        Message text, as reported by the element text of the error xml response.
        """
        return self._Message


    @property
    def Name(self) -> str:
        """ 
        Name value, as reported by the "name" attribute of the error xml response.
        
        Examples: "HTTP_STATUS_UNAUTHORIZED", "HTTP_STATUS_UNSUPPORTED_MEDIA_TYPE", etc.
        """
        return self._Name


    @property
    def Severity(self) -> str:
        """ 
        Severity value, as reported by the "severity" attribute of the error xml response.
        
        Examples: "Unknown"
        """
        return self._Severity


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchError:'
        msg = '%s "%s"' % (msg, str(self._Message))
        if self._ErrorCode != 0: msg = '%s, code="%s"' % (msg, str(self._ErrorCode))
        if self._Name != None: msg = '%s, name="%s"' % (msg, str(self._Name))
        if self._Severity != None: msg = '%s, severity="%s"' % (msg, str(self._Severity))
        return msg 
