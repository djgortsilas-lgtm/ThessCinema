@echo off
cd /d "%~dp0server"
set PYTHONIOENCODING=utf-8
echo Starting ThessCinema server...
start /B python -m uvicorn main:app --host 0.0.0.0 --port 8765 >nul 2>&1
timeout /t 3 >nul
start http://localhost:8765
echo Server running at http://localhost:8765
echo Close this window to stop the server.
pause
