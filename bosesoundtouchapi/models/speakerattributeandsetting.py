# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstappmessages import BSTAppMessages
from ..bstutils import export, _xmlGetAttrBool
from ..soundtoucherror import SoundTouchError
from ..soundtouchmodelrequest import SoundTouchModelRequest

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SISession
_logsi:SISession = SIAuto.Si.GetSession(__package__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__package__, True)
_logsi.SystemLogger = logging.getLogger(__package__)


@export
class SpeakerAttributeAndSetting(SoundTouchModelRequest):
    """
    SoundTouch device Speaker Attribute and Setting configuration object.
       
    This class contains the attributes and sub-items that represent a
    speaker attribute and setting configuration for the device.      
    """

    def __init__(self, controlType:str=None, 
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            controlType (str):
                Type of control the values represent (e.g. "rear", "subwoofer01", "subwoofer02", etc).
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchError:
                controlType argument was not of type str or was not supplied.  
        """
        self._ControlType:str = None
        self._Available:bool = None
        self._Active:bool = None
        self._Wireless:bool = None
        self._Controllable:bool = None
        
        if (root is None):
            
            # validations.
            if (controlType is None) or (not isinstance(controlType, str)):
                raise SoundTouchError(BSTAppMessages.ARGUMENT_TYPE_ERROR % ("controlType","str",str(type(controlType).__name__)), logsi=_logsi)

            self._ControlType = controlType
        
        else:

            self._ControlType = str(root.tag)
            self._Active = _xmlGetAttrBool(root, 'active')
            self._Available = _xmlGetAttrBool(root, 'available')
            self._Controllable = _xmlGetAttrBool(root, 'controllable')
            self._Wireless = _xmlGetAttrBool(root, 'wireless')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Active(self) -> bool:
        """ True if the speaker is active; otherwise, false. """
        return self._Active


    @property
    def Available(self) -> bool:
        """ True if the speaker is available; otherwise, false. """
        return self._Available

    @Available.setter
    def Available(self, value:bool):
        """ 
        Sets the Available property value.
        """
        if value != None:
            if isinstance(value, bool):
                self._Available = value


    @property
    def Controllable(self) -> bool:
        """ True if the speaker is controllable; otherwise, false. """
        return self._Controllable


    @property
    def ControlType(self) -> str:
        """ Type of control the values represent (e.g. "rear", "subwoofer01", "subwoofer02", etc). """
        return self._ControlType


    @property
    def IsAnyPropertySet(self) -> bool:
        """ True if any property besides ControlType is set in this object; otherwise, false. """
        return (self._Active is not None) \
            or (self._Available is not None) \
            or (self._Controllable is not None) \
            or (self._Wireless is not None)


    @property
    def Wireless(self) -> bool:
        """ True if the speaker is wireless; otherwise, false. """
        return self._Wireless


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class.
        
        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element(self._ControlType)
        if isRequestBody == True:
            # I don't think these properties can be updated.
            return elm
        
        if self._Active is not None: elm.set('active', str(self._Active).lower())
        if self._Available is not None: elm.set('available', str(self._Available).lower())
        if self._Wireless is not None: elm.set('wireless', str(self._Wireless).lower())
        if self._Controllable is not None: elm.set('controllable', str(self._Controllable).lower())
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = '%s:' % (self._ControlType)
        if self._Active is not None: msg = '%s Active="%s"' % (msg, str(self._Active).lower())
        if self._Available is not None: msg = '%s Available="%s"' % (msg, str(self._Available).lower())
        if self._Controllable is not None: msg = '%s Controllable="%s"' % (msg, str(self._Controllable).lower())
        if self._Wireless is not None: msg = '%s Wireless="%s"' % (msg, str(self._Wireless).lower())
        return msg 
