@echo off
REM Automated Setup Script for Traffic Signal AI Project
REM Run this file to automatically set up everything

echo ============================================================
echo    AI-BASED TRAFFIC SIGNAL CONTROLLER
echo    Automated Setup Script
echo ============================================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)
python --version
echo Python found!
echo.

echo [2/5] Creating virtual environment (recommended)...
python -m venv traffic_env
echo Virtual environment created!
echo.

echo [3/5] Activating virtual environment...
call traffic_env\Scripts\activate.bat
echo Virtual environment activated!
echo.

echo [4/5] Installing required packages...
echo This may take 2-5 minutes...
pip install --upgrade pip
pip install -r requirements.txt
echo.

echo [5/5] Testing installation...
cd src
python test_installation.py
cd ..
echo.

echo ============================================================
echo    SETUP COMPLETE!
echo ============================================================
echo.
echo Next Steps:
echo 1. Place a traffic video in the 'videos' folder
echo 2. Connect Arduino and upload 'arduino/traffic_light.ino'
echo 3. Update COM port in src/main.py if needed
echo 4. Run: python src/main.py
echo.
echo For detailed instructions, read: docs/QUICK_START_GUIDE.md
echo.
echo To activate virtual environment later, run:
echo    traffic_env\Scripts\activate.bat
echo.
pause
