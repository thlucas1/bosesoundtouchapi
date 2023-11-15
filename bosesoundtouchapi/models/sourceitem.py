# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind, _xmlFindAttr

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
        if (root is None):
            pass  # no other parms to process.
        else:

            # base fields.
            self._IsLocal:bool = bool(root.get('isLocal', default='false') == 'true')
            self._IsMultiroomAllowed:bool = bool(root.get('multiroomallowed', default='false') == 'true')
            self._Source:str = root.get('source')
            self._SourceAccount:str = root.get('sourceAccount')
            self._Status:str = root.get('status')
            self._UserName:str = root.text

        
    def __repr__(self) -> str:
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
            # the following comparison will fail if the property value is None!  
            # use the following syntax when calling a sort method that uses lambda searches:
            # epColl.sort(Source=lambda x: x.Source or "", reverse=False)     <- GOOD syntax
            # epColl.sort(Source=lambda x: x.Source, reverse=False)           <- BAD syntax, as the "x.Source" property may be None, and will cause this to fail!
            return self.Source < other.Source
        except Exception as ex:
            if (isinstance(self, SourceItem )) and (isinstance(other, SourceItem )):
                return self.Source < other.Source
            return False


    @property
    def IsLocal(self) -> bool:
        """
        True if the source can play content locally on the device; otherwise, False to
        indicate the source can only play content remotely.
        
        Local source examples are "BLUETOOTH", "NOTIFICATION", "QPLAY", etc.  
        Remote source examples are "AIRPLAY", "UPNP", "TUNEIN", "SPOTIFY", etc.  
        """
        return self._IsLocal


    @property
    def IsMultiroomAllowed(self) -> bool:
        """ True if multiroom playback is allowed for this source; otherwise, False. """
        return self._IsMultiroomAllowed


    @property
    def Source(self) -> str:
        """ The source of media content (e.g. "TUNEIN", "AIRPLAY", "UPNP", etc). """
        return self._Source


    @property
    def SourceAccount(self) -> str:
        """ 
        A source account used to play media content, if one is required.
        
        Example sources requiring a sourceAccount value are "QPLAY", "SPOTIFY", "AIRPLAY", "ALEXA", etc.
        """
        return self._SourceAccount


    @property
    def Status(self) -> str:
        """ The current status of the source (e.g. "READY", "UNAVAILABLE", etc). """
        return self._Status


    @property
    def UserName(self) -> str:
        """ 
        A user name used to play media content, if one is required.
        
        Example sources requiring a sourceAccount value are "QPLAY", "SPOTIFY", "AIRPLAY", "ALEXA", etc.
        """
        return self._UserName


    def ToElement(self) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 
        """
        elm = Element('sourceitem')
        elm.set('source', str(self._Source))
        elm.set('sourceAccount', str(self._SourceAccount))
        elm.set('status', str(self._Status))
        elm.set('isLocal', str(self._IsLocal))
        elm.set('multiroomAllowed', str(self._IsMultiroomAllowed))
        elm.set('userName', str(self._UserName))
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'SourceItem:'
        if self._Source and len(self._Source) > 0: msg = '%s source="%s"' % (msg, str(self._Source))
        if self._SourceAccount and len(self._SourceAccount) > 0: msg = '%s sourceAccount="%s"' % (msg, str(self._SourceAccount))
        if self._Status and len(self._Status) > 0: msg = '%s status="%s"' % (msg, str(self._Status))
        msg = '%s isLocal=%s' % (msg, str(self._IsLocal).lower())
        msg = '%s multiroomAllowed=%s' % (msg, str(self._IsMultiroomAllowed).lower())
        if self._UserName and len(self._UserName) > 0: msg = '%s username="%s"' % (msg, str(self._UserName))
        return msg 
