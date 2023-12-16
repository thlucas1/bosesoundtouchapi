# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring
import xmltodict

# our package imports.
from ..bstutils import export
from .recent import Recent

@export
class RecentList:
    """
    SoundTouch device RecentList configuration object.
       
    This class contains the attributes and sub-items that represent the
    recent configuration of the device.
    
    The list of `Recent` objects are sorted by `CreatedOn` in descending
    order so that the last entry added to the recents list is the first 
    to appear in the list.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._LastUpdatedOn:int = 0
        self._Recents:list[Recent] = []
        
        if (root is None):

            pass

        else:

            for recent in root.findall('recent'):
                
                config:Recent = Recent(root=recent)
                self._Recents.append(config)
                
                if config.CreatedOn is not None and config.CreatedOn > self._LastUpdatedOn:
                    self._LastUpdatedOn = config.CreatedOn
                
            # sort items on CreatedOn property, descending order (latest first).
            if len(self._Recents) > 0:
                self._Recents.sort(key=lambda x: x.CreatedOn, reverse=True)


    def __getitem__(self, key) -> Recent:
        return self._Recents[key]


    def __iter__(self) -> Iterator:
        return iter(self._Recents)


    def __len__(self) -> int:
        return len(self._Recents)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def LastUpdatedOn(self) -> int:
        """ 
        Date and time (in epoch format) of when the recent list was last updated. 
        
        This is a helper property, and is not part of the SoundTouch WebServices API implementation.
        """
        return self._LastUpdatedOn

    @LastUpdatedOn.setter
    def LastUpdatedOn(self, value:int):
        """ 
        Sets the LastUpdatedOn property value.
        """
        if isinstance(value, int) and value > -1:
            self._LastUpdatedOn = value


    @property
    def Recents(self) -> list[Recent]:
        """ 
        The list of `Recent` items. 
        """
        return self._Recents


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
        elm = self.ToElement()
        xml = tostring(elm, encoding=encoding).decode(encoding)
        
        # convert xml to dictionary.
        oDict:dict = xmltodict.parse(xml,
                                     encoding=encoding,
                                     process_namespaces=False)
        return oDict


    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('recents')
        
        item:Recent
        for item in self._Recents:
            elm.append(item.ToElement())
        return elm

        
    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'RecentList:'
        msg = '%s LastUpdatedOn="%s"' % (msg, str(self._LastUpdatedOn))
        msg = "%s (%d items)" % (msg, len(self._Recents))
        
        if includeItems == True:
            item:Recent
            for item in self._Recents:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg


    def ToXmlString(self, encoding: str = 'utf-8') -> str:
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
