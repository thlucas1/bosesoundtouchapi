# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr

@export
class ContentItem:
    """
    SoundTouch device ContentItem configuration object.
       
    This class contains the attributes and sub-items that represent the 
    content item (e.g. media source) configuration of the device.  

    Instances of this class can be used to switch the input source of media.
    """
    def __init__(self, source:str=None, itemType:str=None, location:str=None, sourceAccount:str=None, 
                 isPresetable:bool=None, name:str=None, containerArt:str=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                source input.
            itemType (str):
                type of item.
            location (str):
                a direct link to the media (if present).
            sourceAccount (str):
                source account this content item is played with.
            isPresetable (bool):
                true if this item can be saved as a Preset; otherwise, false.
            name (str):
                item name (if present).
            containerArt (str)
                a url link to the container art (if present).
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        if (root is None):
            
            self._ContainerArt:str = containerArt
            self._IsPresetable:bool = isPresetable
            self._ItemType:str = itemType
            self._Location:str = location
            self._Name:str = name
            self._Source:str = source
            self._SourceAccount:str = sourceAccount

        else:

            self._ContainerArt:str = _xmlFind(root, "containerArt")
            self._IsPresetable:bool = root.get("isPresetable") == 'true'
            self._ItemType:str = root.get("type")
            self._Location:str = root.get("location")
            self._Name:str = _xmlFind(root, "itemName")
            self._Source:str = root.get("source")
            self._SourceAccount:str = root.get("sourceAccount")
        
        
    def __repr__(self) -> str:
        return self.ToString()


    @property
    def ContainerArt(self) -> str:
        """ The item's container art url. """
        return self._ContainerArt


    @property
    def IsPresetable(self) -> bool:
        """ Returns True if the content item can be saved as a Preset; otherwise, False. """
        return self._IsPresetable


    @property
    def ItemType(self) -> str:
        """ Specifies the type of this item. """
        return self._ItemType


    @property
    def Location(self) -> str:
        """ If present, a direct link to the media. """
        return self._Location


    @property
    def Name(self) -> str:
        """ The item's name. """
        return self._Name


    @property
    def Source(self) -> str:
        """ 
        The media source type. 
        This value is defined at `bosesoundtouchapi.soundtouchsource.SoundTouchSources`. 
        """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ The source account this content item is played with. """
        return self._SourceAccount


    def ToElement(self) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 
        """
        elm = Element('ContentItem')
        if self._Source and len(self._Source) > 0: elm.set('source', str(self._Source))
        if self._ItemType and len(self._ItemType) > 0: elm.set('type', str(self._ItemType))
        if self._Location and len(self._Location) > 0: elm.set('location', str(self._Location))
        if self._SourceAccount and len(self._SourceAccount) > 0: elm.set('sourceAccount', str(self._SourceAccount))
        if self._IsPresetable: elm.set('isPresetable', str(self._IsPresetable).lower())

        elm_itemname = Element('itemName')
        if self._Name: 
            elm_itemname.text = self._Name
            elm.append(elm_itemname)

        elm_containerart = Element('containerArt')
        if self._ContainerArt: 
            elm_containerart.text = self._ContainerArt
            elm.append(elm_containerart)
            
        return elm


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'ContentItem:'
        if self._Name and len(self._Name) > 0: msg = '%s name="%s"' % (msg, str(self._Name))
        if self._Source and len(self._Source) > 0: msg = '%s source="%s"' % (msg, str(self._Source))
        if self._ItemType and len(self._ItemType) > 0: msg = '%s type="%s"' % (msg, str(self._ItemType))
        if self._Location and len(self._Location) > 0: msg = '%s location="%s"' % (msg, str(self._Location))
        if self._SourceAccount and len(self._SourceAccount) > 0: msg = '%s sourceAccount="%s"' % (msg, str(self._SourceAccount))
        msg = '%s isPresetable="%s"' % (msg, str(self._IsPresetable).lower())
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
        elm = self.ToElement()
        xml = tostring(elm, encoding=encoding).decode(encoding)
        return xml
    