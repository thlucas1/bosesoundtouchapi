from bosesoundtouchapi import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10

    # display device basic details and all installed components.
    print(device.ToString(True))

    # iterate over all components that match the given category.
    print("\nDisplaying specific components - SCM ...")
    for component in device.GetComponents('SCM'):
        print(component.ToString())
            
    # iterate over all components that match the given category.
    print("\nDisplaying specific components - LPM ...")
    for component in device.GetComponents('LPM'):
        print(component.ToString())
            
    # iterate over all components that match the given category.
    print("\nDisplaying specific components - LPMBL ...")
    for component in device.GetComponents('LPMBL'):
        print(component.ToString())
            
    # iterate over all components that match the given category.
    print("\nDisplaying specific components - BASS ...")
    for component in device.GetComponents('BASS'):
        print(component.ToString())

    # dump the webapi list of uri's this device supports.
    print("\nSupported URI's for device '%s':" % (device.DeviceName))
    for item in device.SupportedUris:
        print("- %s" % (str(item)))
            
except Exception as ex:

    print("** Exception: %s" % str(ex))
