# external package imports.
from abc import abstractmethod
from xml.etree.ElementTree import Element, tostring

# our package imports.
from .bstutils import export

@export
class SoundTouchModelRequest:
    """
    A class representing a model that can issue a POST request with an
    xml payload that gets placed in the request body.
    """
    
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        # nothing to do here - subclasses just need to implement methods.
        pass


    @abstractmethod
    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        raise NotImplementedError("The '%s' class has not overridden the ToElement() method." % (self.__class__.__name__))

        
    @abstractmethod
    def ToXmlRequestBody(self, encoding:str='utf-8') -> str:
        """ 
        Returns a POST request body, which is used to update the device configuration.
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.

        Returns:
            An xml string that can be used in a POST request to update the
            device configuration.
        """
        if encoding is None:
            encoding = 'utf-8'
            
        elm:Element = self.ToElement(True)
        xml:str = tostring(elm, encoding=encoding)
        
        # always return a string, as some encodings return a byte array!
        if not isinstance(xml, str):
            xml = xml.decode(encoding=encoding)
        return xml
