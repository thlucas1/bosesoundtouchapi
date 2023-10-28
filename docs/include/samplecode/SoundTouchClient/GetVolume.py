from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get real-time configuration from the device.
    volume:Volume = client.GetVolume()
    print(volume.ToString())
    print("Volume Level = %d" % volume.Actual)

    # get cached configuration, refreshing from device if needed.
    volume:Volume = client.GetVolume(False)
    print("\nCached configuration:\n%s" % volume.ToString())
    print("Volume Level = %d" % volume.Actual)

    # get cached configuration directly from the configuration manager dictionary.
    if SoundTouchNodes.volume.Path in client.ConfigurationCache:
        volume:Volume = client.ConfigurationCache[SoundTouchNodes.volume.Path]
        print("\nCached configuration, direct:\n%s" % volume.ToString())
        print("Volume Level = %d" % volume.Actual)

except Exception as ex:

    print("** Exception: %s" % str(ex))
