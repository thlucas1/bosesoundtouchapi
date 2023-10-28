from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:

    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.131") # Bose SoundTouch 10

    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # get current settings that will be restored by the snapshot.
    print("** Settings before StoreSnapshot ... **")
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("Now Playing: '%s' - '%s'" % (nowPlaying.ContentItem.Name, nowPlaying.ContentItem.Location))
    volume:Volume = client.GetVolume(True)
    print("Volume     : %s" % (volume.ToString()))
            
    # store current settings to snapshot.
    print("\n** Storing Snapshot ... **")
    client.StoreSnapshot()
    print("\n** Snapshot stored **\n")
            
    # select a different source.
    print("Changing Source ...")
    client.SelectSource(SoundTouchSources.BLUETOOTH)
            
    # change the volume level.
    print("Changing Volume to 30 ...")
    client.SetVolumeLevel(30)

    # mute the device.
    print("Changing Mute to On ...")
    client.mute_on()

    # get current settings before the snapshot restore.
    print("\n** Settings before RestoreSnapshot ... **")
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("Now Playing: '%s' - '%s'" % (nowPlaying.ContentItem.Name, nowPlaying.ContentItem.Location))
    volume:Volume = client.GetVolume(True)
    print("Volume     : %s" % (volume.ToString()))
    
    # if you don't want to restore a configuration, then simply delete 
    # it from the snapshot dictionary, like so:
    # if SoundTouchNodes.volume.Path in client.SnapshotSettings:
    #     client.SnapshotSettings.pop(SoundTouchNodes.volume.Path)
           
    # restore settings from snapshot.
    print("\n** Restoring Snapshot ... **")
    client.RestoreSnapshot()

    # get current settings after the snapshot restore.
    print("\n** Settings after RestoreSnapshot (should match settings before StoreSnapshot) ... **")
    nowPlaying:NowPlayingStatus = client.GetNowPlayingStatus(True)
    print("Now Playing: '%s' - '%s'" % (nowPlaying.ContentItem.Name, nowPlaying.ContentItem.Location))
    volume:Volume = client.GetVolume(True)
    print("Volume     : %s" % (volume.ToString()))
            
except Exception as ex:

    print("** Exception: %s" % str(ex))
