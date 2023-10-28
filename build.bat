@echo off
cls
echo Script starting.

echo Setting Python Search path (PYTHONPATH).
set PYTHONPATH=C:\Users\thluc\source\repos\BoseSoundTouchApiProject;C:\Users\thluc\source\repos\BoseSoundTouchApiProject\bosesoundtouchapi


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


echo.
echo Building project ...
echo.
python.exe setup.py bdist_wheel


echo Deactivating python virtual environment.  
call ".\env\scripts\deactivate.bat"


echo.
echo Restoring current working directory.
cd C:\Users\thluc\source\repos\BoseSoundTouchApiProject


@echo.
echo Compressing Local GIT Repository.
git gc --auto

echo Uploading dist package to TEST Pypi.org site.
echo Note that this could fail if the version has already been uploaded.
py -m twine upload --repository testpypi ./dist/*%BUILDENV_PACKAGEVERSION%*

echo.
echo Use the following command to upload the dist package to TEST Pypi:
echo ^> py -m twine upload --repository testpypi dist/*%BUILDENV_PACKAGEVERSION%*

echo.
echo Use the following command to install the package from TEST Pypi:
echo ^> pip install -i https://test.pypi.org/simple/ %BUILDENV_PACKAGENAME%

echo.
echo Use the following command to upload the dist package to PROD Pypi:
echo ^> py -m twine upload --repository pypi dist/*%BUILDENV_PACKAGEVERSION%*

echo.
echo Use the following command to install the package from PROD Pypi:
echo ^> pip install %BUILDENV_PACKAGENAME%

echo.
echo Script completed.
pause