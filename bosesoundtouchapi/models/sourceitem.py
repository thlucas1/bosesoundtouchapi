# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlGetAttrBool

@export
class SourceItem:
    """
    SoundTouch device SourceItem configuration object.
       
    This class contains the attributes and sub-items that represent a
    single source item configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._IsLocal:bool = None
        self._IsMultiroomAllowed:bool = None
        self._Source:str = None
        self._SourceAccount:str = None
        self._Status:str = None
        self._FriendlyName:str = None
        
        # helper properties (non-xml).
        self._SourceTitle:str = None
        
        if (root is None):
            
            pass
        
        else:

            self._IsLocal = _xmlGetAttrBool(root,'isLocal')
            self._IsMultiroomAllowed = _xmlGetAttrBool(root, 'multiroomallowed')
            self._Source = root.get('source')
            self._SourceAccount = root.get('sourceAccount')
            self._Status = root.get('status')
            self._FriendlyName = root.text
            
            # set source title based upon source, source account, and friendly name values.
            self._SetSourceTitle()
            
        
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    # implement sorting support.
    def __eq__(self, other):
        try:
            return self.Source == other.Source
        except Exception as ex:
            if (isinstance(self, SourceItem )) and (isinstance(other, SourceItem )):
                return self.Source == other.Source
            return False

    def __lt__(self, other):
        try:
            return self.Source < other.Source
        except Exception as ex:
            if (isinstance(self, SourceItem )) and (isinstance(other, SourceItem )):
                return self.Source < other.Source
            return False


    @property
    def FriendlyName(self) -> str:
        """ 
        The friendly name of the source (e.g. "My Media Player", "SpotifyConnectUserName", etc).        
        """
        return self._FriendlyName


    @property
    def IsLocal(self) -> bool:
        """
        True if a local source (e.g. "AUX", "BLUETOOTH", "QPLAY", etc); otherwise, False.
        """
        return self._IsLocal


    @property
    def IsMultiroomAllowed(self) -> bool:
        """ True if the source can be rebroadcast in a multi-room zone; otherwise, False. """
        return self._IsMultiroomAllowed


    @property
    def Source(self) -> str:
        """ The source of media content (e.g. "TUNEIN", "AIRPLAY", "UPNP", etc). """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ The account associated with the Source. """
        return self._SourceAccount


    @property
    def SourceTitle(self) -> str:
        """ The source title of media content (e.g. "Tunein", "Airplay", "NAS Music Server", etc). """
        return self._SourceTitle


    @property
    def Status(self) -> str:
        """ Indicates whether the source is available or not, and its current status. """
        return self._Status


    def _SetSourceTitle(self) -> None:
        """
        Sets the `SourceTitle` value based upon source, source account, and friendly name values.
        """
        if self._Source is None:
            self._SourceTitle = None
        elif self._Source in ['AUX']:
            self._SourceTitle = self._FriendlyName.title()
        elif self._Source in ['LOCAL_MUSIC','STORED_MUSIC']:
            self._SourceTitle = self._FriendlyName
        elif self._Source in ['AIRPLAY','ALEXA','BLUETOOTH','NOTIFICATION','TUNEIN','UPNP']:
            self._SourceTitle = self._Source.title()
        elif self._Source in ['DEEZER','IHEART','PANDORA','QPLAY','QQMUSIC','SIRIUSXM','SPOTIFY']:
            self._SourceTitle = '%s (%s)' % (self._Source.title(), self._FriendlyName)
        elif self._Source in ['STORED_MUSIC_MEDIA_RENDERER']:
            self._SourceTitle = '%s (%s)' % (self._Source.replace('_',' ').title(), self._FriendlyName)
        elif self._Source in ['LOCAL_INTERNET_RADIO']:
            self._SourceTitle = self._Source.replace('_',' ').title()
        else:
            self._SourceTitle = '%s (%s)' % (self._Source.title(), self._SourceAccount)


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('sourceitem')
        elm.set('source', str(self._Source))
        elm.set('sourceAccount', str(self._SourceAccount))
        elm.set('status', str(self._Status))
        elm.set('isLocal', str(self._IsLocal))
        elm.set('multiroomAllowed', str(self._IsMultiroomAllowed))
        if self._FriendlyName is not None and len(self._FriendlyName) > 0:
            elm.text = str(self._FriendlyName)
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SourceItem:'
        if self._Source is not None and len(self._Source) > 0: msg = '%s source="%s"' % (msg, str(self._Source))
        if self._SourceAccount is not None and len(self._SourceAccount) > 0: msg = '%s sourceAccount="%s"' % (msg, str(self._SourceAccount))
        if self._Status is not None and len(self._Status) > 0: msg = '%s status="%s"' % (msg, str(self._Status))
        if self._IsLocal is not None: msg = '%s isLocal=%s' % (msg, str(self._IsLocal).lower())
        if self._IsMultiroomAllowed is not None: msg = '%s multiroomAllowed=%s' % (msg, str(self._IsMultiroomAllowed).lower())
        if self._FriendlyName is not None and len(self._FriendlyName) > 0: msg = '%s friendlyName="%s"' % (msg, str(self._FriendlyName))
        if self._SourceTitle is not None and len(self._SourceTitle) > 0: msg = '%s SourceTitle="%s"' % (msg, str(self._SourceTitle))
        return msg 
