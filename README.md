<h1 class="modulename">
Bose SoundTouch API Python3 Library
</h1>

## Overview
This API provides Python programmers the ability to control Bose SoundTouch speakers from any program written in Python 3.

It utilizes the Bose SoundTouch Webservices API, which is hosted on each SoundTouch device.

More information about Bose SoundTouch speakers can be found on the <a href="https://www.boselatam.com/en_ar/products/speakers/smart_home/soundtouch_family.html" target="_blank">Bose SoundTouch Family page</a>.

## Features

The following features are supported by this API.
- Media Player controls (play pause, resume, next track, prev track, repeat, shuffle, etc)
- Media Content (streaming radio, play http or https url, Google TTS)
- Media Volume control (set / retrieve, tick up / down, mute, smart mute)
- Select Sources (Aux, Bluetooth, Airplay, Deezer, Spotify, iHeart, SiriusXm, etc)
- Multi-room Zone functions (create zone, add / remove zone members, syncronized play)
- Power functions (smart power on / off, power toggle, power to standby)
- Audio mode switching (Normal, Dialog, etc)
- Audio Tone Controls for Bass Level (set, retrieve, supported min / max values)
- Audio Tone Controls for Treble Level (set, retrieve, supported min / max values)
- Audio Product CEC HDMI Control support (set, retrieve, supported values)
- Presets (store, remove, remove all, select)
- Recent Media History (list recent content that was played, select recent item for play)
- Favorites (add, remove, thumbs up, thumbs down)
- Snapshot device settings (store, restore)
- Change Device Name
- Configuration data (clock time, clock, timezone, capabilities, bass capabilities)
- Notifications (receive real-time status updates from the device)
- Zeroconf (aka MDNS) discovery of SoundTouch devices on the network
- ID3 tag support for media content played from a url
- ... and more

## Requirements and Dependencies
The following requirements must be met in order to utilize this API:

* Bose SoundTouch Speaker(s) that support the SoundTouch Webservices API.
    - SoundTouch 10
    - SoundTouch 300
    - I have only tested with the above (what can I say; Bose products are expensive, and I can only afford the two! :D )
    - Other SoundTouch devices should be compatible.
    - Note that the newer line of Bose Speakers (Home Speaker 500, 700, etc) are NOT supported as they do not utilize the Bose WebServices API.

The following Python-related requirements must be met in order to utilize this API:

* Python 3.4 or greater (Python 2 not supported).
* smartinspectPython package (>= 3.0.21) - for diagnostics and logging support.
* websocket-client package (>= 2.0).
* urllib3 package (>= 1.2.0).

## Documentation
Documentation is located in the package library under the 'docs' folder; use the index.html as your starting point. 
You can also view the latest docs on the <a href="https://bosesoundtouchapi.readthedocs.io/en/latest/__init__.html" target="_blank">readthedocs web-site</a>.

## Installation

This module can be easily installed via pip:
``` bash
$ python3 -m pip install bosesoundtouchapi
```

## Quick-Start Sample Code

Almost every method is documented with sample code; just click on the "Sample Code" links under the method, and use the "Copy to Clipboard" functionality to copy / paste.

Check out the following classes to get you started:
- `bosesoundtouchapi.soundtouchclient.SoundTouchClient` - device controls and data gathering.  
- `bosesoundtouchapi.soundtouchdiscovery.SoundTouchDiscovery` - device discovery via Zeroconf.  
- `bosesoundtouchapi.ws.soundtouchwebsocket.SoundTouchWebSocket` - web-socket notification support.  

## Licensing
This project is licensed and distributed under the terms of the MIT End-User License Agreement (EULA) license.

Portions of this code and the overall "flow" were taken from contributions made by <a href="https://github.com/MatrixEditor" target="_blank">MatrixEditor</a>.  My original intent was to fork his repository and add some changes, but there were just too many and I wanted to change some things that would have broken backward compatibility so I continued with my own repository.  

## Logging / Tracing Support

The SmartInspectPython package (installed with this package) can be used to easily debug your applications that utilize this API.

The following topics and code samples will get you started on how to enable logging support.  
Note that logging support can be turned on and off without changing code or restarting the application.  
Click on the topics below to expand the section and reveal more information.  

<details>
  <summary>Configure Logging Support Settings File</summary>
  <br/>
  Add the following lines to a new file (e.g. "smartinspect.cfg") in your application startup / test directory.  
  Note the file name can be whatever you like, just specify it on the call to `SiAuto.Si.LoadConfiguration()` when initializing the logger.

``` ini
; smartinspect.cfg

; SmartInspect Logging Configuration General settings.
; - "Enabled" parameter to turn logging on (True) or off (False).
; - "Level" parameter to control the logging level (Debug|Verbose|Message|Warning|Error).
; - "AppName" parameter to control the application name.
Enabled = False 
Level = Verbose
DefaultLevel = Debug
AppName = My Application Name

; SmartInspect Logging Configuration Output settings.
; - Log to SmartInspect Console Viewer running on the specified network address.
Connections = tcp(host=192.168.1.1,port=4228,timeout=5000,reconnect=true,reconnect.interval=10s,async.enabled=true)
; - Log to a file, keeping 14 days worth of logs.
;Connections = "file(filename=\"./tests/logfiles/logfile.log\", rotate=daily, maxparts=14, append=true)"
; - Log to an encrypted file, keeping 14 days worth of logs.
;Connections = "file(filename=\"./tests/logfiles/logfileEncrypted.sil\", encrypt=true, key=""1234567890123456"", rotate=daily, maxparts=14, append=true)"
        
; set defaults for new sessions
; note that session defaults do not apply to the SiAuto.Main session, since
; this session was already added before a configuration file can be loaded. 
; session defaults only apply to newly added sessions and do not affect existing sessions.
SessionDefaults.Active = True
SessionDefaults.Level = Message
SessionDefaults.ColorBG = 0xFFFFFF

; configure some individual session properties.
; note that this does not add the session to the sessionmanager; it simply
; sets the property values IF the session name already exists.
Session.Main.Active = True
Session.Main.ColorBG = 0xFFFFFF
```

</details>

<details>
  <summary>Initialize Logging Support, MAIN module</summary>
  <br/>
  Add the following lines to your program startup module.  
  This will import the necessary package modules, and initialize logging support.  
  NOTE - This code should only be executed one time!  

``` python
# load SmartInspect settings from a configuration settings file.
from smartinspectpython.siauto import *
siConfigPath:str = "./tests/smartinspect.cfg"
SIAuto.Si.LoadConfiguration(siConfigPath)

# start monitoring the configuration file for changes, and reload it when it changes.
# this will check the file for changes every 60 seconds.
siConfig:SIConfigurationTimer = SIConfigurationTimer(SIAuto.Si, siConfigPath, 60)

# get smartinspect logger reference.
_logsi:SISession = SIAuto.Main

# log system environment and application startup parameters.
_logsi.LogSeparator(SILevel.Fatal)
_logsi.LogAppDomain(SILevel.Verbose)
_logsi.LogSystem(SILevel.Verbose)
```

</details>

<details>
  <summary>Initialize Logging Support, CLASS or sub-modules</summary>
  <br/>
  Add the following lines to your program supporting modules.  
  This will import the necessary package modules, and initialize the shared logging session.  

``` python
# get smartinspect logger reference.
from smartinspectpython.siauto import *
_logsi:SISession = SIAuto.Main
```

</details>

<details>
  <summary>More Information on SmartInspect</summary>
  <br/>
  You can use SmartInspectPython by itself to create log files for your own applications.  
  Use the following PIP command to install the SmartInspectPython package from PyPi.org:  

  ``` bash
  $ python3 -m pip install smartinspectpython
  ```

  The SmarrtInspect Redistributable Console Viewer (free) is required to view SmartInspect Log (.sil) formatted log files, as well capture packets via the TcpProtocol or PipeProtocol connections.  The Redistributable Console Viewer can be downloaded from the <a href="https://code-partners.com/offerings/smartinspect/releases/" target="_blank">Code-Partners Software Downloads Page</a>. Note that the "Redistributable Console Viewer" is a free product, while the "SmartInspect Full Setup" is the Professional level viewer that adds a few more bells and whistles for a fee.  Also note that a Console Viewer is NOT required to view plain text (non .sil) formatted log files.
</details>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch  `git checkout -b feature/AmazingFeature`
3. Commit your Changes  `git commit -m 'Add some AmazingFeature'`
4. Push to the Branch  `git push origin feature/AmazingFeature`
5. Open a Pull Request
