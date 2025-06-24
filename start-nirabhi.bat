@echo off
title Nirabhi AI Content Moderator - Startup
echo.
echo 🛡️ Starting Nirabhi - AI-Powered Content Moderator
echo ====================================================
echo.

echo 📍 Current directory: %CD%
echo.

echo 🔄 Setting up backend...
cd backend
echo 📦 Installing Python dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
)

pip install -q fastapi uvicorn vaderSentiment pydantic loguru rich python-dotenv
echo ✅ Backend dependencies installed!

echo 🚀 Starting backend server...
start "Nirabhi Backend" cmd /k "title Nirabhi Backend - Port 8000 && venv\Scripts\activate.bat && python main.py"

cd ..\frontend
echo.
echo 🔄 Setting up frontend...
echo 📦 Installing Node dependencies (this may take a moment)...
call npm install --legacy-peer-deps --silent
echo ✅ Frontend dependencies installed!

echo 🚀 Starting frontend server...
start "Nirabhi Frontend" cmd /k "title Nirabhi Frontend - Port 3000 && npm start"

cd ..
echo.
echo ✅ Nirabhi is starting up!
echo.
echo 🌐 Your application will be available at:
echo    💻 Frontend: http://localhost:3000
echo    🔧 Backend:  http://localhost:8000
echo    📚 API Docs: http://localhost:8000/docs
echo.
echo 🎯 Next steps:
echo    1. Wait for both servers to fully start (may take 1-2 minutes)
echo    2. Open http://localhost:3000 in your browser
echo    3. Test the content analyzer with sample text
echo    4. Check DEPLOY.md for hosting instructions
echo.
echo Press any key to open the deployment guide...
pause > nul
start notepad DEPLOY.md
