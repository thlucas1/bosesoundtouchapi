# external package imports.
from xml.etree.ElementTree import Element

# our package imports.
from bosesoundtouchapi import *
from bosesoundtouchapi.firmware import *

print("** Test Starting\n")

try:
    
    # get SoundTouch firmware update index.xml data.
    print("\nRetrieving index.xml document from: %s" % BOSE_SOUNDTOUCH_UPDATE_INDEX_URL)
    index:Element = SoundTouchFirmware.GetIndex(BOSE_SOUNDTOUCH_UPDATE_INDEX_URL)
    
    # create list of SoundTouchFirmware objects from index.xml data.
    print("\nParsing index.xml document ...")
    firmwareList:list = SoundTouchFirmware.LoadIndex(index)
    
    # print SoundTouchFirmware object summary.
    print("\nFirmware items found:")
    for item in firmwareList:
        print(item.ToString())

except Exception as ex:

    print("** Exception: %s" % str(ex))
        
finally:
            
    print("\n** Test Completed")
