@echo off
echo Starting Percepta Pro v2.0...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Install/Update dependencies
echo Installing/Updating dependencies...
pip install -r requirements.txt

REM Set environment variables
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Start the application
echo Starting Percepta Pro...
echo Access the dashboard at http://localhost:8501
streamlit run reputation_dashboard.py

REM Keep window open if there's an error
if %ERRORLEVEL% neq 0 (
    echo.
    echo Error starting Percepta Pro! Check the error message above.
    pause
) 