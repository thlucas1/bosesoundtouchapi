@echo off
cls
echo Script starting.

echo Setting Python Search path (PYTHONPATH).
set PYTHONPATH=C:\Users\thluc\source\repos\BoseSoundTouchApiProject;C:\Users\thluc\source\repos\BoseSoundTouchApiProject\bosesoundtouchapi
set PDOC_DISPLAY_ENV_VARS=1


echo Changing working directory to package source folder.
cd C:\Users\thluc\source\repos\BoseSoundTouchApiProject


echo Activating python virtual environment.
call ".\env\scripts\activate.bat"


echo Cleaning up the project build output folder.
del /Q /S .\build\*.* >nul


echo Setting build environment variables via buildEnv.py ...
FOR /F "delims=|" %%G IN ('"python.exe .\docspdoc\buildEnv.py"') DO SET "%%G"
echo.
echo Build Environment variables:
echo - BUILDENV_PACKAGENAME = %BUILDENV_PACKAGENAME%
echo - BUILDENV_PACKAGEVERSION = %BUILDENV_PACKAGEVERSION%
echo - BUILDENV_PDOC_BRAND_ICON_URL = %BUILDENV_PDOC_BRAND_ICON_URL%
echo - BUILDENV_PDOC_BRAND_ICON_URL_SRC = %BUILDENV_PDOC_BRAND_ICON_URL_SRC%
echo - BUILDENV_PDOC_BRAND_ICON_URL_TITLE = %BUILDENV_PDOC_BRAND_ICON_URL_TITLE%


echo Building project documentation ...
echo.
call ".\docspdoc\make.bat"


echo Deactivating python virtual environment.
call ".\env\scripts\deactivate.bat"


echo.
echo Script completed.
pause