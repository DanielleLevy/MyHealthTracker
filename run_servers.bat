@echo off
echo Starting the backend server...

REM Navigate to the backend directory
cd /d "%~dp0backend" || (
    echo Backend directory not found!
    exit /b 1
)

REM Run the backend Python server
start "Backend Server" cmd /c python auth_api.py
set "BACKEND_PID=%ERRORLEVEL%"

echo Backend server is running

REM Navigate to the frontend directory
echo Setting up the frontend...
cd /d "%~dp0my_health_tracker" || (
    echo Frontend directory not found!
    exit /b 1
)

REM Install frontend dependencies
call npm install || (
    echo npm install failed!
    exit /b 1
)

REM Start the frontend server
start "Frontend Server" cmd /c npm start
set "FRONTEND_PID=%ERRORLEVEL%"

echo Frontend server is running

REM Wait for user to press CTRL+C to stop servers
echo Press CTRL+C to stop the servers.

REM Trap CTRL+C to stop both servers
:LOOP
timeout /t 1 >nul
goto LOOP

REM Cleanup on exit
:EXIT
echo Stopping servers...
taskkill /PID %BACKEND_PID% /F
taskkill /PID %FRONTEND_PID% /F

exit /b 0
