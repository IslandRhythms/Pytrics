@echo off
REM Setup script: Create virtual environment and install dependencies
echo Setting up Pytrics Unit Converter...
echo.

REM Check if virtual environment exists
if exist env (
    echo Virtual environment already exists.
) else (
    echo Creating virtual environment...
    python -m venv env
    if errorlevel 1 (
        echo Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

REM Activate virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo Setup complete!
echo.
echo To run the application:
echo   1. Activate the environment: activate.bat
echo   2. Run: python src\main.py
echo.
echo Or simply double-click run.bat
echo.
pause

