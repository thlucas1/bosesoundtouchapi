# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export, _xmlFind
from ..soundtoucherror import SoundTouchError
from .contentitem import ContentItem
from .mediaitemcontainer import MediaItemContainer

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SISession
_logsi:SISession = SIAuto.Si.GetSession(__package__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__package__, True)
_logsi.SystemLogger = logging.getLogger(__package__)

@export
class NavigateItem:
    """
    SoundTouch device NavigateItem configuration object.
       
    This class contains the attributes and sub-items that represent a
    single source item configuration of the device.
    """

    def __init__(self, source:str=None, sourceAccount:str=None, 
                 name:str=None, typeValue:str=None, contentItem:ContentItem=None,
                 location:str=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                Music service source to navigate (e.g. "PANDORA", "STORED_MUSIC", etc).
            sourceAccount (str):
                Music service source account (e.g. the music service user-id).
            name (str):
                Parent container name to navigate, if navigating for child containers.  
                Specify null if navigating a root container.
            typeValue (str):
                Parent container type to navigate, if navigating for child containers.  
                Specify null if navigating a root container.
            contentItem (ContentItem):
                Parent container ContentItem to navigate, if navigating for child containers.  
                Specify null if navigating a root container.
            location (str):
                Parent container location to navigate, if navigating for child containers.  
                This argument will not be used if the contentItem argument is specified.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._BackupUrl:str = None
        self._BitRate:str = None
        self._ContentItem:ContentItem = None
        self._Description:str = None
        self._Format:str = None
        self._Location:str = None
        self._Logo:str = None
        self._MediaItemContainer:MediaItemContainer = None
        self._Mime:str = None
        self._Name:str = None
        self._Playable:int = None
        self._Reliability:str = None
        self._Token:str = None
        self._TypeValue:str = None
        self._Url:str = None
        self._UtcTime:str = None
        # containerType    STS.ItemType.Enum
        # containerToken 
        # containerName 
        # artistName
        # albumName 
        # availability     STS.Availability.Enum

        if (root is None):
                       
            # validations.
            if (contentItem is not None) and (not isinstance(contentItem, ContentItem)):
                raise SoundTouchError('contentItem argument was not of type ContentItem', logsi=_logsi)

            # if name, type, or contentItem specified, then all three are required.
            if (name is not None) or (typeValue is not None) or (contentItem is not None):
                if name is None:
                    raise SoundTouchError('name argument is required if a parent container is to be navigated.', logsi=_logsi)
                if typeValue is None:
                    raise SoundTouchError('typeValue argument is required if a parent container is to be navigated.', logsi=_logsi)
                if contentItem is None and location is None:
                    raise SoundTouchError('contentItem argument is required if a parent container is to be navigated.', logsi=_logsi)

            # if location specified, then build a content item (if one was not specified).
            if contentItem is None and location is not None:
                contentItem = ContentItem(source, None, location, sourceAccount, True)

            self._ContentItem = contentItem
            self._Name = name
            self._Source = source
            self._SourceAccount = sourceAccount
            self._TypeValue = typeValue
        
        else:

            self._BackupUrl = _xmlFind(root, 'backupurl')
            self._BitRate = _xmlFind(root, 'bitrate')
            self._Description = _xmlFind(root, 'description')
            self._Format = _xmlFind(root, 'format')
            self._Location = _xmlFind(root, 'location')
            self._Logo = _xmlFind(root, 'logo')
            self._Mime = _xmlFind(root, 'mime')
            self._Name = _xmlFind(root, 'name')
            self._Playable = root.get('Playable')
            self._Reliability = _xmlFind(root, 'reliability')
            self._Token = _xmlFind(root, 'token')
            self._TypeValue = _xmlFind(root, 'type')
            self._Url = _xmlFind(root, 'url')
            self._UtcTime = _xmlFind(root, 'utctime')

            elmNode:Element = root.find('ContentItem')
            if elmNode is not None:
                self._ContentItem:ContentItem = ContentItem(root=elmNode)

            elmNode:Element = root.find('mediaItemContainer')
            if elmNode is not None:
                self._MediaItemContainer:MediaItemContainer = MediaItemContainer(root=elmNode)

            
    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    # implement sorting support.
    def __eq__(self, other):
        try:
            return self.Source == other.Source
        except Exception as ex:
            if (isinstance(self, NavigateItem )) and (isinstance(other, NavigateItem )):
                return self.Source == other.Source
            return False

    def __lt__(self, other):
        try:
            return self.Source < other.Source
        except Exception as ex:
            if (isinstance(self, NavigateItem )) and (isinstance(other, NavigateItem )):
                return self.Source < other.Source
            return False


    @property
    def BackupUrl(self) -> str:
        """ BackupUrl value. """
        return self._BackupUrl


    @property
    def BitRate(self) -> str:
        """ BitRate value. """
        return self._BitRate


    @property
    def ContentItem(self) -> ContentItem:
        """ 
        Parent container ContentItem to navigate, if navigating for child containers.  
        Specify null if navigating a root container.
        """
        return self._ContentItem


    @property
    def Description(self) -> str:
        """ Description value. """
        return self._Description


    @property
    def Format(self) -> str:
        """ Format value. """
        return self._Format


    @property
    def Location(self) -> str:
        """ Location value. """
        return self._Location


    @property
    def Logo(self) -> str:
        """ Logo value. """
        return self._Logo


    @property
    def MediaItemContainer(self) -> MediaItemContainer:
        """ MediaItemContainer value. """
        return self._MediaItemContainer


    @property
    def Mime(self) -> str:
        """ Mime value. """
        return self._Mime


    @property
    def Name(self) -> str:
        """ Name value. """
        return self._Name


    @property
    def Playable(self) -> str:
        """ Playable value. """
        return self._Playable


    @property
    def Reliability(self) -> str:
        """ Reliability value. """
        return self._Reliability


    @property
    def Token(self) -> str:
        """ Token value. """
        return self._Token


    @property
    def TypeValue(self) -> str:
        """ TypeValue value. """
        return self._TypeValue


    @property
    def Url(self) -> str:
        """ Url value. """
        return self._Url


    @property
    def UtcTime(self) -> str:
        """ UtcTime value. """
        return self._UtcTime


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('item')
        if self._Playable is not None: elm.set('Playable', str(self._Playable))

        if self._Name is not None and len(self._Name) > 0:
            elmNode = Element('name')
            elmNode.text = self._Name
            elm.append(elmNode)

        if self._TypeValue is not None and len(self._TypeValue) > 0:
            elmNode = Element('type')
            elmNode.text = self._TypeValue
            elm.append(elmNode)

        if self._Logo is not None and len(self._Logo) > 0:
            elmNode = Element('logo')
            elmNode.text = self._Logo
            elm.append(elmNode)

        if self._Token is not None and len(self._Token) > 0:
            elmNode = Element('token')
            elmNode.text = self._Token
            elm.append(elmNode)

        if self._BackupUrl is not None and len(self._BackupUrl) > 0:
            elmNode = Element('backupurl')
            elmNode.text = self._BackupUrl
            elm.append(elmNode)

        if self._BitRate is not None and len(self._BitRate) > 0:
            elmNode = Element('bitrate')
            elmNode.text = self._BitRate
            elm.append(elmNode)

        if self._Description is not None and len(self._Description) > 0:
            elmNode = Element('description')
            elmNode.text = self._Description
            elm.append(elmNode)

        if self._Format is not None and len(self._Format) > 0:
            elmNode = Element('format')
            elmNode.text = self._Format
            elm.append(elmNode)

        if self._Location is not None and len(self._Location) > 0:
            elmNode = Element('location')
            elmNode.text = self._Location
            elm.append(elmNode)

        if self._Mime is not None and len(self._Mime) > 0:
            elmNode = Element('mime')
            elmNode.text = self._Mime
            elm.append(elmNode)

        if self._Reliability is not None and len(self._Reliability) > 0:
            elmNode = Element('reliability')
            elmNode.text = self._Reliability
            elm.append(elmNode)

        if self._Url is not None and len(self._Url) > 0:
            elmNode = Element('url')
            elmNode.text = self._Url
            elm.append(elmNode)

        if self._UtcTime is not None and len(self._UtcTime) > 0:
            elmNode = Element('utctime')
            elmNode.text = self._UtcTime
            elm.append(elmNode)

        if self._ContentItem is not None:
            elmNode = self._ContentItem.ToElement()
            elm.append(elmNode)
            
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'NavigateItem:'
        if self._Name is not None and len(self._Name) > 0: msg = '%s Name="%s"' % (msg, str(self._Name))
        if self._TypeValue is not None and len(self._TypeValue) > 0: msg = '%s Type="%s"' % (msg, str(self._TypeValue))
        if self._BackupUrl is not None and len(self._BackupUrl) > 0: msg = '%s BackupUrl="%s"' % (msg, str(self._BackupUrl))
        if self._BitRate is not None and len(self._BitRate) > 0: msg = '%s BitRate="%s"' % (msg, str(self._BitRate))
        if self._Description is not None and len(self._Description) > 0: msg = '%s Description="%s"' % (msg, str(self._Description))
        if self._Format is not None and len(self._Format) > 0: msg = '%s Format="%s"' % (msg, str(self._Format))
        if self._Location is not None and len(self._Location) > 0: msg = '%s Location="%s"' % (msg, str(self._Location))
        if self._Logo is not None and len(self._Logo) > 0: msg = '%s Logo="%s"' % (msg, str(self._Logo))
        if self._Mime is not None and len(self._Mime) > 0: msg = '%s Mime="%s"' % (msg, str(self._Mime))
        if self._Reliability is not None and len(self._Reliability) > 0: msg = '%s Reliability="%s"' % (msg, str(self._Reliability))
        if self._Token is not None and len(self._Token) > 0: msg = '%s Token="%s"' % (msg, str(self._Token))
        if self._Url is not None and len(self._Url) > 0: msg = '%s Url="%s"' % (msg, str(self._Url))
        if self._UtcTime is not None and len(self._UtcTime) > 0: msg = '%s UtcTime="%s"' % (msg, str(self._UtcTime))
        if self._ContentItem is not None: msg = '%s %s' % (msg, str(self._ContentItem))
        if self._Playable is not None: msg = '%s Playable="%s"' % (msg, str(self._Playable))
        if self._MediaItemContainer is not None: msg = '%s %s' % (msg, str(self._MediaItemContainer))
        return msg 
