# external package imports.
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlGetAttrInt
from .contentitem import ContentItem

@export
class MediaItemContainer:
    """
    SoundTouch device MediaItemContainer configuration object.
       
    This class contains the attributes and sub-items that represent a
    single MediaItemContainer configuration of the device.
    """

    def __init__(self, root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Offset:int = None
        self._ContentItem:ContentItem = ContentItem()

        if (root is None):
            
            pass
        
        else:

            self._Offset = _xmlGetAttrInt(root, 'offset')

            rootCI:Element = root.find('ContentItem')
            if rootCI is not None:
                self._ContentItem:ContentItem = ContentItem(root=rootCI)

        
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ContentItem(self) -> ContentItem:
        """ ContentItem value. """
        return self._ContentItem


    @property
    def ContainerArt(self) -> str:
        """ Content item's container art url. """
        if self._ContentItem is None:
            return None
        return self._ContentItem._ContainerArt


    @property
    def IsPresetable(self) -> str:
        """ Returns True if the content item can be saved as a Preset; otherwise, False. """
        if self._ContentItem is None:
            return None
        return self._ContentItem._IsPresetable


    @property
    def Location(self) -> str:
        """ If present, the content item's direct link to the media. """
        if self._ContentItem is None:
            return None
        return self._ContentItem._Location


    @property
    def Name(self) -> str:
        """ Content item's name. """
        if self._ContentItem is None:
            return None
        return self._ContentItem._Name


    @property
    def Offset(self) -> int:
        """ Offset of the item. """
        return self._Offset


    @property
    def Source(self) -> str:
        """ 
        Content item source type. 
        
        This value is defined at `bosesoundtouchapi.soundtouchsources.SoundTouchSources`. 
        """
        if self._ContentItem is None:
            return None
        return self._ContentItem._Source


    @property
    def SourceAccount(self) -> str:
        """ The account associated with the Source. """
        if self._ContentItem is None:
            return None
        return self._ContentItem._SourceAccount


    @property
    def TypeValue(self) -> str:
        """ Specifies the type of the content item. """
        if self._ContentItem is None:
            return None
        return self._ContentItem._TypeValue


    def ToDictionary(self, encoding:str='utf-8') -> dict:
        """
        Returns a dictionary representation of the class.
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.
        """
        if encoding is None:
            encoding = 'utf-8'
            
        contentItem:dict = {}
        if self._ContentItem is not None:
            contentItem = self._ContentItem.ToDictionary(encoding)
        
        result:dict = {}
        
        if self._Offset is not None: 
            result['Offset'] = self._Offset
        result['ContentItem'] = contentItem
        
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
        elm = Element('mediaItemContainer')
        if self._Offset is not None: elm.set('offset', str(self._Offset))
        
        if self._ContentItem is not None:
            elmNode = self._ContentItem.ToElement()
            elm.append(elmNode)
            
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'MediaItemContainer:'
        if self._Offset is not None: msg = '%s Offset="%s"' % (msg, str(self._Offset))
        if self._ContentItem is not None: msg = '%s %s' % (msg, str(self._ContentItem))
        return msg 


    def ToXmlString(self, encoding:str='utf-8') -> str:
        """ 
        Returns an xml string representation of the class. 
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.
        """
        if encoding is None:
            encoding = 'utf-8'
            
        elm:Element = self.ToElement(False)
        xml:str = tostring(elm, encoding=encoding)
        
        # always return a string, as some encodings return a byte array!
        if not isinstance(xml, str):
            xml = xml.decode(encoding=encoding)
        return xml
