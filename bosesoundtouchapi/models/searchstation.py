# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtouchsources import SoundTouchSources

@export
class SearchStation(SoundTouchModelRequest):
    """
    SoundTouch device SearchStation configuration object.
       
    This class contains the attributes and sub-items that represent
    SearchStation criteria.
    """

    def __init__(self, source:str=None, sourceAccount:str=None, searchText:str=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                Music service source to search (e.g. "PANDORA", "SPOTIFY", etc).
            sourceAccount (str):
                Music service source account (e.g. the music service user-id).
            searchText (str):
                Text to search for in the Music service.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchError:
                startItem argument was not of type int.  
        """
        
        # <search source="PANDORA" sourceAccount="thlucas@yahoo.com">
        #   Zach Williams
        # </search>

        self._SearchText:str = None
        self._Source:str = None
        self._SourceAccount:str = None
        
        if (root is None):
            
            if isinstance(source, SoundTouchSources):
                source = str(source.value)
                
            self._SearchText = searchText
            self._Source = source
            self._SourceAccount = sourceAccount
        
        else:

            self._SearchText = root.text
            self._Source = root.get('source', default=None)
            self._SourceAccount = root.get('sourceAccount', default=None)
            

    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def SearchText(self) -> str:
        """ Text to search for in the Music service. """
        return self._SearchText

    @SearchText.setter
    def SearchText(self, value:str):
        """ 
        Sets the SearchText property value.
        """
        if value is not None:
            if isinstance(value, str):
                self._SearchText = value


    @property
    def Source(self) -> str:
        """ Music service source to search (e.g. "PANDORA", "SPOTIFY", etc). """
        return self._Source

    @Source.setter
    def Source(self, value:str):
        """ 
        Sets the Source property value.
        """
        if value is not None:
            if isinstance(value, SoundTouchSources):
                self._Source = value.value
            elif isinstance(value, str):
                self._Source = value


    @property
    def SourceAccount(self) -> str:
        """ Music service source account (e.g. the music service user-id). """
        return self._SourceAccount

    @SourceAccount.setter
    def SourceAccount(self, value:str):
        """ 
        Sets the SourceAccount property value.
        """
        if value is not None:
            if isinstance(value, str):
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
        elm = Element('search')
        if self._Source and len(self._Source) > 0: elm.set('source', str(self._Source))
        if self._SourceAccount and len(self._SourceAccount) > 0: elm.set('sourceAccount', str(self._SourceAccount))

        if self._SearchText and len(self._SearchText) > 0: 
            elm.text = self._SearchText

        return elm
        
        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SearchStation:'
        msg = '%s Source="%s"' % (msg, str(self._Source))
        msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        msg = '%s SearchText="%s"' % (msg, str(self._SearchText))
        return msg 
    