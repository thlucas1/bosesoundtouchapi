# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export
from .surveyresultitem import SurveyResultItem

@export
class PerformWirelessSiteSurveyResponse:
    """
    SoundTouch device PerformWirelessSiteSurveyResponse configuration object.
       
    This class contains the attributes and sub-items that represent the
    UPnP media server configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._SurveyResultItems = []

        if (root is None):

            pass

        else:

            elmItems:Element = root.find('items')
            if elmItems is not None:
                elmItem:Element
                for elmItem in elmItems.findall('item'):
                    self._SurveyResultItems.append(SurveyResultItem(root=elmItem))

            # sort items on FriendlyName property, ascending order.
            if len(self._SurveyResultItems) > 0:
                self._SurveyResultItems.sort(key=lambda x: (x.Ssid or "").lower(), reverse=False)


    def __getitem__(self, key) -> SurveyResultItem:
        return self._SurveyResultItems[key]


    def __iter__(self) -> Iterator:
        return iter(self._SurveyResultItems)


    def __len__(self) -> int:
        return len(self._SurveyResultItems)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def SurveyResultItems(self) -> list[SurveyResultItem]:
        """ 
        The list of `SurveyResultItem` items. 
        """
        return self._SurveyResultItems


    def ToString(self, includeItems:bool=False) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base list.
        """
        msg:str = 'PerformWirelessSiteSurveyResponse:'
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            item:SurveyResultItem
            for item in self:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
