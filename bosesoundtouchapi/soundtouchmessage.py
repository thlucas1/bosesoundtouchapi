# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from .bstutils import export
from .uri.soundtouchuri import SoundTouchUri

@export
class SoundTouchMessage:
    """
    A class representing an exchange object.

    In order to exchange data between a client and the device, this class
    type is used. It stores the request text/uri and the response as an XML-
    Element.
    """
    
    def __init__(self, uri:SoundTouchUri=None, xmlMessage:str=None, response:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            uri (SoundTouchUri):
                The target uri which should be queried.
            xmlMessage (str):
                If a key should be pressed or new data should be saved on the target
                device, an xml formatted string is needed.
            response (xml.etree.ElementTree.Element):
                The response object as an XML-Element.
        """
        self._Uri = uri
        self._XmlMessage = xmlMessage
        self._Response = response

      
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def HasXmlMessage(self) -> bool:
        """ 
        Returns True if an xml message was returned with the response; otherwise, False. 
        """
        return self._XmlMessage is not None


    @property
    def IsSimpleResponse(self) -> bool:
        """ 
        Returns True if the response is a simple pass / fail response; otherwise, False
        if the response requires further processing.
        """
        return self._Response and len(self._Response) != 0


    @property
    def Response(self) -> Element:
        """ 
        Returns the device response as an xml.etree.ElementTree.Element object. 
        """
        return self._Response

    @Response.setter
    def Response(self, value:Element):
        """ 
        Sets the Response property value.
        """
        if isinstance(value, Element):
            self._Response = value
        

    @property
    def Uri(self) -> str: 
        """ 
        The SoundTouchUri object used to make the request.
        """
        return self._Uri


    @property
    def XmlMessage(self) -> str: 
        """ 
        The returned xml formatted message string. 
        """
        return self._XmlMessage


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SoundTouchMessage:'
        msg = '%s uri="%s"' % (msg, str(self._Uri.Path))
        if self._XmlMessage and len(self._XmlMessage) > 0: msg = '%s Message="%s"' % (msg, self._XmlMessage)
        if self.IsSimpleResponse: msg = '%s response="%s"' % (msg, str(self.IsSimpleResponse).lower())
        return msg 
