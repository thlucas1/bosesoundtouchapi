# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstappmessages import BSTAppMessages
from ..bstutils import export
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
class ControlLevelInfo(SoundTouchModelRequest):
    """
    SoundTouch device generic Control Level Info configuration object.
       
    This class contains the attributes and sub-items that represent a
    control value configuration for the device.      
    """

    def __init__(self, controlType:str=None, value:int=None, minValue:int=None, maxValue:int=None, step:int=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            controlType (str):
                Type of control the values represent (e.g. "bass", "treble", etc).
            value (int):
                The current value of the tone control.
            minValue (int):
                The minimum allowed value.
            maxValue (int):
                The maximum allowed value.
            step (int):
                The amount the value can increase or decrease at a time.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchError:
                controlType argument was not of type str or was not supplied.  
                value argument was not of type int.  
                minValue argument was not of type int.  
                maxValue argument was not of type int.  
                step argument was not of type int.  
        """
        # initialize storage.
        self._ControlType:str = None
        self._Value:int = None
        self._MinValue:int = None
        self._MaxValue:int = None
        self._Step:int = None
        
        if (root is None):
            
            # validations.
            if (controlType is None) or (not isinstance(controlType, str)):
                raise SoundTouchError(BSTAppMessages.ARGUMENT_TYPE_ERROR % ("controlType","str",str(type(controlType).__name__)), logsi=_logsi)
            if (value is not None) and (not isinstance(value, int)):
                raise SoundTouchError(BSTAppMessages.ARGUMENT_TYPE_ERROR % ('value','int',str(type(value).__name__)), logsi=_logsi)
            if (minValue is not None) and (not isinstance(minValue, int)):
                raise SoundTouchError(BSTAppMessages.ARGUMENT_TYPE_ERROR % ('minValue','int',str(type(minValue).__name__)), logsi=_logsi)
            if (maxValue is not None) and (not isinstance(maxValue, int)):
                raise SoundTouchError(BSTAppMessages.ARGUMENT_TYPE_ERROR % ('maxValue','int',str(type(maxValue).__name__)), logsi=_logsi)
            if (step is not None) and (not isinstance(step, int)):
                raise SoundTouchError(BSTAppMessages.ARGUMENT_TYPE_ERROR % ('step','int',str(type(step).__name__)), logsi=_logsi)

            # base fields.
            self._ControlType = controlType
            self._Value = value
            self._MinValue = minValue
            self._MaxValue = maxValue
            self._Step = step
        
        else:

            # base fields.
            self._ControlType = str(root.tag)
            self._Value = int(root.get('value', default=0))
            self._MinValue = int(root.get('minValue', default=0))
            self._MaxValue = int(root.get('maxValue', default=0))
            self._Step = int(root.get('step', default=0))


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def ControlType(self) -> str:
        """ Type of control the values represent (e.g. "bass", "treble", etc). """
        return self._ControlType


    @property
    def MinValue(self) -> int:
        """ The minimum allowed value. """
        return self._MinValue


    @property
    def MaxValue(self) -> int:
        """ The maximum allowed value. """
        return self._MaxValue


    @property
    def Step(self) -> int:
        """ The amount the value can increase or decrease at a time. """
        return self._Step


    @property
    def Value(self) -> int:
        """ The current value of the tone control. """
        return self._Value

    @Value.setter
    def Value(self, value:int):
        """ 
        Sets the Value property value.
        """
        if value != None:
            if isinstance(value, int):
                self._Value = value


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class.
        
        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element(self._ControlType)
        if self._Value is not None: elm.set('value', str(self._Value))
        if isRequestBody == True:
            return elm
        
        if self._MinValue is not None: elm.set('minValue', str(self._MinValue))
        if self._MaxValue is not None: elm.set('maxValue', str(self._MaxValue))
        if self._Step is not None: elm.set('step', str(self._Step))
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = '%s:' % (self._ControlType)
        msg = '%s Value="%s"' % (msg, str(self._Value))
        msg = '%s MinValue="%s"' % (msg, str(self._MinValue))
        msg = '%s MaxValue="%s"' % (msg, str(self._MaxValue))
        msg = '%s Step="%s"' % (msg, str(self._Step))
        return msg 


    def ToXmlRequestBody(self, encoding:str='utf-8') -> str:
        """ 
        Overridden.
        Returns a POST request body, which is used to update the device configuration.
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.

        Returns:
            An xml string that can be used in a POST request to update the
            device configuration.
        """
        elm = self.ToElement(True)
        xml = tostring(elm, encoding='unicode')
        return xml
