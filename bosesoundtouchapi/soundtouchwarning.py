# external package imports.
from smartinspectpython.sisession import SISession

# our package imports.
from .bstutils import export


@export
class SoundTouchWarning(Exception):
    """
    Exception thrown when a SoundTouch device returns a warning status.
    """
    def __init__(self, message:str, warningCode:int=0, logsi:SISession=None) -> None:
        """
        Initializes a new class instance using specified message text.

        Args:
            message (str):
                Warning message text.
            warningCode (int):
                Warning code value, that can uniquely identify this message.
            logsi (SISession):
                Trace session object that this exception will be logged to, or null to bypass trace logging.  
                Default is None.
        """
        
        # initialize base class.
        super().__init__(message)

        # initialize class instance.
        self._Message:str = message
        self._WarningCode:int = warningCode

        # trace.
        if logsi is not None:
            if (isinstance(logsi, SISession)):
                logsi.LogWarning(self.ToString())


    @property
    def Message(self) -> str:
        """ 
        Warning message text.
        """
        return self._Message


    @property
    def WarningCode(self) -> int:
        """ 
        Warning code value, that can uniquely identify this message.
        """
        return self._WarningCode


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchWarning:'
        msg = '%s "%s"' % (msg, str(self._Message))
        if self._WarningCode is not 0:
            msg = '%s, code="%s"' % (msg, str(self._WarningCode))
        return msg 
