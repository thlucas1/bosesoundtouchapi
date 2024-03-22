from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # manually make a request to the volume status node.
    volume:Volume = Volume(25)
    print("\nVolume object:\n%s" % volume.ToString())
    reqBody:str = volume.ToXmlRequestBody()
    message = SoundTouchMessage(SoundTouchNodes.volume, reqBody)
    client.MakeRequest('POST', message)
    print("\nMakeRequest Response:\n%s" % message.XmlMessage)

except Exception as ex:

    print("** Exception: %s" % str(ex))
