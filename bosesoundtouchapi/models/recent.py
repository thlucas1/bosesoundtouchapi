# external package imports.
import time
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind
from .contentitem import ContentItem

@export
class Recent:
    """
    SoundTouch device Recent configuration object.
       
    This class contains the attributes and sub-items that represent a
    single recent configuration of the device.
    """

    def __init__(self, recentId:int = None, createdOn:int = None, source: str = None, typeValue: str = None, 
                 location: str = None, sourceAccount: str = None, isPresetable: bool = None, name: str = None, containerArt:str = None,
                 root : Element = None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            recentId (int):
                Recent identifier.
            createdOn (int):
                Date time (in epoch format) the recent was created; 
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
            self._RecentId:int = int(recentId) if recentId else 0
            self._CreatedOn:int = int(createdOn) if createdOn else 0

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

        else:

            # base fields.
            self._CreatedOn:int = int(root.get("utcTime", default=0))
            self._RecentId:int = int(root.get("id"))

            # ContentItem fields.
            root_ci = root.find('contentItem')
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

    # implement sorting support.
    def __eq__(self, other):
        try:
            return self.CreatedOn == other.CreatedOn
        except Exception as ex:
            if (isinstance(self, Recent )) and (isinstance(other, Recent )):
                return self.CreatedOn == other.CreatedOn
            return False

    def __lt__(self, other):
        try:
            # the following comparison will fail if the property value is None!  
            # use the following syntax when calling a sort method that uses lambda searches:
            # epColl.sort(CreatedOn=lambda x: x.CreatedOn or "", reverse=False)     <- GOOD syntax
            # epColl.sort(CreatedOn=lambda x: x.CreatedOn, reverse=False)           <- BAD syntax, as the "x.CreatedOn" property may be None, and will cause this to fail!
            return self.CreatedOn < other.CreatedOn
        except Exception as ex:
            if (isinstance(self, Recent )) and (isinstance(other, Recent )):
                return self.CreatedOn < other.CreatedOn
            return False


    @property
    def CreatedOn(self) -> int:
        """ Date and time (in epoch format) of when the recent was created. """
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
    def RecentId(self) -> int:
        """ The recent identifier (1 - 6). """
        return self._RecentId


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
        elm = Element('recent')
        if self._RecentId and self._RecentId > 0: elm.set('id', str(self._RecentId))
        if self._CreatedOn and self._CreatedOn > 0: elm.set('createdOn', str(self._CreatedOn))
        
        elm.append(self.ContentItem_ToElement())
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Recent:'
        if self._RecentId: msg = '%s id="%s"' % (msg, str(self._RecentId))
        if self._Name and len(self._Name) > 0: msg = '%s name="%s"' % (msg, str(self._Name))
        if self._Source and len(self._Source) > 0: msg = '%s source="%s"' % (msg, str(self._Source))
        if self._SourceAccount and len(self._SourceAccount) > 0: msg = '%s sourceAccount="%s"' % (msg, str(self._SourceAccount))
        if self._ItemType and len(self._ItemType) > 0: msg = '%s type="%s"' % (msg, str(self._ItemType))
        if self._Location and len(self._Location) > 0: msg = '%s location="%s"' % (msg, str(self._Location))
        msg = '%s isPresetable="%s"' % (msg, str(self._IsPresetable).lower())
        if self._CreatedOn > 0: msg = '%s created="%s"' % (msg, str(self._CreatedOn))
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
