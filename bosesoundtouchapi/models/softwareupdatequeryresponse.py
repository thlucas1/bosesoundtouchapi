# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind

@export
class SoftwareUpdateQueryResponse:
    """
    SoundTouch device SoftwareUpdateQueryResponse configuration object.
       
    This class contains the attributes and sub-items that represent a
    software update query response.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._CanAbort:bool = None
        self._DeviceId:str = None
        self._FailureCode:str = None
        self._FailureId:str = None
        self._PercentComplete:int = None
        self._State:str = None

        if (root is None):

            pass

        else:

            self._DeviceId = root.get('deviceID')
            self._CanAbort = _xmlFind(root, "canAbort") == 'true'
            self._FailureCode = _xmlFind(root, 'failureCode')
            self._FailureId = _xmlFind(root, 'failureId')
            self._PercentComplete = int(_xmlFind(root, 'percentComplete'))
            self._State = _xmlFind(root, 'state')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId


    @property
    def CanAbort(self) -> bool:
        """ True if the software update can be aborted; otherwise, False. """
        return self._CanAbort


    @property
    def FailureCode(self) -> str:
        """ 
        Failure code value, if the software update failed.
        """
        return self._FailureCode


    @property
    def FailureId(self) -> str:
        """ 
        Failure id value, if the software update failed.
        """
        return self._FailureId


    @property
    def HasFailed(self) -> bool:
        """ 
        True if the software update failed; otherwise, False.
        """
        return (self._FailureCode is not None) or (self._FailureId is not None)


    @property
    def PercentComplete(self) -> int:
        """ Denotes the progress percent to completion (0 - 100). """
        return self._PercentComplete


    @property
    def State(self) -> str:
        """ 
        Current state of the software update: "IDLE", "DOWNLOADING", "AUTHENTICATING",
        "INSTALLING", "COMPLETED", "CHECKING". 
        """
        return self._State


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoftwareUpdateQueryResponse:'
        if self._DeviceId is not None and len(self._DeviceId) > 0: msg = '%s DeviceId="%s"' % (msg, self._DeviceId)
        if self._PercentComplete is not None: msg = '%s PercentComplete="%s"' % (msg, str(self._PercentComplete))
        if self._CanAbort is not None: msg = '%s CanAbort="%s"' % (msg, str(self._CanAbort).lower())
        if self._State is not None and len(self._State) > 0: msg = '%s State="%s"' % (msg, self._State)
        msg = '%s HasFailed="%s"' % (msg, str(self.HasFailed).lower())
        if self._FailureCode is not None and len(self._FailureCode) > 0: msg = '%s FailureCode="%s"' % (msg, self._FailureCode)
        if self._FailureId is not None and len(self._FailureId) > 0: msg = '%s FailureId="%s"' % (msg, self._FailureId)
        return msg
