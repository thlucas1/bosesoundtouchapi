# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind

@export
class Service:
    """
    SoundTouch device Service configuration object.
       
    This class contains the attributes and sub-items that represent a
    service configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        
        # initialize storage.
        self._IsAvailable:bool = None
        self._Reason:str = None
        self._ServiceType:str = None
        
        if (root is None):
            
            pass  # no other parms to process.
        
        else:

            # base fields.
            self._IsAvailable = bool(root.get('isAvailable', default='false') == 'true')
            self._Reason = root.get('reason', default=None)
            self._ServiceType = root.get('type', default=None)


    def __repr__(self) -> str:
        return self.ToString()


    # implement sorting support.
    def __eq__(self, other):
        try:
            return self.ServiceType == other.ServiceType
        except Exception as ex:
            if (isinstance(self, Service )) and (isinstance(other, Service )):
                return self.ServiceType == other.ServiceType
            return False

    def __lt__(self, other):
        try:
            # the following comparison will fail if the property value is None!  
            # use the following syntax when calling a sort method that uses lambda searches:
            # epColl.sort(ServiceType=lambda x: x.ServiceType or "", reverse=False)     <- GOOD syntax
            # epColl.sort(ServiceType=lambda x: x.ServiceType, reverse=False)           <- BAD syntax, as the "x.ServiceType" property may be None, and will cause this to fail!
            return self.ServiceType < other.ServiceType
        except Exception as ex:
            if (isinstance(self, Service )) and (isinstance(other, Service )):
                return self.ServiceType < other.ServiceType
            return False


    @property
    def IsAvailable(self) -> bool:
        """ True if the service is currently available; otherwise, False. """       
        return self._IsAvailable


    @property
    def Reason(self) -> str:
        """ Reason why the service is unavailable (e.g. "INVALID_SOURCE_TYPE", etc). """
        return self._Reason


    @property
    def ServiceType(self) -> str:
        """ Service type value (e.g. "BLUETOOTH", "SPOTIFY", etc). """
        return self._ServiceType


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Service:'
        if self._ServiceType is not None and len(self._ServiceType) > 0: msg = '%s type="%s"' % (msg, self._ServiceType)
        if self._IsAvailable is not None: msg = '%s isAvailable="%s"' % (msg, str(self._IsAvailable).lower())
        if self._Reason is not None and len(self._Reason) > 0: msg = '%s reason="%s"' % (msg, self._Reason)
        return msg