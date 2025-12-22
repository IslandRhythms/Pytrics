# PowerShell script to activate virtual environment
if (Test-Path "env\Scripts\Activate.ps1") {
    & "env\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To install dependencies, run: pip install -r requirements.txt"
    Write-Host "To run the application, run: python src\main.py"
    Write-Host "To deactivate, run: deactivate"
} else {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create it first with: python -m venv env"
}

