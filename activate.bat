@echo off
REM Activate virtual environment and provide instructions
if exist env\Scripts\activate.bat (
    call env\Scripts\activate.bat
    echo Virtual environment activated!
    echo.
    echo To install dependencies, run: pip install -r requirements.txt
    echo To run the application, run: python src\main.py
    echo To deactivate, run: deactivate
) else (
    echo Virtual environment not found!
    echo Please create it first with: python -m venv env
)

