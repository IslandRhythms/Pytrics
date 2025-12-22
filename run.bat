@echo off
REM Activate virtual environment and run the application
if exist env\Scripts\activate.bat (
    call env\Scripts\activate.bat
    echo Running Pytrics Unit Converter...
    echo.
    python src\main.py
) else (
    echo Virtual environment not found!
    echo Please create it first with: python -m venv env
    echo Then activate it and install dependencies: pip install -r requirements.txt
    pause
)

