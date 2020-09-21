@echo off
pathman add %CD%
set /p commandname="Enter command name you want (no spaces, no special characters): "
python3 -m pip install requirements.txt
echo python3 %CD% >> %commandname%.bat
del pathman.exe
echo "finished installing StreamDownloader."
echo "You can now run it using these options:"
echo.
echo "1. Hit: Windows Key+R, then type in %commandname% and hit Enter."
echo.
echo "2. Open Command prompt (in the application finder, type 'cmd'), and then type in %commandname%"
echo.
echo "Thank you for using my software."
pause > nul
exit
