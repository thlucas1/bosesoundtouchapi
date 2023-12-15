# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export
from .service import Service

@export
class ServiceAvailability:
    """
    SoundTouch device ServiceAvailability configuration object.
       
    This class contains the attributes and sub-items that represent the
    service availability configuration of the device.
    """

    def __init__(self, root:Element) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Services:list[Service] = []
        
        if (root is None):

            pass

        else:

            elmServices:Element = root.find('services')
            for service in elmServices.findall('service'):
                self._Services.append(Service(root=service))
            
            # sort items on ServiceType property, ascending order.
            if len(self._Services) > 0:
                self._Services.sort(key=lambda x: (x.ServiceType or "").lower(), reverse=False)


    def __getitem__(self, key) -> Service:
        return self._Services[key]


    def __iter__(self) -> Iterator:
        return iter(self._Services)


    def __len__(self) -> int:
        return len(self._Services)


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def ServiceCount(self) -> int:
        """ 
        The total number of services defined. 
        """
        return len(self._Services)


    @property
    def Services(self) -> list[Service]:
        """ 
        The list of `Service` items. 
        """
        return self._Services


    def ToString(self, includeItems:bool=True) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base attributes.
        """
        msg:str = 'ServiceAvailability:'
        msg = "%s (%d items)" % (msg, len(self._Services))
        
        if includeItems == True:
            item:Service
            for item in self._Services:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
