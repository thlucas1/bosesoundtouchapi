# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindBool

@export
class PowerManagement:
    """
    SoundTouch device PowerManagement configuration object.
       
    This class contains the attributes and sub-items that represent the
    power management status configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._BatteryCapable:bool = None
        self._State:str = None

        if (root is None):

            pass

        else:

            self._BatteryCapable = _xmlFindBool(root, 'capable')
            self._State = _xmlFind(root, 'powerState')
        
            if (self._BatteryCapable is None):
                elmNode = root.find('battery')
                if (elmNode != None):
                    self._BatteryCapable = _xmlFindBool(elmNode, 'capable')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def BatteryCapable(self) -> bool:
        """ True if the device is capable of being powered via a battery; otherwise, False. """
        return self._BatteryCapable


    @property
    def State(self) -> str:
        """ Current state of the power supplied (e.g. "FullPower", etc). """
        return self._State


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'battery_capable': self._BatteryCapable,
            'state_value': self._State,
        }
        return result
        

    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'PowerManagement:'
        if self._State is not None and len(self._State) > 0: msg = '%s state="%s"' % (msg, str(self._State))
        if self._BatteryCapable is not None: msg = '%s batteryCapable=%s' % (msg, str(self._BatteryCapable).lower())
        return msg
