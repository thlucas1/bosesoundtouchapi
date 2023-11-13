# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export
from ..soundtouchmodelrequest import SoundTouchModelRequest

@export
class SimpleConfig(SoundTouchModelRequest):
    """
    SoundTouch device SimpleConfig configuration object.
       
    This class contains the attributes and sub-items that represent a
    single-node xml-response item configuration of the device.
    """

    def __init__(self, configName:str=None, value:str=None, attribute:str=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            configName (str):
                The configuration name (or XML tag name when initializing the instance).
            value (str):
                The stored text value.
            attribute (str):
                The stored attributes.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        if (root is None):
            
            self._ConfigName:str = configName if configName else None
            self._Value:str = value if value else None
            self._Attribute:dict = attribute if attribute else None

        else:

            self._ConfigName:str = root.tag
            self._Value:str = root.text
            self._Attribute:dict = root.attrib


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def Attribute(self) -> dict:
        """ The stored attributes. """
        return self._Attribute


    @property
    def ConfigName(self) -> str:
        """ The configuration name (or XML tag name when initializing the instance). """
        return self._ConfigName


    @property
    def Value(self) -> str:
        """ The stored text value from the XML-Element. """
        return self._Value


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SimpleConfig:'
        if self._ConfigName and len(self._ConfigName) > 0: msg = '%s tag="%s"' % (msg, str(self._ConfigName))
        if self._Value and len(self._Value) > 0: msg = '%s value="%s"' % (msg, str(self._Value))
        if self._Attribute and len(self._Attribute) > 0: msg = '%s attr="%s"' % (msg, str(self._Attribute))
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
        return '<%s>%s</%s>' % (self._ConfigName, self._Value, self._ConfigName)
