#!/bin/bash

# Navigate to the backend directory
echo "Starting the backend server..."
cd backend || { echo "Backend directory not found!"; exit 1; }

# Run the backend Python server
python3 auth_api.py &
BACKEND_PID=$! # Save the backend process ID to terminate it later

echo "Backend server is running (PID: $BACKEND_PID)"

# Navigate to the frontend directory
echo "Setting up the frontend..."
cd ../my_health_tracker || { echo "Frontend directory not found!"; exit 1; }

# Install frontend dependencies
npm install || { echo "npm install failed!"; exit 1; }

# Start the frontend server
npm start &
FRONTEND_PID=$! # Save the frontend process ID to terminate it later

echo "Frontend server is running (PID: $FRONTEND_PID)"

# Wait for the user to press CTRL+C to stop both servers
echo "Press CTRL+C to stop the servers."

# Trap CTRL+C to stop both servers
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" SIGINT

# Keep the script running to allow the servers to continue
while true; do
  sleep 1
done
