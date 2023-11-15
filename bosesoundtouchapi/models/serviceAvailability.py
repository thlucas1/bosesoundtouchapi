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
        self._services = []
        
        if (root is None):
            
            pass  # no other parms to process.
        
        else:

            # base fields.
            elmServices:Element = root.find('services')
        
            for service in elmServices.findall('service'):
                self.append(Service(root=service))
            
            # sort items on ServiceType property, ascending order.
            if len(self._services) > 0:
                self._services.sort(key=lambda x: x.ServiceType, reverse=False)


    def __getitem__(self, key) -> Service:
        return self._services[key]


    def __iter__(self) -> Iterator:
        return iter(self._services)


    def __len__(self) -> int:
        return len(self._services)


    def __repr__(self) -> str:
        return self.ToString()


    @property
    def ServiceCount(self) -> int:
        """ 
        The total number of services defined. 
        """
        return len(self._services)


    def append(self, value:Service):
        """
        Append a new `Service` item to the list.
        
        Args:
            value:
                The `Service` object to append.
        """
        self._services.append(value)


    def ToString(self, includeItems:bool=True) -> str:
        """
        Returns a displayable string representation of the class.
        
        Args:
            includeItems (bool):
                True to include all items in the list; otherwise False to only
                include the base attributes.
        """
        msg:str = 'ServiceAvailability:'
        msg = "%s (%d items)" % (msg, self.__len__())
        
        if includeItems == True:
            item:Service
            for item in self:
                msg = "%s\n- %s" % (msg, item.ToString())
            
        return msg
