#!/bin/bash

DB_FILE="myhealthtracker_sample.sql"

# Prompt user for MySQL username, password, database name, and host
read -p "Enter MySQL username [default: root]: " DB_USER
DB_USER=${DB_USER:-root}

read -s -p "Enter MySQL password (press Enter if none): " DB_PASSWORD
echo ""

read -p "Enter MySQL database name [default: myhealthtracker_sample]: " DB_NAME
DB_NAME=${DB_NAME:-myhealthtracker_sample}

read -p "Enter MySQL host [default: localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

# Display the database configurations (excluding password for security)
echo "✅ MySQL Configurations:"
echo "DB_NAME=$DB_NAME"
echo "DB_USER=$DB_USER"
echo "DB_HOST=$DB_HOST"

# Export environment variables so the backend can access them
export DB_NAME
export DB_USER
export DB_PASSWORD
export DB_HOST

# Check if MySQL is running
if ! mysqladmin ping -h "$DB_HOST" --silent; then
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

# Move to backend directory
echo "🐍 Setting up Python environment..."
cd backend || { echo "❌ Backend directory not found!"; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "🔧 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r ../requirements.txt || { echo "❌ Failed to install Python dependencies!"; exit 1; }

# Start the backend server with the user-provided credentials
echo "🚀 Starting the backend server..."
python3 auth_api.py &
BACKEND_PID=$!

echo "✅ Backend server is running (PID: $BACKEND_PID)"

# Navigate to the frontend directory and install dependencies
echo "🛠️ Setting up the frontend..."
cd ../my_health_tracker || { echo "❌ Frontend directory not found!"; exit 1; }
npm install || { echo "❌ npm install failed!"; exit 1; }

# Start the frontend server
npm start &
FRONTEND_PID=$!

echo "✅ Frontend server is running (PID: $FRONTEND_PID)"

# Keep the script running to allow stopping servers with CTRL+C
trap "echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" SIGINT

while true; do
  sleep 1
done
