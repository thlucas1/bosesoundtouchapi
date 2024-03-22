from bosesoundtouchapi import *
from bosesoundtouchapi.models import *
from bosesoundtouchapi.uri import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
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

    # various NAS Library containers in my environment.
    containerAlbumArtists:NavigateItem = NavigateItem(nasSource, nasSourceAccount, "Album Artists", "dir", location="107")
    containerAlbums:NavigateItem = NavigateItem(nasSource, nasSourceAccount, "Albums", "dir", location="7")
    containerAllArtists:NavigateItem = NavigateItem(nasSource, nasSourceAccount, "All Artists", "dir", location="6")
    containerAllMusic:NavigateItem = NavigateItem(nasSource, nasSourceAccount, "All Music", "dir", location="4")
    containerMusicPlaylists:NavigateItem = NavigateItem(nasSource, nasSourceAccount, "Music Playlists", "dir", location="F")

    # search NAS library "Root \ Music \ Music Playlists" for track name.
    search:Search = Search(nasSource, nasSourceAccount, SearchTerm("baby", SearchFilterTypes.Track), containerItem=containerMusicPlaylists)
    print("\nSearching Container: '%s' ..." % search.ContainerTitle)
    results:SearchResponse = client.SearchMusicLibrary(search)
    for navItem in results:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))

    # at this point, you can play any track in the returned results, like so:
    #client.PlayContentItem(results.Items[0].ContentItem)
           
    # search NAS library "Root \ Music \ All Music" for track name.
    search:Search = Search(nasSource, nasSourceAccount, SearchTerm("christmas", SearchFilterTypes.Track), containerItem=containerAllMusic)
    print("\nSearching Container: '%s' ..." % search.ContainerTitle)
    results:SearchResponse = client.SearchMusicLibrary(search)
    for navItem in results:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))
            
    # search NAS library "Root \ Music \ Album Artists" for artist name.
    search:Search = Search(nasSource, nasSourceAccount, SearchTerm("MercyMe", SearchFilterTypes.Artist), containerItem=containerAllArtists)
    print("\nSearching Container: '%s' ..." % search.ContainerTitle)
    results:SearchResponse = client.SearchMusicLibrary(search)
    for navItem in results:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))
            
    # search NAS library "Root \ Music \ Album Artists" for album artist name.
    search:Search = Search(nasSource, nasSourceAccount, SearchTerm("MercyMe", SearchFilterTypes.Artist), containerItem=containerAlbumArtists)
    print("\nSearching Container: '%s' ..." % search.ContainerTitle)
    results:SearchResponse = client.SearchMusicLibrary(search)
    for navItem in results:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))
            
    # search NAS library "Root \ Music \ Albums" for album name.
    search:Search = Search(nasSource, nasSourceAccount, SearchTerm("Welcome to the New", SearchFilterTypes.Album), containerItem=containerAlbums)
    print("\nSearching Container: '%s' ..." % search.ContainerTitle)
    results:SearchResponse = client.SearchMusicLibrary(search)
    for navItem in results:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))
            
    # search NAS library "Root \ Music \ Albums" for album name.
    search:Search = Search(nasSource, nasSourceAccount, SearchTerm("christmas", SearchFilterTypes.Album), containerItem=containerAlbums)
    print("\nSearching Container: '%s' ..." % search.ContainerTitle)
    results:SearchResponse = client.SearchMusicLibrary(search)
    for navItem in results:
        print("- %s (%s)" % (navItem.Name, navItem.ContentItem.Location))
                          
except Exception as ex:

    print("** Exception: %s" % str(ex))
