@echo off
echo ============================================================
echo    Dynamic Traffic Signal AI - Quick Launcher
echo ============================================================
echo.
echo Choose an option:
echo.
echo [1] Dashboard Only (No Arduino)
echo [2] Arduino Controller Only
echo [3] Full System (Arduino + Dashboard)
echo [4] Test Synchronization
echo [5] Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto dashboard
if "%choice%"=="2" goto arduino
if "%choice%"=="3" goto fullsystem
if "%choice%"=="4" goto test
if "%choice%"=="5" goto end

:dashboard
echo.
echo Starting Dashboard Only...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop
echo.
cd dashboard
python app.py
goto end

:arduino
echo.
echo Starting Arduino Controller...
echo Make sure Arduino is connected!
echo Press Ctrl+C to stop
echo.
cd src
python main.py
goto end

:fullsystem
echo.
echo Starting Full System...
echo.
echo This will open 2 windows:
echo   1. Arduino Controller
echo   2. Web Dashboard
echo.
echo Then open your browser to: http://localhost:5000
echo.
pause
start cmd /k "cd src && python main.py"
timeout /t 2 /nobreak >nul
start cmd /k "cd dashboard && python app.py"
echo.
echo Both systems started!
echo Check the new windows that opened.
goto end

:test
echo.
echo Running synchronization test...
echo.
python test_sync.py
echo.
pause
goto end

:end
echo.
echo Goodbye!
pause
