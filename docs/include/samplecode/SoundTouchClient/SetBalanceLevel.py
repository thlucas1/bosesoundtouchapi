from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
import time

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # This test only works if the device is configured as part of a stereo pair.
    # this example will perform the following steps:
    # - set balance to minimum (left speaker).
    # - set balance to middle (both speakers).
    # - set balance to maximum (right speaker).
    # - restore balance to original value.

    print("Getting balance capability configuration ...")

    # get current balance levels and capabilities.
    balanceBefore:Balance = client.GetBalance(True)
    print("\nCurrent Balance Config: %s" % (balanceBefore.ToString()))
   
    # does the device have the capability to change the balance level?
    if balanceBefore.IsAvailable:

        # set balance to specific level.
        NEW_LEVEL:int = balanceBefore.Minimum
        print("Setting Balance level to Minimum: %s" % (NEW_LEVEL))
        client.SetBalanceLevel(NEW_LEVEL)

        # get current balance levels.
        balanceAfter:Balance = client.GetBalance(True)
        print("Current Balance Config: %s" % (balanceAfter.ToString()))
                
        # give the tester time to verify.
        time.sleep(3)
            
        # set balance to specific level.
        NEW_LEVEL:int = balanceBefore.Default
        print("Setting Balance level to Default: %s" % (NEW_LEVEL))
        client.SetBalanceLevel(NEW_LEVEL)

        # get current balance levels.
        balanceAfter:Balance = client.GetBalance(True)
        print("Current Balance Config: %s" % (balanceAfter.ToString()))

        # give the tester time to verify.
        time.sleep(5)
            
        # set balance to specific level.
        NEW_LEVEL:int = balanceBefore.Maximum
        print("Setting Balance level to Maximum: %s" % (NEW_LEVEL))
        client.SetBalanceLevel(NEW_LEVEL)

        # get current balance levels.
        balanceAfter:Balance = client.GetBalance(True)
        print("Current Balance Config: %s" % (balanceAfter.ToString()))

        # give the tester time to verify.
        time.sleep(5)
            
        # restore original level.
        NEW_LEVEL:int = balanceBefore.Actual
        print("Restoring original Balance level to: %s" % (NEW_LEVEL))
        client.SetBalanceLevel(NEW_LEVEL)

        # get current balance levels.
        balanceAfter:Balance = client.GetBalance(True)
        print("Current Balance Config: %s" % (balanceAfter.ToString()))
        
    else:
        
        print("\n** Device '%s' does not support changing balance levels!" % device.DeviceName)
                                  
except Exception as ex:

    print("** Exception: %s" % str(ex))
