# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtouchsources import SoundTouchSources
from .contentitem import ContentItem

@export
class AddStation(SoundTouchModelRequest):
    """
    SoundTouch device AddStation configuration object.
    """

    def __init__(self, source:str=None, sourceAccount:str=None, token:str=None, name:str=None, 
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                Music service source where the station resides (e.g. "PANDORA", "SPOTIFY", etc).
            sourceAccount (str):
                Music service source account value to login with.
            token (str):
                Music service token that uniquely identifies the music service station.
            name (str):
                Music service station name (for logging purposes).
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._ContentItem:ContentItem = ContentItem()
        
        if (root is None):
            
            if isinstance(source, SoundTouchSources):
                source = str(source.value)

            self._Name = name
            self._Source = source
            self._SourceAccount = sourceAccount
            self._Token = token
        
        else:

            rootCI:Element = root.find('ContentItem')
            if rootCI is not None:
                self._ContentItem:ContentItem = ContentItem(root=rootCI)

            
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()



    @property
    def Name(self) -> str:
        """ Music service station name (for logging purposes). """
        return self._Name


    @property
    def Source(self) -> str:
        """ Music service source where the station resides (e.g. "PANDORA", "SPOTIFY", etc). """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ Music service source account value to login with. """
        return self._SourceAccount


    @property
    def Token(self) -> str:
        """ Music service token that uniquely identifies the music service station. """
        return self._Token


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('addStation')
        if self._Source is not None and len(self._Source) > 0: elm.set('source', str(self._Source))
        if self._SourceAccount is not None and len(self._SourceAccount) > 0: elm.set('sourceAccount', str(self._SourceAccount))
        if self._Token is not None and len(self._Token) > 0: elm.set('token', str(self._Token))
        
        if self._Name is not None and len(self._Name) > 0:
            elmNode = Element('name')
            elmNode.text = self._Name
            elm.append(elmNode)
            
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'AddStation:'
        if self._Source is not None and len(self._Source) > 0: msg = '%s Source="%s"' % (msg, str(self._Source))
        if self._SourceAccount is not None and len(self._SourceAccount) > 0: msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        if self._Token is not None and len(self._Token) > 0: msg = '%s Token="%s"' % (msg, str(self._Token))
        if self._Name is not None and len(self._Name) > 0: msg = '%s Name="%s"' % (msg, str(self._Name))
        return msg 
