# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export, _xmlFindInt
from ..soundtouchmodelrequest import SoundTouchModelRequest
from .userratingtypes import UserRatingTypes

@export
class UserRating(SoundTouchModelRequest):
    """
    SoundTouch device UserRating configuration object.
       
    This class contains the attributes and sub-items that represent the 
    UserRating configuration of the device.      
    """

    def __init__(self, rating:UserRatingTypes=None,
                 root:Element=None
                 ) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            rating (str):
                User rating value to set.
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._Rating:str = None

        if (root is None):
            
            if isinstance(rating, UserRatingTypes):
                rating = rating.value
                
            self._Rating = rating

        else:

            self._Rating = root.text


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def Rating(self) -> str:
        """ User Rating value. """
        return self._Rating

    
    def ToElement(self, isRequestBody:bool=False) -> Element:
        """ 
        Overridden.  
        Returns an xmltree Element node representation of the class. 

        Args:
            isRequestBody (bool):
                True if the element should only return attributes needed for a POST
                request body; otherwise, False to return all attributes.
        """
        elm = Element('Rating')
        if isRequestBody == True:
    
            if self._Rating is not None:
                elm.text = self._Rating
            
        else:
            
            if self._Rating and len(self._Rating) > 0: elm.text = self._Rating
                
        return elm

        
    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'Rating:'
        if self._Rating is not None: msg = '%s %s' % (msg, self._Rating)
        return msg 
    