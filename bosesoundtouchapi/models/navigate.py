# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# our package imports.
from ..bstutils import export
from ..soundtoucherror import SoundTouchError
from ..soundtouchmenutypes import SoundTouchMenuTypes
from ..soundtouchmodelrequest import SoundTouchModelRequest
from ..soundtouchsources import SoundTouchSources

# get smartinspect logger reference; create a new session for this module name.
import logging
from smartinspectpython.siauto import SIAuto, SISession
_logsi:SISession = SIAuto.Si.GetSession(__package__)
if (_logsi == None):
    _logsi = SIAuto.Si.AddSession(__package__, True)
_logsi.SystemLogger = logging.getLogger(__package__)


@export
class Navigate(SoundTouchModelRequest):
    """
    SoundTouch device Navigate configuration object.
       
    This class contains the attributes and sub-items that represent
    Navigate criteria.
    """

    def __init__(self, source:str=None, sourceAccount:str=None, menu:str=None, startItem:int=None, numItems:int=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            source (str):
                Music service source to navigate (e.g. "PANDORA", "SPOTIFY", etc).
            sourceAccount (str):
                Music service source account (e.g. the music service user-id).
            menu (str):
                Music service menu to navigate (e.g. "radioStations", etc).
            startItem (int):
                Starting item number to return information for.
            numItems (int):
                Number of items to return.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
                
        Raises:
            SoundTouchError:
                startItem argument was not of type int.  
        """
        # initialize storage.
        self._Menu:str = None
        self._NumItems:int = None
        self._Source:str = None
        self._SourceAccount:str = None
        self._StartItem:int = None
        
        if (root is None):
            
            # convert enums to strings.
            if isinstance(menu, SoundTouchMenuTypes):
                menu = str(menu.value)
            if isinstance(source, SoundTouchSources):
                source = str(source.value)
                
            # validations.
            if numItems is not None:
                if not isinstance(numItems, int):
                    raise SoundTouchError('numItems argument was not of type int', logsi=_logsi)
            if startItem is not None:
                if not isinstance(startItem, int):
                    raise SoundTouchError('startItem argument was not of type int', logsi=_logsi)

            # base fields.
            self._Menu = menu
            self._NumItems = numItems
            self._Source = source
            self._SourceAccount = sourceAccount
            self._StartItem = startItem
        
        elif root.tag == 'navigate':

            # base fields.
            self._Menu = root.get('menu', default=None)
            self._Source = root.get('source', default=None)
            self._SourceAccount = root.get('sourceAccount', default=None)
            

    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Menu(self) -> str:
        """ Music service menu to navigate (e.g. "radioStations", etc). """
        return self._Menu

    @Menu.setter
    def Menu(self, value:str):
        """ 
        Sets the Menu property value.
        """
        if value is not None:
            if isinstance(value, SoundTouchMenuTypes):
                self._Menu = value.value
            elif isinstance(value, str):
                self._Menu = value


    @property
    def NumItems(self) -> int:
        """ Number of items to return. """
        return self._NumItems

    @NumItems.setter
    def NumItems(self, value:int):
        """ 
        Sets the NumItems property value.
        """
        if value != None:
            if isinstance(value, int):
                self._NumItems = value


    @property
    def Source(self) -> str:
        """ Music service source to navigate (e.g. "PANDORA", "SPOTIFY", etc). """
        return self._Source

    @Source.setter
    def Source(self, value:str):
        """ 
        Sets the Source property value.
        """
        if value is not None:
            if isinstance(value, SoundTouchSources):
                self._Source = value.value
            elif isinstance(value, str):
                self._Source = value


    @property
    def SourceAccount(self) -> str:
        """ Music service source account (e.g. the music service user-id). """
        return self._SourceAccount

    @SourceAccount.setter
    def SourceAccount(self, value:str):
        """ 
        Sets the SourceAccount property value.
        """
        if value is not None:
            if isinstance(value, str):
                self._SourceAccount = value


    @property
    def StartItem(self) -> int:
        """ Starting item number to return information for. """
        return self._StartItem

    @StartItem.setter
    def StartItem(self, value:int):
        """ 
        Sets the StartItem property value.
        """
        if value != None:
            if isinstance(value, int):
                self._StartItem = value


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('navigate')
        if self._Source and len(self._Source) > 0: elm.set('source', str(self._Source))
        if self._SourceAccount and len(self._SourceAccount) > 0: elm.set('sourceAccount', str(self._SourceAccount))
        if self._Menu and len(self._Menu) > 0: elm.set('menu', str(self._Menu))

        if (self._StartItem is not None) and (self._StartItem > 0):
            elmStartItem = Element('startItem')
            elmStartItem.text = str(self._StartItem)
            elm.append(elmStartItem)

        if (self._NumItems is not None) and (self._NumItems > 0):
            elmNumItems = Element('numItems')
            elmNumItems.text = str(self._NumItems)
            elm.append(elmNumItems)

        return elm
        
        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Navigate:'
        msg = '%s Source="%s"' % (msg, str(self._Source))
        msg = '%s SourceAccount="%s"' % (msg, str(self._SourceAccount))
        msg = '%s Menu="%s"' % (msg, str(self._Menu))
        msg = '%s StartItem=%s' % (msg, str(self._StartItem))
        msg = '%s NumItems=%s' % (msg, str(self._NumItems))
        return msg 
    