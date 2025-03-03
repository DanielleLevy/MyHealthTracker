@echo off
SET DB_NAME=myhealthtracker_sample
SET DB_FILE=myhealthtracker_sample.sql

:: Prompt for MySQL username
set /p DB_USER="Enter MySQL username [default: root]: "
if "%DB_USER%"=="" set DB_USER=root

:: Prompt for MySQL password (note: password hiding is not supported in Windows cmd)
set /p DB_PASSWORD="Enter MySQL password (leave blank if none): "

echo Checking if MySQL is running...
mysqladmin ping -h localhost --silent >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ MySQL is not running! Please start MySQL and try again.
    exit /b 1
)

echo 🛠️ Creating database %DB_NAME% (if not exists)...
mysql -u %DB_USER% -p%DB_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS %DB_NAME%;"

echo 📂 Importing database from %DB_FILE%...
mysql -u %DB_USER% -p%DB_PASSWORD% %DB_NAME% < %DB_FILE%

echo ✅ Database setup completed!

echo 🚀 Starting the backend server...
cd backend || exit /b 1
start /B python auth_api.py
echo ✅ Backend server started.

echo 🛠️ Setting up the frontend...
cd ../my_health_tracker || exit /b 1
npm install
start /B npm start
echo ✅ Frontend server started.

echo 🔄 All servers are running. Press any key to stop...
pause
taskkill /F /IM python.exe
taskkill /F /IM node.exe
