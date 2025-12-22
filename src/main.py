"""Main application entry point for Pytrics unit converter."""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from converter import (
    UnitConverter, UnitCategory, LengthUnit, WeightUnit,
    TemperatureUnit, VolumeUnit
)


class UnitConverterApp(QMainWindow):
    """Main window for the unit converter application."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pytrics - Unit Converter")
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Category selection
        category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.addItems([cat.value for cat in UnitCategory])
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        
        category_layout = QHBoxLayout()
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        
        # Input section
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter value")
        self.input_field.textChanged.connect(self.on_input_changed)
        self.from_unit_combo = QComboBox()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(QLabel("from"))
        input_layout.addWidget(self.from_unit_combo)
        layout.addLayout(input_layout)
        
        # Output section
        output_layout = QHBoxLayout()
        self.output_field = QLineEdit()
        self.output_field.setReadOnly(True)
        self.output_field.setPlaceholderText("Result will appear here")
        self.to_unit_combo = QComboBox()
        output_layout.addWidget(self.output_field)
        output_layout.addWidget(QLabel("to"))
        output_layout.addWidget(self.to_unit_combo)
        layout.addLayout(output_layout)
        
        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert)
        layout.addWidget(self.convert_button)
        
        # Initialize with default category
        self.current_category = UnitCategory.LENGTH
        self.update_unit_combos()
        
        # Connect unit combo changes
        self.from_unit_combo.currentTextChanged.connect(self.on_input_changed)
        self.to_unit_combo.currentTextChanged.connect(self.on_input_changed)
    
    def on_category_changed(self, category_name: str):
        """Handle category selection change."""
        self.current_category = UnitCategory(category_name)
        self.update_unit_combos()
        self.input_field.clear()
        self.output_field.clear()
    
    def update_unit_combos(self):
        """Update unit combo boxes based on current category."""
        self.from_unit_combo.clear()
        self.to_unit_combo.clear()
        
        if self.current_category == UnitCategory.LENGTH:
            units = [unit.value for unit in LengthUnit]
        elif self.current_category == UnitCategory.WEIGHT:
            units = [unit.value for unit in WeightUnit]
        elif self.current_category == UnitCategory.TEMPERATURE:
            units = [unit.value for unit in TemperatureUnit]
        elif self.current_category == UnitCategory.VOLUME:
            units = [unit.value for unit in VolumeUnit]
        else:
            units = []
        
        self.from_unit_combo.addItems(units)
        self.to_unit_combo.addItems(units)
    
    def on_input_changed(self):
        """Handle input field or unit changes - clear output."""
        self.output_field.clear()
    
    def convert(self):
        """Perform the unit conversion."""
        try:
            # Get input value
            input_text = self.input_field.text().strip()
            if not input_text:
                self.output_field.clear()
                return
            
            value = float(input_text)
            
            # Get selected units
            from_unit_str = self.from_unit_combo.currentText()
            to_unit_str = self.to_unit_combo.currentText()
            
            if not from_unit_str or not to_unit_str:
                return
            
            # Perform conversion based on category
            if self.current_category == UnitCategory.LENGTH:
                from_unit = LengthUnit(from_unit_str)
                to_unit = LengthUnit(to_unit_str)
                result = UnitConverter.convert_length(value, from_unit, to_unit)
            elif self.current_category == UnitCategory.WEIGHT:
                from_unit = WeightUnit(from_unit_str)
                to_unit = WeightUnit(to_unit_str)
                result = UnitConverter.convert_weight(value, from_unit, to_unit)
            elif self.current_category == UnitCategory.TEMPERATURE:
                from_unit = TemperatureUnit(from_unit_str)
                to_unit = TemperatureUnit(to_unit_str)
                result = UnitConverter.convert_temperature(value, from_unit, to_unit)
            elif self.current_category == UnitCategory.VOLUME:
                from_unit = VolumeUnit(from_unit_str)
                to_unit = VolumeUnit(to_unit_str)
                result = UnitConverter.convert_volume(value, from_unit, to_unit)
            else:
                return
            
            # Display result
            self.output_field.setText(f"{result:.6f}".rstrip('0').rstrip('.'))
            
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    
    window = UnitConverterApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

