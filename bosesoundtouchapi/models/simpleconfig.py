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
        self._Attribute:dict = None
        self._ConfigName:str = None
        self._Value:str = None

        if (root is None):
            
            self._Attribute = str(attribute)
            self._ConfigName = str(configName)
            self._Value = str(value)

        else:

            self._Attribute = root.attrib
            self._ConfigName = root.tag
            self._Value = root.text


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Attribute(self) -> dict:
        """ Stored attributes. """
        return self._Attribute


    @property
    def ConfigName(self) -> str:
        """ Configuration name (or XML tag name when initializing the instance). """
        return self._ConfigName


    @property
    def Value(self) -> str:
        """ Stored text value from the XML-Element. """
        return self._Value


    def ToDictionary(self) -> dict:
        """
        Returns a dictionary representation of the class.
        """
        result:dict = \
        {
            'attribute': self._Attribute,
            'config_name': self._ConfigName,
            'value': self._Value,
        }
        return result
        

    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element(self._ConfigName)
        elm.text = self._Value
        return elm


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SimpleConfig:'
        if self._ConfigName and len(self._ConfigName) > 0: msg = '%s tag="%s"' % (msg, str(self._ConfigName))
        if self._Value and len(self._Value) > 0: msg = '%s value="%s"' % (msg, str(self._Value))
        if self._Attribute and len(self._Attribute) > 0: msg = '%s attr="%s"' % (msg, str(self._Attribute))
        return msg 
    