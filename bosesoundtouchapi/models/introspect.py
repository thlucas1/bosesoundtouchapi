# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindInt
from ..soundtoucherror import SoundTouchError
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtouchsources import SoundTouchSources

@export
class Introspect(SoundTouchModelRequest):
    """
    SoundTouch device Introspect configuration object.
       
    This class contains the attributes and sub-items that represent
    Introspect criteria.
    """

    def __init__(self, source:str=None, sourceAccount:str=None, 
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                Type or name of the service to introspect (e.g. "SPOTIFY", "TUNEIN", etc).
            sourceAccount (str):
                Account associated with the Source.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchError:
                startItem argument was not of type int.  
        """
        self._Source:str = None
        self._SourceAccount:str = None

        # helper attributes (not part of the xml definition).
        self._ContainerTitleFormatString:str = None
        
        if (root is None):
            
            # convert enums to strings.
            if isinstance(source, SoundTouchSources):
                source = source.value
            if sourceAccount is None:
                sourceAccount = ""
                
            self._Source = source
            self._SourceAccount = sourceAccount
                              
        elif root.tag == 'introspect':

            self._Source = root.get('source')
            self._SourceAccount = root.get('sourceAccount')


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Source(self) -> str:
        """ Type or name of the service to introspect (e.g. "SPOTIFY", "TUNEIN", etc). """
        return self._Source

    @Source.setter
    def Source(self, value:str):
        """ 
        Sets the Source property value.
        """
        if isinstance(value, SoundTouchSources):
            value = value.value
        self._Source = value


    @property
    def SourceAccount(self) -> str:
        """ Account associated with the Source. """
        return self._SourceAccount

    @SourceAccount.setter
    def SourceAccount(self, value:str):
        """ 
        Sets the SourceAccount property value.
        """
        self._SourceAccount = value


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('introspect')
        elm.set('source', str(self._Source))
        elm.set('sourceAccount', str(self._SourceAccount))
        return elm
        
        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Introspect:'
        msg = '%s Source="%s"' % (msg, str(self._Source))
        msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        return msg 
