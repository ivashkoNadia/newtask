@echo off
setlocal enabledelayedexpansion

if not exist venv (
    echo venv not found 
    pause
    exit /b 1
)

call venv\Scripts\activate

set n=3  :: Set 'n' to the number of iterations you want
set logFile=command_log.txt

:: Clear the log file
type nul > "%logFile%"

:: Start the server in the same cmd window
start "Server" cmd /k "runserver.py --port=80"
echo runserver.py --port=80 >> "%logFile%"

:: Loop through and start the nodes in separate cmd windows
for /l %%i in (1, 1, %n%) do (
    set /a port=8080+%%i
    start "Node%%i" cmd /k "runnode.py --proxy=192.168.1.8 --port=!port! --local"
    echo runnode.py --proxy=192.168.1.8 --port=!port! --local >> "%logFile%"
)