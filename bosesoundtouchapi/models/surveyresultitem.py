# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr

@export
class SurveyResultItem:
    """
    SoundTouch device SurveyResultItem configuration object.
       
    This class contains the attributes and sub-items that represent a
    single survey result item configuration of the device.
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
        self._Secure:bool = None
        self._SecurityTypes:list[str] = None
        self._SignalStrength:int = None
        self._Ssid:str = None
        
        if (root is None):

            pass
        
        else:

            # base fields.
            self._Secure:bool = root.get("secure") == 'true'
            self._SecurityTypes:list[str] = []
            self._SignalStrength:int = root.get('signalStrength')
            self._Ssid:str = root.get('ssid')
            
            # load all security types.
            elmSecurityTypes:Element = root.find('securityTypes')
            if elmSecurityTypes is not None:
                elmSecurityType:Element
                for elmSecurityType in elmSecurityTypes.findall('type'):
                    self._SecurityTypes.append(elmSecurityType.text)
                

    def __repr__(self) -> str:
        return self.ToString()


    # implement sorting support.
    def __eq__(self, other):
        try:
            return self.Ssid == other.Ssid
        except Exception as ex:
            if (isinstance(self, SurveyResultItem )) and (isinstance(other, SurveyResultItem )):
                return self.Ssid == other.Ssid
            return False

    def __lt__(self, other):
        try:
            return self.Ssid < other.Ssid
        except Exception as ex:
            if (isinstance(self, SurveyResultItem )) and (isinstance(other, SurveyResultItem )):
                return self.Ssid < other.Ssid
            return False


    @property
    def Secure(self) -> bool:
        """ True if the discovered network service requires a secure connection; otherwise, False. """
        return self._Secure


    @property
    def SecurityTypes(self) -> list[str]:
        """ List of security types that the discovered network service requires for connectivity. """
        return self._SecurityTypes


    @property
    def SignalStrength(self) -> int:
        """ Signal strength of the discovered wireless network. """
        return self._SignalStrength


    @property
    def Ssid(self) -> str:
        """ Network service set identifier (SSID) of the discovered wireless network. """
        return self._Ssid


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SurveyResultItem:'
        if self._Ssid is not None and len(self._Ssid) > 0: msg = '%s ssid="%s"' % (msg, str(self._Ssid))
        if self._Secure is not None: msg = '%s secure="%s"' % (msg, str(self._Secure))
        if self._SignalStrength is not None: msg = '%s signalStrength="%s"' % (msg, str(self._SignalStrength))
        if self._SecurityTypes is not None and len(self._SecurityTypes) > 0: msg = '%s securityTypes="%s"' % (msg, str(self._SecurityTypes))
        return msg
