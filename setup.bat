@echo off
echo ===================================================
echo   Passport Photo Pro - One-Click Setup
echo ===================================================

echo.
echo [1/3] Checking for Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in your PATH. Please install Python 3.8 or higher.
    pause
    exit /b
)

echo.
echo [2/3] Creating virtual environment...
IF NOT EXIST "venv" (
    python -m venv venv
    echo Virtual environment created.
) ELSE (
    echo Virtual environment already exists.
)

echo.
echo [3/3] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo ===================================================
echo   Setup Complete!
echo   You can now double-click "run.bat" to start the app.
echo ===================================================
pause
