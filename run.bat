@echo off
echo ===================================================
echo   Starting Passport Photo Pro...
echo ===================================================

IF NOT EXIST "venv" (
    echo Error: Virtual environment not found!
    echo Please double-click "setup.bat" first to install the application.
    pause
    exit /b
)

call venv\Scripts\activate.bat
start http://127.0.0.1:5000
python app.py

pause
