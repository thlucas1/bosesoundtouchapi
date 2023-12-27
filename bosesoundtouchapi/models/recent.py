# external package imports.
import time
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlGetAttrBool, _xmlGetAttrInt
from ..soundtouchsources import SoundTouchSources
from .contentitem import ContentItem

@export
class Recent:
    """
    SoundTouch device Recent configuration object.
       
    This class contains the attributes and sub-items that represent a
    single recent configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._RecentId:int = None
        self._CreatedOn:int = None
        self._ContentItem:ContentItem = ContentItem()

        # helper properties (non-xml).
        self._SourceTitle:str = None

        if (root is None):
            
            pass

        else:

            self._CreatedOn = _xmlGetAttrInt(root, 'utcTime')
            self._DeviceId = root.get('deviceID')
            self._RecentId = _xmlGetAttrInt(root, 'id')

            rootCI:Element = root.find('contentItem')
            if rootCI is not None:
                self._ContentItem:ContentItem = ContentItem(root=rootCI)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    # implement sorting support.
    def __eq__(self, other):
        try:
            return self.CreatedOn == other.CreatedOn
        except Exception:
            if (isinstance(self, Recent )) and (isinstance(other, Recent )):
                return self.CreatedOn == other.CreatedOn
            return False

    def __lt__(self, other):
        try:
            return self.CreatedOn < other.CreatedOn
        except Exception:
            if (isinstance(self, Recent )) and (isinstance(other, Recent )):
                return self.CreatedOn < other.CreatedOn
            return False


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
    def CreatedOn(self) -> int:
        """ Date and time (in epoch format) of when the recent was created. """
        return self._CreatedOn
    

    @property
    def DeviceId(self) -> str:
        """ Device identifier the configuration information was obtained from. """
        return self._DeviceId

    
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
    def RecentId(self) -> int:
        """ The recent identifier (1 - 6). """
        return self._RecentId


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
    def SourceTitle(self) -> str:
        """ 
        The source title of media content (e.g. "Tunein", "Airplay", "NAS Music Server", etc). 
        
        This property is not part of the returned xml of the configuration, but is set after
        a call to `SoundTouchClient.GetRecentList(resolveSourceTitles=True)' so that source
        titles can be displayed by user-interfaces.
        """
        return self._SourceTitle

    @SourceTitle.setter
    def SourceTitle(self, value:str):
        """ 
        Sets the SourceTitle property value.
        """
        self._SourceTitle = value


    @property
    def TypeValue(self) -> str:
        """ Specifies the type of the content item. """
        if self._ContentItem is None:
            return None
        return self._ContentItem._TypeValue


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('recent')
        if self._DeviceId is not None and len(self._DeviceId) > 0: elm.set('deviceID', str(self._DeviceId))
        if self._RecentId is not None and self._RecentId > 0: elm.set('id', str(self._RecentId))
        if self._CreatedOn is not None and self._CreatedOn > 0: elm.set('createdOn', str(self._CreatedOn))
        if self._SourceTitle is not None and len(self._SourceTitle) > 0: elm.set('SourceTitle', str(self._SourceTitle))
        
        if self._ContentItem is not None:
            elmNode = self._ContentItem.ToElement()
            elm.append(elmNode)

        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Recent:'
        msg = '%s Id="%s"' % (msg, str(self._RecentId))
        if self._ContentItem is not None: msg = '%s %s' % (msg, str(self._ContentItem))
        if self._DeviceId is not None: msg = '%s DeviceId="%s"' % (msg, str(self._DeviceId))
        msg = '%s CreatedOn="%s"' % (msg, str(self._CreatedOn))
        if self._SourceTitle is not None: msg = '%s SourceTitle="%s"' % (msg, str(self._SourceTitle))
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
