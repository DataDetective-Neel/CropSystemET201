@echo off
REM Windows batch file to run the mobile app
REM Double-click this file or run: mobile_app\run_mobile_app.bat

cd /d %~dp0
python run_mobile_app.py

if errorlevel 1 (
    echo.
    echo Error: Python not found or script failed
    echo Make sure Python is installed and in your PATH
    pause
)

