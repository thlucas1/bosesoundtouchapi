from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *
from xml.etree.ElementTree import Element
from xml.etree import ElementTree

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # update configuration for specified node.
    msg:SoundTouchMessage = client.Put(SoundTouchNodes.volume, '<volume>10</volume>')
    
    if msg != None:
        ElementTree.indent(msg.Response)  # for pretty printing
        responseEncoded = ElementTree.tostring(msg.Response, encoding="unicode")
        print("Put Response Message:\n%s" %  responseEncoded)

except Exception as ex:

    print("** Exception: %s" % str(ex))
