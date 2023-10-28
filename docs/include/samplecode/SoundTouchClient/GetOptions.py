from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # list available HTTP-Methods for a specific node.
    node:SoundTouchUri = SoundTouchNodes.volume
    methods:list = client.GetOptions(node)
    print("Options for '%s' node: %s" % (node.Path, str(methods)))
    
    # list available HTTP-Methods for ALL nodes supported by the device.
    node:SoundTouchUri
    for node in device.SupportedUris:
        methods:list = client.GetOptions(node)
        print("Options for '%s' node: %s" % (node.Path, str(methods)))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
