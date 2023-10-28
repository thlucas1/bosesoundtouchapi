from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current nowPlaying status.
    nowPlayingBefore:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\n** Current Now Playing Status:\n%s" % nowPlayingBefore.ToString())

    # create various content items to play.
    contentRadio01:ContentItem = ContentItem("TUNEIN","stationurl","/v1/playback/station/s249983","",True,"Christian Hits")
    contentRadio02:ContentItem = ContentItem("TUNEIN","stationurl","/v1/playback/station/s309605","",True,"K-LOVE 90s")

    # ensure the now playing changes.
    selection:ContentItem = contentRadio01
    if nowPlayingBefore.ContentItem != None:
        if nowPlayingBefore.ContentItem.Location == contentRadio01.Location:
            selection = contentRadio02

    # selects the specified content item.
    print("\n** Playing content item: %s - %s ..." % (selection.Name, selection.Location))
    client.SelectContentItem(selection)

    # create various content items to play.
    selections:list = []
    selections.append(ContentItem("TUNEIN","stationurl","/v1/playback/station/s249983",None,True,"Christian Hits"))
    selections.append(ContentItem("UPNP",None,"http://192.168.1.186:8123/api/tts_proxy/c96b99f3a949febd2a1f680e3b6dc4f01eb67e68_en_-_google_translate.mp3","UPnPUserName",True))
    selections.append(ContentItem("LOCAL_INTERNET_RADIO","stationurl","https://content.api.bose.io/core02/svc-bmx-adapter-orion/prod/orion/station?data=eyJuYW1lIjoiSm1uIDgwOTYiLCJpbWFnZVVybCI6IiIsInN0cmVhbVVybCI6Imh0dHA6Ly9qbThuLi5jb20vODA5Ni9zdHJlYW0ifQ%3D%3D",None,True,"Jmn 8096"))
    selections.append(ContentItem("TUNEIN","stationurl","/v1/playback/station/s309605",None,True,"K-LOVE 90s"))

    # play them all
    selection:ContentItem
    for selection in selections:
        print("\n** Playing content item: %s - %s ..." % (selection.Name, selection.Location))
        client.SelectContentItem(selection, 10)
            
    print("\n** Restoring original source ...")

    # play original source (if one was selected).
    if nowPlayingBefore.ContentItem.Source != "STANDBY":
        client.SelectContentItem(nowPlayingBefore.ContentItem)

    # get current nowPlaying status.
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("\n** Updated Now Playing Status:\n%s" % nowPlaying.ToString())
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
