from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131")
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get introspect data for the TUNEIN source.
    introspect:Introspect = Introspect(SoundTouchSources.TUNEIN)
    xmlResponse:str = client.GetIntrospectData(introspect)
    print("\n%s - Response:\n%s" % (introspect.ToString(), xmlResponse))
            
    # get introspect data for the SPOTIFY source.
    introspect:Introspect = Introspect(SoundTouchSources.SPOTIFY, "SpotifyConnectUserName")
    xmlResponse:str = client.GetIntrospectData(introspect)
    print("\n%s - Response:\n%s" % (introspect.ToString(), xmlResponse))
            
    # get introspect data for the LOCAL_MUSIC source.
    introspect:Introspect = Introspect(SoundTouchSources.LOCAL_MUSIC, "3f205110-4a57-4e91-810a-ad949d25abb2")
    xmlResponse:str = client.GetIntrospectData(introspect)
    print("\n%s - Response:\n%s" % (introspect.ToString(), xmlResponse))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
