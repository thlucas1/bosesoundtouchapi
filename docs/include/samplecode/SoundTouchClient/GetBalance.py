from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    balance:Balance = client.GetBalance()
    print(balance.ToString())
    print("Balance Level = %d" % balance.Actual)

    # get cached configuration, refreshing from device if needed.
    balance:Balance = client.GetBalance(False)
    print("\nCached configuration:\n%s" % balance.ToString())
    print("Balance Level = %d" % balance.Actual)

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.balance.Path in client.ConfigurationCache:
        balance:Balance = client.ConfigurationCache[SoundTouchNodes.balance.Path]
        print("\nCached configuration, direct:\n%s" % balance.ToString())
        print("Balance Level = %d" % balance.Actual)
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
