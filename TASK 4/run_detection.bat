@echo off
echo Starting Object Detection and Tracking System...
echo.
echo Step 1: Setting up dependencies...
python setup.py
echo.
echo Step 2: Choose your interface:
echo.
echo Option 1: Command Line Interface (CLI)
echo - Press 1 to run CLI with webcam
echo - Press 2 to run CLI with video file
echo.
echo Option 2: Web Interface
echo - Press 3 to run web interface
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting CLI with webcam...
    python object_detection_tracking.py --source 0
) else if "%choice%"=="2" (
    echo.
    set /p video="Enter video file path: "
    echo Starting CLI with video file...
    python object_detection_tracking.py --source "%video%"
) else if "%choice%"=="3" (
    echo.
    echo Starting web interface...
    echo Server will be available at: http://localhost:5020
    echo.
    python web_interface.py
) else (
    echo Invalid choice. Please run the script again.
) 