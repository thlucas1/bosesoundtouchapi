# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFind, _xmlGetAttrBool
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtouchsources import SoundTouchSources


@export
class ContentItem(SoundTouchModelRequest):
    """
    SoundTouch device ContentItem configuration object.
       
    This class contains the attributes and sub-items that represent the 
    content item (e.g. media source) configuration of the device.  

    Instances of this class can be used to switch the input source of media.
    """
    def __init__(self, source:SoundTouchSources=None, typeValue:str=None, location:str=None, sourceAccount:str=None, 
                 isPresetable:bool=None, name:str=None, containerArt:str=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (SoundTouchSources|str):
                source input.
            typeValue (str):
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
        self._ContainerArt:str = None
        self._IsNavigate:bool = None
        self._IsPresetable:bool = None
        self._Location:str = None
        self._Name:str = None
        self._Offset:int = None
        self._Source:str = None
        self._SourceAccount:str = None
        self._TypeValue:str = None

        if (root is None):
            
            if isinstance(source, SoundTouchSources):
                source = str(source.value)

            self._ContainerArt = containerArt
            self._IsPresetable = isPresetable
            self._Location = location
            self._Name = name
            self._Source = source
            self._SourceAccount = sourceAccount
            self._TypeValue = typeValue

        else:

            self._ContainerArt = _xmlFind(root, "containerArt")
            self._IsNavigate = _xmlGetAttrBool(root, "isNavigate")
            self._IsPresetable = _xmlGetAttrBool(root, "isPresetable")
            self._Location = root.get("location")
            self._Name = _xmlFind(root, "itemName")
            self._Offset = root.get("offset")
            self._Source = root.get("source")
            self._SourceAccount = root.get("sourceAccount")
            self._TypeValue = root.get("type")
            
        
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ContainerArt(self) -> str:
        """ Item's container art url. """
        return self._ContainerArt


    @property
    def IsNavigate(self) -> bool:
        """ Returns True if the content item is part of a navigate result; otherwise, False. """
        return self._IsNavigate


    @property
    def IsPresetable(self) -> bool:
        """ Returns True if the content item can be saved as a Preset; otherwise, False. """
        return self._IsPresetable


    @property
    def Location(self) -> str:
        """ If present, a direct url link to the media. """
        return self._Location


    @property
    def Name(self) -> str:
        """ Item's name. """
        return self._Name


    @property
    def Offset(self) -> int:
        """ If present, the offset of the currently playing content. """
        return self._Offset


    @property
    def Source(self) -> str:
        """ The type or name of the service that is currently playing or to be played. """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ The account associated with the Source. """
        return self._SourceAccount


    @property
    def TypeValue(self) -> str:
        """ Specifies the type of this item. """
        return self._TypeValue


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('ContentItem')
        if self._Source is not None and len(self._Source) > 0: elm.set('source', str(self._Source))
        if self._TypeValue is not None and len(self._TypeValue) > 0: elm.set('type', str(self._TypeValue))
        if self._Location is not None and len(self._Location) > 0: elm.set('location', str(self._Location))
        if self._SourceAccount is not None and len(self._SourceAccount) > 0: elm.set('sourceAccount', str(self._SourceAccount))
        if self._IsNavigate is not None: elm.set('isNavigate', str(self._IsNavigate).lower())
        if self._IsPresetable is not None: elm.set('isPresetable', str(self._IsPresetable).lower())
        if self._Offset is not None and self._Offset > 0: elm.set('offset', str(self._Offset))

        if self._Name is not None: 
            elmNode = Element('itemName')
            elmNode.text = self._Name
            elm.append(elmNode)

        if self._ContainerArt is not None: 
            elmNode = Element('containerArt')
            elmNode.text = self._ContainerArt
            elm.append(elmNode)
            
        return elm


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'ContentItem:'
        if self._Name is not None and len(self._Name) > 0: msg = '%s Name="%s"' % (msg, str(self._Name))
        if self._Source is not None and len(self._Source) > 0: msg = '%s Source="%s"' % (msg, str(self._Source))
        if self._TypeValue is not None and len(self._TypeValue) > 0: msg = '%s Type="%s"' % (msg, str(self._TypeValue))
        if self._Location is not None and len(self._Location) > 0: msg = '%s Location="%s"' % (msg, str(self._Location))
        if self._SourceAccount is not None and len(self._SourceAccount) > 0: msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        if self._Offset is not None and self._Offset > 0: msg = '%s Offset="%s"' % (msg, str(self._Offset))
        if self._IsPresetable is not None: msg = '%s IsPresetable="%s"' % (msg, str(self._IsPresetable).lower())
        if self._IsNavigate is not None: msg = '%s IsNavigate="%s"' % (msg, str(self._IsNavigate).lower())
        if self._ContainerArt is not None and len(self._ContainerArt) > 0: msg = '%s ContainerArt="%s"' % (msg, str(self._ContainerArt))
        return msg 
