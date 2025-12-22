# Pytrics
Metric and Imperial Unit converter GUI

## Setup

### Prerequisites
- Python 3.8 or higher

### Installation

1. **Create a virtual environment** (if you haven't already):
   ```bash
   python -m venv env
   ```

2. **Activate the virtual environment**:
   
   **Windows (Command Prompt):**
   ```cmd
   env\Scripts\activate
   ```
   
   **Windows (PowerShell):**
   ```powershell
   env\Scripts\Activate.ps1
   ```
   
   **Windows (Git Bash):**
   ```bash
   source env/Scripts/activate
   ```
   
   **Or use the provided script:**
   - Double-click `activate.bat` (Command Prompt)
   - Run `.\activate.ps1` (PowerShell)

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Quick Setup (Windows)

For a one-time setup, you can use the provided setup script:
- Double-click `setup.bat` - This will create the virtual environment and install all dependencies automatically.

## Running the Application

### Method 1: Using the run script (Windows)
- Double-click `run.bat` - This will activate the environment and run the application.

### Method 2: Manual run
1. Activate the virtual environment (see above)
2. Run the application:
   ```bash
   python src\main.py
   ```

## Features

- **Length conversions**: meters, kilometers, miles, feet, inches, yards, centimeters, millimeters
- **Weight conversions**: kilograms, grams, pounds, ounces, tons, metric tons
- **Temperature conversions**: Celsius, Fahrenheit, Kelvin
- **Volume conversions**: liters, milliliters, gallons, quarts, pints, cups, fluid ounces

## Project Structure

```
Pytrics/
├── src/
│   ├── main.py          # Main application GUI
│   └── converter.py     # Unit conversion logic
├── requirements.txt     # Python dependencies
├── setup.bat           # Automated setup script (Windows)
├── activate.bat        # Activation helper (Windows)
├── activate.ps1        # Activation helper (PowerShell)
└── run.bat             # Quick run script (Windows)
```
