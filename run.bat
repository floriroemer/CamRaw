@echo off
REM Run script for Windows

echo Starting CamRaw...

REM Check if dependencies are installed
python -c "import cv2, PIL, numpy" >nul 2>&1
if errorlevel 1 (
    echo Dependencies not found. Running installation...
    call install.bat
)

REM Run the application
python main.py
pause