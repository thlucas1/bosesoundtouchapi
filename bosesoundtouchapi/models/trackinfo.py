# external package imports.
from typing import Iterator
from xml.etree.ElementTree import Element

# our package imports.
from ..bstutils import export

@export
class TrackInfo:
    """
    SoundTouch device TrackInfo configuration object.
       
    This class contains the attributes and sub-items that represent the 
    TrackInfo configuration of the device.      
    """

    def __init__(self, root:Element=None) -> None:
        """
        Initializes a new instance of the class.
        
        Args:
            root (Element):
                xmltree Element item to load arguments from.  
                If specified, then other passed arguments are ignored.
        """
        self._DeviceId:str = None
        self._TrackInfo:str = None

        if (root is None):
            
            pass
        
        elif root.tag == 'trackInfo':

            self._DeviceId = root.get('deviceID')
            self._TrackInfo = root.text


    def __repr__(self) -> str:
        return self.ToString()


    def __str__(self) -> str:
        return self.ToString()


    @property
    def DeviceId(self) -> str:
        """ Device ID that the configuration was obtained from. """
        return self._DeviceId


    @property
    def TrackInfo(self) -> str:
        """ 
        Track information value. 
        
        This information can differ slightly from the NowPlaying "Track" information, as it
        contains the track name plus extended details about the track.  The extended 
        details are delimited by a semi-colon; a semi-colon is still present after the track
        name if there is no extended data present.  For example(s):
        ```
        Who You Are To Me (feat. Lady A);vocal duets;upbeat lyrics;paired vocal harmony;  
        A Marshmallow World;  <- no extended track info
        ```
        """
        return self._TrackInfo


    def ToString(self) -> str:
        """
        Returns a displayable string representation of the class.
        """
        msg:str = 'TrackInfo:'
        msg = '%s TrackInfo="%s"' % (msg, str(self._TrackInfo))
        msg = '%s DeviceId="%s"' % (msg, str(self._DeviceId))
        return msg 
