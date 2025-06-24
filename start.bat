@echo off
echo 🛡️ Starting Nirabhi - AI-Powered Content Moderator
echo.

echo 🔄 Starting Backend Server...
cd backend
start cmd /k "python main.py"

echo 🔄 Starting Frontend Server...
cd ..\frontend
start cmd /k "npm start"

echo.
echo ✅ Nirabhi is starting up!
echo 📱 Frontend: http://localhost:3000
echo 🖥️ Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul
