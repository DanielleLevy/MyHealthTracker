#!/bin/bash

DB_NAME="myhealthtracker_sample"
DB_FILE="myhealthtracker_sample.sql"

# Prompt user for MySQL username and password
read -p "Enter MySQL username [default: root]: " DB_USER
DB_USER=${DB_USER:-root}

read -s -p "Enter MySQL password (press Enter if none): " DB_PASSWORD
echo ""

# Check if MySQL is running
if ! mysqladmin ping -h "localhost" --silent; then
  echo "❌ MySQL is not running! Please start MySQL and try again."
  exit 1
fi

# Create database if it does not exist
echo "🛠️ Creating database: $DB_NAME (if not exists)..."
mysql -u "$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

# Import the database dump
echo "📂 Importing database from $DB_FILE..."
mysql -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$DB_FILE"

echo "✅ Database setup completed!"

# Start the backend server
echo "🚀 Starting the backend server..."
cd backend || { echo "❌ Backend directory not found!"; exit 1; }
python3 auth_api.py &
BACKEND_PID=$!

echo "✅ Backend server is running (PID: $BACKEND_PID)"

# Navigate to the frontend directory and start the server
echo "🛠️ Setting up the frontend..."
cd ../my_health_tracker || { echo "❌ Frontend directory not found!"; exit 1; }
npm install || { echo "❌ npm install failed!"; exit 1; }
npm start &
FRONTEND_PID=$!

echo "✅ Frontend server is running (PID: $FRONTEND_PID)"

# Keep the script running to allow stopping servers with CTRL+C
trap "echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" SIGINT

while true; do
  sleep 1
done
