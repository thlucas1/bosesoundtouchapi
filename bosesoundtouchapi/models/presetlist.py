# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring
import xmltodict

# our package imports.
from ..bstutils import export
from .preset import Preset

@export
class PresetList:
    """
    SoundTouch device PresetList configuration object.
       
    This class contains the attributes and sub-items that represent the
    preset configuration of the device.
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Presets:list[Preset] = []
        
        if (root is None):

            pass

        else:

            for preset in root.findall('preset'):
                self.append(Preset(root=preset))


    def __getitem__(self, key) -> Preset:
        return self._Presets[key]


    def __iter__(self) -> Iterator:
        return iter(self._Presets)


    def __len__(self) -> int:
        return len(self._Presets)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Presets(self) -> list[Preset]:
        """ 
        The list of `Preset` items. 
        """
        return self._Presets


    def append(self, value: Preset):
        """
        Append a new `Preset` item to the list.
        
        Args:
            value:
                The `Preset` object to append.
        """
        self._Presets.append(value)


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


    def ToElement(self) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 
        """
        elm = Element('presets')
        
        item:Preset
        for item in self:
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
        msg:str = 'PresetList:'
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            item:Preset
            for item in self:
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
