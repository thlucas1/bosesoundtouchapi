from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # the following shows how to traverse the structure of a NAS Music Library.
    # in this example, my NAS Music Library has the following containers defined:
    # - Root container
    # -- Music
    # ---- Albums
    # ------ Welcome to the New
    # ------ ... and more (albums from other artists)
    # ---- ... and more (Album Artists, All Artists, All Music, Composers, Genre, etc)
    # -- ... and more (Pictures, PlayLists, Videos)

    # set NAS library source to access.
    nasSource:str = SoundTouchSources.STORED_MUSIC.value
    nasSourceAccount:str = "d09708a1-5953-44bc-a413-7d516e04b819/0"
    navItem:NavigateItem = None

    # this example show how to return all tracks for a specific album; it requires that
    # you know the specific name and location of the container as its defined to your library.

    # get NAS library content - static container.
    # the "7_114e8de9" location maps to: Root \ Music \ Albums \ "Welcome to the New" album container.
    staticContainer:NavigateItem = NavigateItem(nasSource, nasSourceAccount, typeValue="dir", name="Welcome to the New", location="7_114e8de9")
    criteria:Navigate = Navigate(nasSource, nasSourceAccount, staticContainer)
    print("\nNavigating Container: '%s' ..." % criteria.ContainerTitle)
    tracksContainer:NavigateResponse = client.GetMusicLibraryItems(criteria)
    for navItem in tracksContainer:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))

    # at this point, I can play any track in the returned results, like so (track 1 selected):
    #client.PlayContentItem(tracksContainer.Items[0].ContentItem)

    # or even play the whole album (parent container):
    #client.PlayContentItem(tracksContainer.Items[0].MediaItemContainer.ContentItem)


    # the following examples show how to navigate your library starting at the root container,
    # and work your way down to a specific album container.

    # get NAS library content - Root container.
    criteria:Navigate = Navigate(nasSource, nasSourceAccount)
    print("\nNavigating Container: '%s' ..." % criteria.ContainerTitle)
    rootContainer:NavigateResponse = client.GetMusicLibraryItems(criteria)
    for navItem in rootContainer:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))

    # get NAS library content - Root \ Music container.
    criteria:Navigate = Navigate(nasSource, nasSourceAccount, rootContainer.GetItemByName("Music"))
    print("\nNavigating Container: '%s' ..." % criteria.ContainerTitle)
    musicContainer:NavigateResponse = client.GetMusicLibraryItems(criteria)
    for navItem in musicContainer:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))

    # get NAS library content - Root \ Music \ Albums container.
    criteria:Navigate = Navigate(nasSource, nasSourceAccount, musicContainer.GetItemByName("Albums"))
    print("\nNavigating Container: '%s' ..." % criteria.ContainerTitle)
    albumsContainer:NavigateResponse = client.GetMusicLibraryItems(criteria)
    for navItem in albumsContainer:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))

    # get NAS library content - Root \ Music \ Albums \ "Welcome to the New" album container.
    criteria:Navigate = Navigate(nasSource, nasSourceAccount, albumsContainer.GetItemByName("Welcome to the New"))
    print("\nNavigating Container: '%s' ..." % criteria.ContainerTitle)
    tracksContainer:NavigateResponse = client.GetMusicLibraryItems(criteria)
    for navItem in tracksContainer:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))
           
    # sort the results (in place) by Name, ascending order.
    tracksContainer.Items.sort(key=lambda x: (x.ContentItem.Name or "").lower(), reverse=True)
    print("\nList sorted by Name descending:")
    for navItem in tracksContainer:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))
        
except Exception as ex:

    print("** Exception: %s" % str(ex))
