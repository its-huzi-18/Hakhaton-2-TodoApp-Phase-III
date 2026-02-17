@echo off
REM Quick Start Script for Hakhaton TodoApp Phase III
REM Run this script to start both backend and frontend servers

echo ========================================
echo Hakhaton TodoApp Phase III - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/4] Checking environment files...
if not exist "backend\.env" (
    echo WARNING: backend\.env not found. Copying from backend\.env.example
    copy "backend\.env.example" "backend\.env"
    echo Please edit backend\.env with your credentials before continuing!
    echo Press any key to continue after editing...
    pause
)

if not exist "frontend\.env.local" (
    echo WARNING: frontend\.env.local not found. Copying from frontend\.env.local.example
    copy "frontend\.env.local.example" "frontend\.env.local"
)

echo.
echo [2/4] Starting Backend Server...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt -q

REM Start backend in background
echo Starting FastAPI server on http://localhost:8000
start "Backend Server" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

cd ..

echo.
echo [3/4] Starting Frontend Server...
cd frontend

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

REM Start frontend in background
echo Starting Next.js dev server on http://localhost:3000
start "Frontend Server" cmd /k "npm run dev"

cd ..

echo.
echo [4/4] Startup Complete!
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend:     http://localhost:3000
echo.
echo IMPORTANT: Make sure to configure your environment files!
echo   - backend\.env (especially OPENAI_API_KEY and DATABASE_URL)
echo   - frontend\.env.local
echo.
echo Press any key to open the application in your browser...
pause >nul
start http://localhost:3000

echo.
echo To stop the servers:
echo   1. Close the "Backend Server" and "Frontend Server" windows
echo   2. Or press Ctrl+C in each window
echo.
