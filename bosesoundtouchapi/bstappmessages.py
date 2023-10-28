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

    ARGUMENT_REQUIRED_ERROR:str = "BST0002E - The \"{0}\" argument is required, and cannot be null / None."
    """
    BST0002E - The \"{0}\" argument is required, and cannot be null / None.
    """

    ARGUMENT_TYPE_ERROR:str = "BST0003E - {0} argument must be of type \"{1}\"; the \"{2}\" type is not supported for this argument."
    """
    BST0003E - {0} argument must be of type \"{1}\"; the \"{2}\" type is not supported for this argument.
    """

    BST_HOST_ADDRESS_INVALID:str = "BST1000E - SoundTouch host address is not recognized as a valid IPV4 network address: '%s'."
    """
    BST1000E - SoundTouch host address is not recognized as a valid IPV4 network address: '%s'.
    """
