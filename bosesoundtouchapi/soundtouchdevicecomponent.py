# external package imports.
# none

# our package imports.
from .bstutils import export


class SoundTouchDeviceComponent:
    """ 
    A small wrapper class to store component related data.
    """

    def __init__(self, category:str=None, softwareVersion:str=None, serialNumber:str=None) -> None:
        """
        Initiallizes a new instance of the class.

        Args:
            category (str):
                A simple string used to identify the component object.
            softwareVersion (str):
                If present, this attribute contains the current version the software
                is running with.
            serialNumber (str):
                This string contains a serial number, if present.
        """
        self._Category:str = category
        self._SoftwareVersion = softwareVersion
        self._SerialNumber = serialNumber


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Category(self) -> str:
        """ A simple string used to identify the component object. """
        return self._Category


    @property
    def SerialNumber(self) -> str:
        """
        If present, this attribute contains the current version the software is 
        running with.
        """
        return self._SerialNumber


    @property
    def SoftwareVersion(self) -> str:
        """ This string contains a serial number, if present. """
        return self._SoftwareVersion


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchDeviceComponent:'
        msg = "%s Category='%s'" % (msg, self._Category)
        msg = "%s SerialNumber='%s'" % (msg, self._SerialNumber)
        msg = "%s SoftwareVersion='%s'" % (msg, self._SoftwareVersion)
        return msg
