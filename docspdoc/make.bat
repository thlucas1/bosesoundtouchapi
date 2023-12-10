@echo off
echo Build PDoc Documentation Script starting.


echo Changing working directory to docspdoc folder.
cd C:\Users\thluc\source\repos\BoseSoundTouchApiProject\docspdoc


echo Activating python virtual environment.
call "..\env\scripts\activate.bat"


echo Setting build environment variables via buildEnv.py ...
FOR /F "delims=|" %%G IN ('"python.exe .\buildEnv.py"') DO SET "%%G"
echo.
echo Build Environment variables ...
echo - BUILDENV_PACKAGENAME = %BUILDENV_PACKAGENAME%
echo - BUILDENV_PACKAGEVERSION = %BUILDENV_PACKAGEVERSION%
echo - BUILDENV_PDOC_BRAND_ICON_URL = %BUILDENV_PDOC_BRAND_ICON_URL%
echo - BUILDENV_PDOC_BRAND_ICON_URL_SRC = %BUILDENV_PDOC_BRAND_ICON_URL_SRC%
echo - BUILDENV_PDOC_BRAND_ICON_URL_TITLE = %BUILDENV_PDOC_BRAND_ICON_URL_TITLE%


echo Cleaning up the PDoc Documentation output folder.
del /S /Q .\build\bosesoundtouchapi\*.*
del /S /Q .\build\*.*


echo Copying include files to PDoc output folder.
mkdir .\build\bosesoundtouchapi
copy .\include\*.js .\build
copy .\include\*.ico .\build


echo Changing working directory to package source folder.
cd C:\Users\thluc\source\repos\BoseSoundTouchApiProject\bosesoundtouchapi


echo Building PDoc Documentation ...
rem can also add custom footer text with this option:  --footer-text "This is some footer text" 
echo.
pdoc -o ..\docspdoc\build -d google --no-show-source --no-math --no-mermaid --search -t ..\docspdoc\templates\darkmode __init__ firmware/soundtouchfirmware.py firmware/soundtouchfirmwareproduct.py firmware/soundtouchfirmwarerelease.py models/addstation.py models/audiodspaudiomodes.py models/audiodspcontrols.py models/audioproducttonecontrols.py models/audiospeakerattributeandsetting.py models/balance.py models/bass.py models/basscapabilities.py models/bluetoothinfo.py models/capabilities.py models/clockconfig.py models/clocktime.py models/contentitem.py models/controllevelinfo.py models/dspmonostereoitem.py models/infonetworkconfig.py models/mediaitemcontainer.py models/mediaserver.py models/mediaserverlist.py models/musicserviceaccount.py models/navigate.py models/navigateitem.py models/navigatemenutypes.py models/navigateresponse.py models/networkinfo.py models/networkinfointerface.py models/networkstatus.py models/networkstatusinterface.py models/nowplayingstatus.py models/performwirelesssitesurveyresponse.py models/playinfo.py models/powermanagement.py models/preset.py models/presetlist.py models/productcechdmicontrol.py models/productcechdmimodes.py models/producthdmiassignmentcontrols.py models/rebroadcastlatencymode.py models/recent.py models/recentlist.py models/removestation.py models/search.py models/searchfiltertypes.py models/searchresult.py models/searchsorttypes.py models/searchstation.py models/searchstationartists.py models/searchstationresults.py models/searchstationsongs.py models/searchterm.py models/service.py models/serviceAvailability.py models/simpleconfig.py models/softwareupdatecheckresponse.py models/softwareupdatequeryresponse.py models/soundtouchconfigurationstatus.py models/sourceitem.py models/sourcelist.py models/speakerattributeandsetting.py models/surveyresultitem.py models/systemtimeout.py models/trackinfo.py models/volume.py models/wirelessprofile.py models/zone.py models/zonemember.py uri/soundtouchnodes.py uri/soundtouchuri.py uri/soundtouchuriscopes.py uri/soundtouchuritypes.py ws/soundtouchwebsocket.py bstappmessages.py bstconst.py bstutils.py soundtouchclient.py soundtouchdevice.py soundtouchdevicecomponent.py soundtouchdiscovery.py soundtoucherror.py soundtouchexception.py soundtouchitemtypes.py soundtouchkeys.py soundtouchmessage.py soundtouchmodelrequest.py soundtouchnotifycategorys.py soundtouchsources.py soundtouchwarning.py


echo Deactivating python virtual environment.
call "..\env\scripts\deactivate.bat"


echo.
echo Changing working directory to package project folder.
cd C:\Users\thluc\source\repos\BoseSoundTouchApiProject


echo Build PDoc Documentation Script completed.
