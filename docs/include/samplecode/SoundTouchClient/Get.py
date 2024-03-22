from bosesoundtouchapi import *
from bosesoundtouchapi.uri import *
from xml.etree.ElementTree import Element
from xml.etree import ElementTree

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get configuration for specified node.
    msg:SoundTouchMessage = client.Get(SoundTouchNodes.volume)
    
    if msg != None:
        ElementTree.indent(msg.Response)  # for pretty printing
        responseEncoded = ElementTree.tostring(msg.Response, encoding="unicode")
        print("Get Response Message:\n%s" %  responseEncoded)

except Exception as ex:

    print("** Exception: %s" % str(ex))
