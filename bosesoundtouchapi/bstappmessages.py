# external package imports.
# none

# our package imports.
from .bstutils import export


@export
class BSTAppMessages:
    """
    A strongly-typed resource class, for looking up localized strings, etc.
    
    Threadsafety:
        This class is fully thread-safe.
    """

    UNHANDLED_EXCEPTION:str = "BST0001E - An unhandled exception occured while processing method \"{0}\".\n{1}\n"
    """
    BST0001E - An unhandled exception occured while processing method \"{0}\".
    {1}
    """

    ARGUMENT_REQUIRED_ERROR:str = "BST0002E - The '%s' argument is required, and cannot be null / None."
    """
    BST0002E - The '%s' argument is required, and cannot be null / None.
    """

    ARGUMENT_TYPE_ERROR:str = "BST0003E - '%s' argument must be of type '%s'; the '%s' type is not supported for this argument."
    """
    BST0003E - '%s' argument must be of type '%s'; the '%s' type is not supported for this argument.
    """

    BST_HOST_ADDRESS_INVALID:str = "BST1000E - SoundTouch host address is not recognized as a valid IPV4 network address: '%s'."
    """
    BST1000E - SoundTouch host address is not recognized as a valid IPV4 network address: '%s'.
    """

    BST_DEVICE_NOT_CAPABLE_FUNCTION:str = "BST1001E - '%s': device is not capable of processing '%s' functions"
    """
    BST1001E - '%s': device is not capable of processing '%s' functions".
    """
    
    BST_WEBSERVICES_API_ERROR:str = "BST1002E - '%s': SoundTouch Web-services API returned an error status: '%s'"
    """
    BST1002E - '%s': SoundTouch Web-services API returned an error status: '%s'
    """
    
    BST_WEBSOCKET_EVENTHANDLER_ERROR:str = "BST1003E - '%s': SoundTouchWebSocket eventhandler exception: %s"
    """
    BST1003E - '%s': SoundTouchWebSocket eventhandler exception: %s
    """

    