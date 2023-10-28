# external package imports.
from smartinspectpython.sisession import SISession

# our package imports.
from .bstutils import export


@export
class SoundTouchException(Exception):
    """
    Exception thrown if a non-fatal application error occurs.
    """
    def __init__(self, message:str, innerException:Exception=None, logsi:SISession=None) -> None:
        """
        Initializes a new class instance using specified message text.

        Args:
            message (str):
                Exception message text.
            innerException (Exception):
                If specified, the exception that caused this exception.  
                Default is None.
            logsi (SISession):
                Trace session object that this exception will be logged to, or null to bypass trace logging.  
                Default is None.
        """

        # initialize base class.
        super().__init__(message)

        # initialize class instance.
        self._Message:str = message
        self._MessageId:str = ""
        self._InnerException:str = innerException

        # check for message identifier prefix (e.g. "BST0005E - xxx").
        if (message) and (len(message) > 8):
            if (message.startswith("BST")):
                if (message[7:8] == "E") or (message[7:8] == "I"):
                    self._MessageId = message[0:8]  # BST0005E

        # trace.
        if (logsi):
            if (isinstance(logsi, SISession)):
                if (innerException):
                    logsi.LogException(message, innerException)
                else:
                    logsi.LogError(message)


    @property
    def InnerException(self) -> Exception:
        """ 
        If specified, the exception that caused this exception.  
        Default is None.

        Returns:
            The InnerException property value.
        """
        return self._InnerException


    @property
    def Message(self) -> str:
        """ 
        Exception message text.

        Returns:
            The Message property value.
        """
        return self._Message


    @property
    def MessageId(self) -> str:
        """ 
        Exception message identifier.

        Returns:
            The Message property value.
        """
        return self._MessageId
