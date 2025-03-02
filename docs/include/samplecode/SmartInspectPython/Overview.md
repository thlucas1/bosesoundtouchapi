# Logging / Tracing Support

The SmartInspectPython package (installed with this package) can be used to easily debug your applications that utilize this API.

The following topics and code samples will get you started on how to enable logging support.  
Note that logging support can be turned on and off without changing code or restarting the application.  
Click on the topics below to expand the section and reveal more information.  

<details>
    <summary>Configure Logging Support Settings File</summary><br/>
    Add the following lines to a new file ("smartinspect.cfg") in your application startup (or test) directory.  
    Note that the file name can be changed to whatever you like (adjust "siConfigPath" in above sample code to match.  

```ini
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
; - Log to a file:
;Connections = "file(filename=\"./tests/logfiles/logfile.log\", rotate=hourly, maxparts=24, append=true)"
; - Log to an encrypted file:
;Connections = "file(filename=\"./tests/logfiles/logfileEncrypted.sil\", encrypt=true, key=""1234567890123456"", rotate=hourly, maxparts=14, append=true)"
        
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
    <summary>Initialize Logging Support, MAIN module</summary><br/>
    Add the following lines to your program startup module.  
    This will import the necessary package modules, and initialize logging support.  
    NOTE - This code should only be executed one time!  

```python
# import smartinspect logging support.
from smartinspectpython.siauto import Level as SILevel, Session as SISession, SiAuto, ConfigurationTimer as SIConfigurationTimer

# load SmartInspect settings from a configuration settings file.
siConfigPath:str = "./tests/smartinspect.cfg"
SiAuto.Si.LoadConfiguration(siConfigPath)

# start monitoring the configuration file for changes, and reload it when it changes.
# this will check the file for changes every 60 seconds.
siConfig:SIConfigurationTimer = SIConfigurationTimer(SiAuto.Si, siConfigPath)

# get smartinspect logger reference.
_logsi:SISession = SiAuto.Main

# log system environment and application startup parameters.
_logsi.LogSeparator(SILevel.Fatal)
_logsi.LogAppDomain(SILevel.Verbose)
_logsi.LogSystem(SILevel.Verbose)
```
</details>

<details>
    <summary>Initialize Logging Support, CLASS or sub-modules</summary><br/>
    Add the following lines to your program supporting modules.  
    This will import the necessary package modules, and initialize the shared logging session.  

```python
# import smartinspect logging support.
from smartinspectpython.siauto import Level as SILevel, Session as SISession, SiAuto

# get smartinspect logger reference.
_logsi:SISession = SiAuto.Main
```
</details>

<details>
    <summary>More Information on SmartInspect</summary><br/>
    You can use SmartInspectPython by itself to create log files for your own applications.  
    Use the following command to install SmartInspectPython suppport from PyPi.org:  
    `pip install smartinspectpython`
    <br/>
    <br/>
    The SmarrtInspect Redistributable Console Viewer (free) is required to view SmartInspect Log (.sil) formatted files, as well capture packets via the TcpProtocol or PipeProtocol connections.  
    The Redistributable Console Viewer can be downloaded from the <a href="https://code-partners.com/offerings/smartinspect/releases/" target="_blank">Code-Partners Software Downloads Page</a>.  
    Note that the "Redistributable Console Viewer" is a free product, while the "SmartInspect Full Setup" is the Professional level viewer that adds a few more bells and whistles for a fee.  
    Also note that a Console Viewer is NOT required to view plain text (non .sil) formatted files.  
</details>
