from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    requestToken:SimpleConfig = client.GetRequestToken()
    print(requestToken.ToString())
    print("\nToken = '%s'" % requestToken.Attribute['value'])

    # get cached configuration, refreshing from device if needed.
    requestToken:SimpleConfig = client.GetRequestToken(False)
    print("\nCached configuration:\n%s" % requestToken.ToString())
    print("\nToken = '%s'" % requestToken.Attribute['value'])

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.requestToken.Path in client.ConfigurationCache:
        requestToken:SimpleConfig = client.ConfigurationCache[SoundTouchNodes.requestToken.Path]
        print("\nCached configuration, direct:\n%s" % requestToken.ToString())
        print("\nToken = '%s'" % requestToken.Attribute['value'])
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
