# external package imports.
import time
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr
from .contentitem import ContentItem

@export
class Preset:
    """
    SoundTouch device Preset configuration object.
       
    This class contains the attributes and sub-items that represent a
    single preset configuration of the device.
    """

    def __init__(self, presetId:int = None, createdOn:int = None, updatedOn: int = None, source: str = None, typeValue: str = None, 
                 location: str = None, sourceAccount: str = None, isPresetable: bool = None, name: str = None, containerArt:str = None,
                 root : Element = None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            presetId (int):
                Preset identifier; valid values are 1 thru 6.
            createdOn (int):
                Date time (in epoch format) the preset was created; 
                the current epoch time is used if the value is zero or None.
            updatedOn (int):
                Date time (in epoch format) the preset was last updated;
                the current epoch time is used if the value is zero or None.
            source (str):
                ContentItem node source value.
            typeValue (str):
                ContentItem node type value.
            location (str):
                ContentItem node location value.
            sourceAccount (str):
                ContentItem node sourceAccount value.
            isPresetable (bool):
                ContentItem node isPresetable value.
            name (str):
                ContentItem node itemName value.
            containerArt (str)
                ContentItem node containerArt value.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        if (root is None):
            
            # base fields.
            self._PresetId:int = int(presetId) if presetId else 0
            self._CreatedOn:int = int(createdOn) if createdOn else 0
            self._UpdatedOn:int = int(updatedOn) if updatedOn else 0

            # ContentItem fields.
            self._Source:str = source
            self._ItemType:str = typeValue
            self._Location:str = location
            self._SourceAccount:str = sourceAccount
            self._IsPresetable:bool = isPresetable
            self._Name:str = name
            self._ContainerArt:str = containerArt
        
            # use current epoch time if created / updated on are not set.
            epoch_time:int = int(time.time())
            if createdOn == 0:
                self._CreatedOn = epoch_time
            if updatedOn == 0:
                self._UpdatedOn = epoch_time

        else:

            # base fields.
            self._CreatedOn:int = int(root.get("createdOn", default=0))
            self._PresetId:int = int(root.get("id"))
            self._UpdatedOn:int = int(root.get("updatedOn", default=0))

            # ContentItem fields.
            root_ci = root.find('ContentItem')
            if root_ci != None:
                self._ContainerArt:str = _xmlFind(root_ci, "containerArt")
                self._IsPresetable:bool = bool(root_ci.get("isPresetable", default='false') == 'true')
                self._ItemType:str = root_ci.get("type")
                self._Location:str = root_ci.get("location")
                self._Name:str = _xmlFind(root_ci, "itemName")
                self._Source:str = root_ci.get("source")
                self._SourceAccount:str = root_ci.get("sourceAccount")

        
    def __repr__(self) -> str:
        return self.ToString()


    @property
    def CreatedOn(self) -> int:
        """ Date and time (in epoch format) of when the preset was created. """
        return self._CreatedOn


    @property
    def ContainerArt(self) -> str:
        """ The content item's container art url. """
        return self._ContainerArt


    @property
    def IsPresetable(self) -> str:
        """ Returns True if the content item can be saved as a Preset; otherwise, False. """
        return self._IsPresetable


    @property
    def ItemType(self) -> str:
        """ Specifies the type of the content item. """
        return self._ItemType


    @property
    def Location(self) -> str:
        """ If present, the content item's direct link to the media. """
        return self._Location


    @property
    def Name(self) -> str:
        """ The content item's name. """
        return self._Name


    @property
    def PresetId(self) -> int:
        """ The preset identifier (1 - 6). """
        return self._PresetId


    @property
    def Source(self) -> str:
        """ 
        The content item source type. 
        This value is defined at `bosesoundtouchapi.soundtouchsource.SoundTouchSources`. 
        """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ The source account this content item is played with. """
        return self._SourceAccount


    @property
    def UpdatedOn(self) -> int:
        """ Date and time (in epoch format) of when the preset was last updated. """
        return self._UpdatedOn


    def ContentItem_ToElement(self) -> Element:
        """ 
        Returns an xmltree Element node representation of the ContentItem fields of the class. 
        """
        elm_ci:ContentItem = ContentItem(self._Source, self._ItemType, self._Location, self._SourceAccount, self._IsPresetable, self._Name, self._ContainerArt)
        return elm_ci.ToElement()

        
    def ContentItem_ToXmlString(self, encoding:str='utf-8') -> str:
        """ 
        Returns an xml string representation of the ContentItem fields of the class. 
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.
        """
        if encoding is None:
            encoding = 'utf-8'
        elm = self.ContentItem_ToElement()
        xml = tostring(elm, encoding=encoding).decode(encoding)
        return xml


    def ToElement(self) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 
        """
        elm = Element('preset')
        if self._PresetId and self._PresetId > 0: elm.set('id', str(self._PresetId))
        if self._CreatedOn and self._CreatedOn > 0: elm.set('createdOn', str(self._CreatedOn))
        if self._UpdatedOn and self._UpdatedOn > 0: elm.set('updatedOn', str(self._UpdatedOn))
        
        elm.append(self.ContentItem_ToElement())
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Preset:'
        if self._PresetId: msg = '%s id="%s"' % (msg, str(self._PresetId))
        if self._Name and len(self._Name) > 0: msg = '%s name="%s"' % (msg, str(self._Name))
        if self._Source and len(self._Source) > 0: msg = '%s source="%s"' % (msg, str(self._Source))
        if self._SourceAccount and len(self._SourceAccount) > 0: msg = '%s sourceAccount="%s"' % (msg, str(self._SourceAccount))
        if self._ItemType and len(self._ItemType) > 0: msg = '%s type="%s"' % (msg, str(self._ItemType))
        if self._Location and len(self._Location) > 0: msg = '%s location="%s"' % (msg, str(self._Location))
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
