# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

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
        self._LastUpdatedOn:int = 0
        self._Presets:list[Preset] = []
        
        if (root is None):

            pass

        else:

            for preset in root.findall('preset'):
                
                config:Preset = Preset(root=preset)
                self._Presets.append(config)
                
                if config.CreatedOn is not None and config.CreatedOn > self._LastUpdatedOn:
                    self._LastUpdatedOn = config.CreatedOn
                if config.UpdatedOn is not None and config.UpdatedOn > self._LastUpdatedOn:
                    self._LastUpdatedOn = config.UpdatedOn


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
    def LastUpdatedOn(self) -> int:
        """ 
        Date and time (in epoch format) of when the preset list was last updated. 
        
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
    def Presets(self) -> list[Preset]:
        """ 
        The list of `Preset` items. 
        """
        return self._Presets


    def ToDictionary(self, encoding:str='utf-8', includeEmptyPresets:bool=False) -> dict:
        """
        Returns a dictionary representation of the class.
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.
            includeEmptyPresets (bool):
                True if the method should return all 6 preset slots, including empty ones;
                otherwise, False (default) to return only presets with content items.
        """
        if encoding is None:
            encoding = 'utf-8'
            
        presets:list = []
        
        # process all possible presets.
        maxPresetCount:int = 6
        for presetId in range(1, maxPresetCount + 1):
            
            # search for preset id in the list.
            isEmpty:bool = True
            item:Preset
            for item in self._Presets:
                if item.PresetId == presetId:
                    # found it - add it to the list.
                    presets.append(item.ToDictionary(encoding))
                    isEmpty = False
                    break
                
            # did we find a preset for this id?  if not and we are adding
            # empty presets, then create an empty preset and add it to the list.
            if isEmpty == True and includeEmptyPresets == True:
                item = Preset(presetId, name="empty preset")
                presets.append(item.ToDictionary(encoding))

        result:dict = {}
        
        if self._LastUpdatedOn is not None: 
            result['LastUpdatedOn'] = self._LastUpdatedOn
        result['Presets'] = presets

        return result
        

    def ToElement(self, isRequestBody:bool=False, includeEmptyPresets:bool=False) -> Element:
        """ 
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the method should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
            includeEmptyPresets (bool):
                True if the method should return all 6 preset slots, including empty ones;
                otherwise, False (default) to return only presets with content items.
        """
        elm = Element('presets')

        # process all possible presets.
        maxPresetCount:int = 6
        for presetId in range(1, maxPresetCount + 1):
            
            # search for preset id in the list.
            isEmpty:bool = True
            item:Preset
            for item in self._Presets:
                if item.PresetId == presetId:
                    # found it - add it to the list.
                    elm.append(item.ToElement())
                    isEmpty = False
                    break
                
            # did we find a preset for this id?  if not and we are adding
            # empty presets, then create an empty preset and add it to the list.
            if isEmpty == True and includeEmptyPresets == True:
                item = Preset(presetId, name="empty preset")
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
        msg = '%s LastUpdatedOn="%s"' % (msg, str(self._LastUpdatedOn))
        msg = "%s (%d items)" % (msg, len(self._Presets))
        
        if includeItems == True:
            item:Preset
            for item in self._Presets:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg


    def ToXmlString(self, encoding:str='utf-8', includeEmptyPresets:bool=False) -> str:
        """ 
        Returns an xml string representation of the class. 
        
        Args:
            encoding (str):
                encode type (e.g. 'utf-8', 'unicode', etc).  
                Default is 'utf-8'.
            includeEmptyPresets (bool):
                True if the method should return all 6 preset slots, including empty ones;
                otherwise, False (default) to return only presets with content items.
        """
        if encoding is None:
            encoding = 'utf-8'
        elm = self.ToElement(includeEmptyPresets=includeEmptyPresets)
        xml = tostring(elm, encoding=encoding).decode(encoding)
        return xml
