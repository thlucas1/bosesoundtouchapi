import time
from bosesoundtouchapi import *
from bosesoundtouchapi.models import *

try:
    
    # create SoundTouch device instance.
    device:SoundTouchDevice = SoundTouchDevice("192.168.1.81") # Bose SoundTouch 10
            
    # create SoundTouch client instance from device.
    client:SoundTouchClient = SoundTouchClient(device)

    # use google text to speech to say a message.
    print("\nSaying message via Google TTS (language=EN) ...")
    client.PlayNotificationTTS("There is activity at the front door.")
   
    # if playing messages back to back, then give the message time to play
    # before playing the next one; otherwise the next message is lost.
    time.sleep(6)

    # use google text to speech to say a message.
    print("\nSaying message via Google TTS (language=DE) ...")
    client.PlayNotificationTTS("There is activity at the front door.", 
                               "http://translate.google.com/translate_tts?ie=UTF-8&tl=DE&client=tw-ob&q={saytext}",
                               volumeLevel=30)
   
    # if playing messages back to back, then give the message time to play
    # before playing the next one; otherwise the next message is lost.
    time.sleep(6)

    # use google text to speech to say a message.
    print("\nSaying message via Google TTS (language=EN) ...")
    client.PlayNotificationTTS("There is activity at the front door.", 
                               "http://translate.google.com/translate_tts?ie=UTF-8&tl=EN&client=tw-ob&q={saytext}",
                               "Activity Detected", # <- appears in nowPlaying.Artist
                               "Front Door",        # <- appears in nowPlaying.Album
                               "Motion Sensor",     # <- appears in nowPlaying.Track
                               volumeLevel=20)

    # if playing messages back to back, then give the message time to play
    # before playing the next one; otherwise the next message is lost.
    time.sleep(6)

    # use google text to speech to say a message using a custom Bose developer appKey.
    print("\nSaying message via Google TTS (language=EN) ...")
    client.PlayNotificationTTS("There is activity at the front door.", 
                               appKey="YourBoseAppKey")
       
except Exception as ex:

    print("** Exception: %s" % str(ex))
