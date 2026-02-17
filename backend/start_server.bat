@echo off
REM Start Backend Server Script
REM Run this from the backend directory

echo ========================================
echo Starting Hakhaton TodoApp Backend
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Set PYTHONPATH to include current directory
set PYTHONPATH=.

echo Starting FastAPI server...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
