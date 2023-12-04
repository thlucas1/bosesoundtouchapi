# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtouchsources import SoundTouchSources
from .contentitem import ContentItem

@export
class RemoveStation(SoundTouchModelRequest):
    """
    SoundTouch device RemoveStation configuration object.
    """

    def __init__(self, source:str=None, sourceAccount:str=None, location:str=None, name:str=None, 
                 contentItem:ContentItem=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                Music service source where the station resides (e.g. "PANDORA", "SPOTIFY", etc).
            sourceAccount (str):
                Music service source account value to login with.
            location (str):
                Music service station location to access.
            name (str):
                Music service station name (for logging purposes).
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
            contentItem (ContentItem):
                ContentItem object to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._ContentItem:ContentItem = ContentItem()

        if (contentItem is not None) and (isinstance(contentItem,ContentItem)):
            
            self._ContentItem._IsPresetable = contentItem.IsPresetable
            self._ContentItem._Location = contentItem.Location
            self._ContentItem._Name = contentItem.Name
            self._ContentItem._Source = contentItem.Source
            self._ContentItem._SourceAccount = contentItem.SourceAccount

        elif (root is None):
            
            if isinstance(source, SoundTouchSources):
                source = str(source.value)

            self._ContentItem._IsPresetable = True
            self._ContentItem._Location = location
            self._ContentItem._Name = name
            self._ContentItem._Source = source
            self._ContentItem._SourceAccount = sourceAccount
        
        else:

            rootCI:Element = root.find('ContentItem')
            if rootCI is not None:
                self._ContentItem:ContentItem = ContentItem(root=rootCI)

            
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ContentItem(self) -> ContentItem:
        """ ContentItem object used to store the supplied values. """
        return self._ContentItem


    @property
    def Location(self) -> str:
        """ Music service station location to access. """
        if self._ContentItem is None:
            return None
        return self._ContentItem._Location


    @property
    def Name(self) -> str:
        """ Music service station name (for logging purposes). """
        if self._ContentItem is None:
            return None
        return self._ContentItem._Name


    @property
    def Source(self) -> str:
        """ Music service source where the station resides (e.g. "PANDORA", "SPOTIFY", etc). """
        if self._ContentItem is None:
            return None
        return self._ContentItem._Source


    @property
    def SourceAccount(self) -> str:
        """ Music service source account value to login with. """
        if self._ContentItem is None:
            return None
        return self._ContentItem._SourceAccount


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        if self._ContentItem is not None:
            return self._ContentItem.ToElement()
            
        return ContentItem()

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        if self._ContentItem is not None: 
            return self._ContentItem.ToString()
        else:
            return 'ContentItem:'
