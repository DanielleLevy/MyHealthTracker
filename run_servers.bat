@echo off
SET DB_FILE=myhealthtracker_sample.sql

:: Prompt for MySQL username, password, database name, and host
set /p DB_USER="Enter MySQL username [default: root]: "
if "%DB_USER%"=="" set DB_USER=root

set /p DB_PASSWORD="Enter MySQL password (leave blank if none): "

set /p DB_NAME="Enter MySQL database name [default: myhealthtracker_sample]: "
if "%DB_NAME%"=="" set DB_NAME=myhealthtracker_sample

set /p DB_HOST="Enter MySQL host [default: localhost]: "
if "%DB_HOST%"=="" set DB_HOST=localhost

:: Display the database configurations (excluding password for security)
echo ✅ MySQL Configurations:
echo DB_NAME=%DB_NAME%
echo DB_USER=%DB_USER%
echo DB_HOST=%DB_HOST%

:: Set environment variables so the backend can access them
setx DB_NAME "%DB_NAME%"
setx DB_USER "%DB_USER%"
setx DB_PASSWORD "%DB_PASSWORD%"
setx DB_HOST "%DB_HOST%"

:: Check if MySQL is running
mysqladmin ping -h "%DB_HOST%" --silent >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ MySQL is not running! Please start MySQL and try again.
    exit /b 1
)

:: Create database if it does not exist
echo 🛠️ Creating database %DB_NAME% (if not exists)...
mysql -u %DB_USER% -p%DB_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS %DB_NAME%;"

:: Import the database dump
echo 📂 Importing database from %DB_FILE%...
mysql -u %DB_USER% -p%DB_PASSWORD% %DB_NAME% < %DB_FILE%

echo ✅ Database setup completed!

:: Move to backend directory
cd backend || exit /b 1

:: Check if virtual environment exists, if not, create it
if not exist venv (
    echo 🔧 Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r ..\requirements.txt || (
    echo ❌ Failed to install Python dependencies!
    exit /b 1
)

:: Start the backend server with the user-provided credentials
echo 🚀 Starting the backend server...
start /B python auth_api.py
echo ✅ Backend server started.

:: Navigate to the frontend directory and install dependencies
cd ../my_health_tracker || exit /b 1
npm install
start /B npm start
echo ✅ Frontend server started.

echo 🔄 All servers are running. Press any key to stop...
pause
taskkill /F /IM python.exe
taskkill /F /IM node.exe
