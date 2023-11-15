# our package imports.
from bosesoundtouchapi import *

try:

    print("Test Starting\n")

    # create a new instance of the discovery class.
    # we will verify device connections, as well as print device details
    # to the console as they are discovered.
    discovery:SoundTouchDiscovery = SoundTouchDiscovery(True, printToConsole=True)

    # discover SoundTouch devices on the network, waiting up to 
    # 5 seconds for all devices to be discovered.
    discovery.DiscoverDevices(timeout=5)
            
    # print all discovered devices.
    print("\n%s" % (discovery.ToString(True)))
                   
except Exception as ex:

    print(str(ex))
    raise
        
finally:
            
    print("\nTests Completed")
