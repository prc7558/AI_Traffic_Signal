@echo off
echo ============================================================
echo    Starting Traffic Dashboard with Gunicorn (Production)
echo ============================================================
echo.
echo This runs the dashboard in production mode using Gunicorn
echo Press Ctrl+C to stop
echo.
echo Dashboard will be available at: http://localhost:8000
echo.

cd dashboard
gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 2 --timeout 120 app:app
