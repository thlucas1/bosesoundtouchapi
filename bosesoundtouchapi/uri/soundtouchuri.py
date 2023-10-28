# external package imports.
# none

# our package imports.
from .soundtouchuriscopes import SoundTouchUriScopes
from .soundtouchuritypes import SoundTouchUriTypes
from bosesoundtouchapi.bstutils import export


@export
class SoundTouchUri:
    """
    A SoundTouchUri object can be used in several ways. Since, the object can not
    be edited, there is no editing available.

    The __str__ and __repr__ method will return the assigned path name (created when
    initiating a new instance).
    """
    
    def __init__(self, 
                 path:str,
                 scope:SoundTouchUriScopes = SoundTouchUriScopes.OP_SCOPE_PUBLIC,
                 uriType:SoundTouchUriTypes = SoundTouchUriTypes.OP_TYPE_REQUEST
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            path (str):
                The target uri which will be formatted into the url in a request.
            scope (SoundTouchUriScope):
                The scope of this URI object. If it is private, the client may not
                request the resource.
            uriType (SoundTouchUriType):
                Defines the type of this uri; it can be either 'request' or 'event'.
        """
        self._Path = path
        self._Scope = scope
        self._UriType = uriType


    def __repr__(self) -> str:
        return self.__str__()


    def __str__(self) -> str:
        return self._Path


    def __eq__(self, __o: object) -> bool:
        return self._Path.__eq__(__o)


    def __len__(self) -> int:
        return self._Path.__len__()


    def __getitem__(self, key):
        return self._Path[key]


    @property
    def Path(self) -> str:
        """ The target uri which will be formatted into the url in a request. """
        return self._Path


    @property
    def Scope(self) -> str:
        """ 
        The scope of this URI object. If it is private, the client may not request 
        the resource.
        """
        return self._Scope


    @property
    def UriType(self) -> str:
        """ Defines the type of this uri; it can be either 'request' or 'event'. """
        return self._UriType

