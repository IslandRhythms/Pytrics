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

- **Multiple Unit Categories**: Convert between units in four categories - length (meters, kilometers, miles, feet, inches, yards, centimeters, millimeters), weight (kilograms, grams, pounds, ounces, tons, metric tons), temperature (Celsius, Fahrenheit, Kelvin), and volume (liters, milliliters, gallons, quarts, pints, cups, fluid ounces). All conversions are handled with precision and support both large and small numbers using scientific notation.

- **Dark/Light Mode**: Toggle between dark and light themes with a single click. The theme button is prominently displayed in the title bar for easy access.

- **Custom Themes**: Create and load your own color palette from a JSON file. Define five main colors (primary, secondary, neutral, accent, and status) to personalize the application's appearance to match your preferences.

- **Conversion History**: Automatically track all your conversions with timestamps. Each entry shows the input value, source unit, converted value, target unit, and optional label. History persists during your session and can be exported to CSV or TXT files.

- **Labeled Conversions**: Add optional labels to your conversions for better organization. This makes it easy to identify and reference specific conversions later in your history.

- **Export History**: Export your conversion history to CSV or TXT format for external use, documentation, or record-keeping purposes.

## Custom Themes

You can create your own custom theme by creating a JSON file with five color values:

```json
{
  "primary": "#667eea",
  "secondary": "#764ba2",
  "neutral": "#4a5568",
  "accent": "#48bb78",
  "status": "#ffffff"
}
```

**Color Definitions:**
- **primary**: Main background gradient color (top)
- **secondary**: Secondary background gradient color (bottom)
- **neutral**: Neutral color for borders and text
- **accent**: Accent color for buttons and highlights
- **status**: Status/text color for labels

To load a custom theme:
1. Go to **Theme → Load Custom Theme...** in the menu bar
2. Select your JSON theme file
3. The theme will be applied immediately

To reset to default: **Theme → Reset to Default**

See `example_theme.json` for a template.

## Project Structure

```
Pytrics/
├── src/
│   ├── main.py          # Main application GUI
│   ├── converter.py     # Unit conversion logic
│   └── theme.py         # Theme management
├── example_theme.json   # Example custom theme file
├── requirements.txt     # Python dependencies
├── setup.bat           # Automated setup script (Windows)
├── activate.bat        # Activation helper (Windows)
├── activate.ps1        # Activation helper (PowerShell)
└── run.bat             # Quick run script (Windows)
```
