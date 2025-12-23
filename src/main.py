"""Main application entry point for Pytrics unit converter."""

import sys
import re
import os
import tempfile
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QComboBox, QPushButton, QLabel, QMessageBox, QListWidget,
    QListWidgetItem, QSplitter, QFileDialog, QMenuBar, QMenu
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPainter, QColor, QPixmap
from converter import (
    UnitConverter, UnitCategory, LengthUnit, WeightUnit,
    TemperatureUnit, VolumeUnit
)
from theme import ThemeManager


class UnitConverterApp(QMainWindow):
    """Main window for the unit converter application."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pytrics - Unit Converter")
        self.setMinimumWidth(950)
        self.setMinimumHeight(800)
        
        # Theme state
        self.dark_mode = True
        self.custom_theme_path = None
        
        # Conversion history
        self.conversion_history = []
        
        # Create menu bar
        menubar = self.menuBar()
        theme_menu = menubar.addMenu("Theme")
        
        load_theme_action = theme_menu.addAction("🎨 Load Custom Theme...")
        load_theme_action.triggered.connect(self.load_custom_theme_dialog)
        
        reset_theme_action = theme_menu.addAction("Reset to Default")
        reset_theme_action.triggered.connect(self.reset_theme)
        
        # History menu
        history_menu = menubar.addMenu("History")
        export_history_action = history_menu.addAction("💾 Export History...")
        export_history_action.triggered.connect(self.export_history)
        
        # Create a wrapper widget with explicit background to override system dark mode
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)
        
        # Create splitter for main layout
        splitter = QSplitter(Qt.Horizontal)
        wrapper_layout.addWidget(splitter)
        self.setCentralWidget(wrapper)
        
        # Left side - Converter
        converter_widget = QWidget()
        converter_layout = QVBoxLayout(converter_widget)
        converter_layout.setSpacing(20)
        converter_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title and theme controls
        title_layout = QHBoxLayout()
        title = QLabel("Pytrics Unit Converter")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignLeft)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        # Theme toggle button - make it more prominent
        self.theme_button = QPushButton("🌙 Dark Mode")
        self.theme_button.setMinimumWidth(160)
        self.theme_button.setMinimumHeight(40)
        theme_button_font = QFont()
        theme_button_font.setPointSize(12)
        theme_button_font.setBold(True)
        self.theme_button.setFont(theme_button_font)
        self.theme_button.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: #ffffff;
                border: 2px solid #ffffff;
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5568d3;
                border: 2px solid #ffffff;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #4c63d2;
            }
        """)
        self.theme_button.clicked.connect(self.toggle_theme)
        title_layout.addWidget(self.theme_button)
        converter_layout.addLayout(title_layout)
        
        converter_layout.addSpacing(10)
        
        # Use consistent label width for column alignment
        label_width = 140
        
        # Category selection (first)
        category_label = QLabel("Category:")
        category_label.setMinimumWidth(label_width)
        category_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.category_combo = QComboBox()
        self.category_combo.addItems([cat.value for cat in UnitCategory])
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        self.category_combo.setMinimumHeight(40)
        
        category_layout = QHBoxLayout()
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo, 2)  # Same stretch factor as input fields
        converter_layout.addLayout(category_layout)
        
        converter_layout.addSpacing(15)
        
        # Label section (second)
        label_label = QLabel("Label (optional):")
        label_label.setMinimumWidth(label_width)
        label_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_field = QLineEdit()
        self.label_field.setPlaceholderText("Add a label for this conversion (e.g., Width, Height)")
        self.label_field.setMinimumHeight(40)
        label_font = QFont()
        label_font.setPointSize(13)
        self.label_field.setFont(label_font)
        
        label_layout = QHBoxLayout()
        label_layout.addWidget(label_label)
        label_layout.addWidget(self.label_field, 2)  # Same stretch factor as other input fields
        converter_layout.addLayout(label_layout)
        
        converter_layout.addSpacing(25)
        
        # Input section (third - text area for large numbers)
        input_label = QLabel("From:")
        input_label.setMinimumWidth(label_width)
        input_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_label)
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Enter value")
        self.input_field.setMinimumHeight(100)
        self.input_field.setMaximumHeight(300)
        input_font = QFont()
        input_font.setPointSize(14)
        self.input_field.setFont(input_font)
        self.input_field.textChanged.connect(self.on_input_changed)
        self.from_unit_combo = QComboBox()
        self.from_unit_combo.setMinimumHeight(100)
        from_unit_font = QFont()
        from_unit_font.setPointSize(13)
        self.from_unit_combo.setFont(from_unit_font)
        input_layout.addWidget(self.input_field, 2)
        input_layout.addWidget(self.from_unit_combo, 1)
        converter_layout.addLayout(input_layout)
        
        converter_layout.addSpacing(30)
        
        # Output section (fourth - LARGE text area - the focus!)
        output_label = QLabel("Result:")
        output_label.setMinimumWidth(label_width)
        output_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        output_layout = QHBoxLayout()
        output_layout.addWidget(output_label)
        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        self.output_field.setPlaceholderText("Conversion result will appear here")
        # Make output field same size as input field
        self.output_field.setMinimumHeight(100)
        self.output_field.setMaximumHeight(300)
        output_font = QFont()
        output_font.setPointSize(20)
        output_font.setBold(True)
        self.output_field.setFont(output_font)
        self.to_unit_combo = QComboBox()
        self.to_unit_combo.setMinimumHeight(100)
        to_unit_font = QFont()
        to_unit_font.setPointSize(16)
        self.to_unit_combo.setFont(to_unit_font)
        output_layout.addWidget(self.output_field, 2)
        output_layout.addWidget(self.to_unit_combo, 1)
        converter_layout.addLayout(output_layout)
        
        converter_layout.addSpacing(20)
        
        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert)
        self.convert_button.setMinimumHeight(50)
        converter_layout.addWidget(self.convert_button)
        
        converter_layout.addStretch()
        
        # Right side - History
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.setContentsMargins(20, 20, 20, 20)
        history_layout.setSpacing(10)
        
        history_header_layout = QHBoxLayout()
        history_title = QLabel("Conversion History")
        history_title_font = QFont()
        history_title_font.setPointSize(18)
        history_title_font.setBold(True)
        history_title.setFont(history_title_font)
        history_header_layout.addWidget(history_title)
        history_header_layout.addStretch()
        
        self.clear_history_button = QPushButton("Clear")
        self.clear_history_button.setMinimumWidth(70)
        self.clear_history_button.clicked.connect(self.clear_history)
        history_header_layout.addWidget(self.clear_history_button)
        history_layout.addLayout(history_header_layout)
        
        self.history_list = QListWidget()
        self.history_list.setAlternatingRowColors(True)
        # Enable word wrap and set minimum height for items to handle large numbers
        self.history_list.setWordWrap(True)
        self.history_list.setSpacing(2)
        history_layout.addWidget(self.history_list)
        
        # Add widgets to splitter
        splitter.addWidget(converter_widget)
        splitter.addWidget(history_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([600, 300])
        
        # Initialize with default category
        self.current_category = UnitCategory.LENGTH
        self.update_unit_combos()
        
        # Connect unit combo changes
        self.from_unit_combo.currentTextChanged.connect(self.on_input_changed)
        self.to_unit_combo.currentTextChanged.connect(self.on_input_changed)
        
        # Create arrow icons for combo boxes
        self.create_arrow_icons()
        
        # Apply theme after all widgets are created
        self.apply_theme()
    
    def create_arrow_icons(self):
        """Create simple arrow icons for combo boxes and save to temp file."""
        # Create a simple down arrow pixmap
        arrow_size = 12
        pixmap = QPixmap(arrow_size, arrow_size)
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        
        # Get neutral color from current theme
        if self.dark_mode:
            arrow_color = QColor(74, 85, 104)  # #4a5568
        else:
            arrow_color = QColor(45, 55, 72)  # #2d3748
        
        painter.setBrush(arrow_color)
        
        # Draw triangle pointing down
        from PySide6.QtGui import QPolygon
        from PySide6.QtCore import QPoint
        points = [
            QPoint(arrow_size // 2, arrow_size - 2),  # Bottom point
            QPoint(2, 4),  # Top left
            QPoint(arrow_size - 2, 4)  # Top right
        ]
        polygon = QPolygon(points)
        painter.drawPolygon(polygon)
        painter.end()
        
        # Save to temporary file
        temp_dir = tempfile.gettempdir()
        arrow_file = os.path.join(temp_dir, "pytrics_arrow.png")
        pixmap.save(arrow_file, "PNG")
        
        # Convert Windows path to forward slashes for stylesheet
        arrow_path = arrow_file.replace("\\", "/")
        
        # Apply to all combo boxes
        arrow_style = f"""
            QComboBox::down-arrow {{
                image: url({arrow_path});
                width: {arrow_size}px;
                height: {arrow_size}px;
            }}
        """
        self.category_combo.setStyleSheet(arrow_style)
        self.from_unit_combo.setStyleSheet(arrow_style)
        self.to_unit_combo.setStyleSheet(arrow_style)
        
        # Store arrow file path for cleanup if needed
        self.arrow_file_path = arrow_file
    
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
    
    def apply_theme(self):
        """Apply the current theme (dark, light, or custom)."""
        stylesheet, output_style = ThemeManager.get_stylesheet(
            self.dark_mode, 
            self.custom_theme_path
        )
        
        if hasattr(self, 'output_field'):
            self.output_field.setStyleSheet(output_style)
        
        # Get the primary and secondary colors for the wrapper widget
        if self.custom_theme_path:
            custom_colors = ThemeManager.load_custom_theme(self.custom_theme_path)
            if custom_colors:
                primary = custom_colors.get('primary', '#667eea')
                secondary = custom_colors.get('secondary', '#764ba2')
            else:
                # Use dark mode colors if no custom theme
                if self.dark_mode:
                    primary = '#1a202c'  # Dark mode primary
                    secondary = '#2d3748'  # Dark mode secondary
                else:
                    primary = '#ffffff'  # Light mode primary
                    secondary = '#f7fafc'  # Light mode secondary
        else:
            # Use dark mode colors if no custom theme
            if self.dark_mode:
                primary = '#1a202c'  # Dark mode primary
                secondary = '#2d3748'  # Dark mode secondary
            else:
                primary = '#ffffff'  # Light mode primary
                secondary = '#f7fafc'  # Light mode secondary
        
        # Apply stylesheet to main window
        self.setStyleSheet(stylesheet)
        
        # Force background on wrapper widget to override system dark mode
        # This ensures the background is visible even when Windows dark mode is active
        if hasattr(self, 'centralWidget') and self.centralWidget():
            wrapper_style = f"""
                QWidget#wrapper {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {primary}, stop:1 {secondary});
                }}
            """
            # Set object name so the style applies only to the wrapper
            self.centralWidget().setObjectName("wrapper")
            self.centralWidget().setStyleSheet(wrapper_style)
        
        # Recreate arrow icons to match new theme
        if hasattr(self, 'category_combo'):
            self.create_arrow_icons()
        
        # Update theme button style to match current mode
        if hasattr(self, 'theme_button'):
            if self.dark_mode:
                self.theme_button.setText("🌙 Dark Mode")
                self.theme_button.setStyleSheet("""
                    QPushButton {
                        background-color: #667eea;
                        color: #ffffff;
                        border: 2px solid #ffffff;
                        border-radius: 10px;
                        padding: 8px 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #5568d3;
                        border: 2px solid #ffffff;
                    }
                    QPushButton:pressed {
                        background-color: #4c63d2;
                    }
                """)
            else:
                self.theme_button.setText("☀️ Light Mode")
                self.theme_button.setStyleSheet("""
                    QPushButton {
                        background-color: #f59e0b;
                        color: #ffffff;
                        border: 2px solid #ffffff;
                        border-radius: 10px;
                        padding: 8px 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #d97706;
                        border: 2px solid #ffffff;
                    }
                    QPushButton:pressed {
                        background-color: #b45309;
                    }
                """)
    
    def load_custom_theme(self, file_path: str) -> bool:
        """Load a custom theme from a file.
        
        Returns:
            True if theme loaded successfully, False otherwise
        """
        theme_data = ThemeManager.load_custom_theme(file_path)
        if theme_data:
            # Validate colors can be used (this will raise ValueError if invalid)
            try:
                # Test if colors can be processed
                ThemeManager.get_custom_stylesheet(theme_data, is_dark=self.dark_mode)
                self.custom_theme_path = file_path
                self.apply_theme()
                return True
            except ValueError:
                # Color format error - re-raise to be caught by dialog
                raise
        return False
    
    def toggle_theme(self):
        """Toggle between dark and light mode."""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.theme_button.setText("🌙 Dark Mode")
            self.theme_button.setStyleSheet("""
                QPushButton {
                    background-color: #667eea;
                    color: #ffffff;
                    border: 2px solid #ffffff;
                    border-radius: 10px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5568d3;
                    border: 2px solid #ffffff;
                }
                QPushButton:pressed {
                    background-color: #4c63d2;
                }
            """)
        else:
            self.theme_button.setText("☀️ Light Mode")
            self.theme_button.setStyleSheet("""
                QPushButton {
                    background-color: #f59e0b;
                    color: #ffffff;
                    border: 2px solid #ffffff;
                    border-radius: 10px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d97706;
                    border: 2px solid #ffffff;
                }
                QPushButton:pressed {
                    background-color: #b45309;
                }
            """)
        self.apply_theme()
    
    def load_custom_theme_dialog(self):
        """Open a file dialog to load a custom theme."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Custom Theme",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                if self.load_custom_theme(file_path):
                    QMessageBox.information(
                        self,
                        "Theme Loaded",
                        f"Custom theme loaded successfully from:\n{file_path}"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Invalid Theme",
                        "Failed to load theme. Please check:\n\n"
                        "1. File contains all required colors:\n"
                        "   - primary, secondary, neutral, accent, status\n"
                        "2. All colors are valid hex format (e.g., #667eea)\n"
                        "3. File is valid JSON format"
                    )
            except ValueError as e:
                QMessageBox.critical(
                    self,
                    "Theme Error",
                    f"Invalid color format in theme file:\n\n{str(e)}\n\n"
                    "Please ensure all colors are valid hex codes (e.g., #667eea)."
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Theme Error",
                    f"Unexpected error loading theme:\n\n{str(e)}"
                )
    
    def reset_theme(self):
        """Reset to default theme."""
        self.custom_theme_path = None
        self.apply_theme()
        QMessageBox.information(self, "Theme Reset", "Theme reset to default.")
    
    def add_to_history(self, value: float, from_unit: str, to_unit: str, result: float, category: str, label: str = ""):
        """Add a conversion to the history with proper formatting for large numbers."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format input value
        if abs(value) >= 1e6 or (abs(value) < 1e-3 and value != 0):
            formatted_value = f"{value:.6e}".rstrip('0').rstrip('.')
        else:
            formatted_value = f"{value:.6f}".rstrip('0').rstrip('.')
        
        # Format result value
        if abs(result) >= 1e6 or (abs(result) < 1e-3 and result != 0):
            formatted_result = f"{result:.6e}".rstrip('0').rstrip('.')
        else:
            formatted_result = f"{result:.6f}".rstrip('0').rstrip('.')
        
        # Build history entry with optional label
        label_part = f" [{label}]" if label.strip() else ""
        history_entry = f"[{timestamp}]{label_part} {formatted_value} {from_unit} → {formatted_result} {to_unit} ({category})"
        self.conversion_history.insert(0, history_entry)
        
        # Add to list widget with word wrap enabled
        item = QListWidgetItem(history_entry)
        item.setToolTip(history_entry)  # Show full text on hover
        # Set minimum height for items to accommodate wrapped text
        current_size = item.sizeHint()
        min_size = QSize(current_size.width(), max(current_size.height(), 40))
        item.setSizeHint(min_size)
        self.history_list.insertItem(0, item)
        
        # Limit history to 50 entries
        if len(self.conversion_history) > 50:
            self.conversion_history.pop()
            self.history_list.takeItem(self.history_list.count() - 1)
    
    def clear_history(self):
        """Clear the conversion history."""
        self.conversion_history.clear()
        self.history_list.clear()
    
    def export_history(self):
        """Export conversion history to a file."""
        if not self.conversion_history:
            QMessageBox.information(
                self,
                "No History",
                "There is no conversion history to export."
            )
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Conversion History",
            "pytrics_history.txt",
            "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    if file_path.endswith('.csv'):
                        # Write CSV format
                        f.write("Timestamp,Label,Input Value,From Unit,Result,To Unit,Category\n")
                        for entry in self.conversion_history:
                            # Parse the entry to extract components
                            # Format: [HH:MM:SS] [label] value from_unit → result to_unit (Category)
                            # Label is optional
                            match = re.match(r'\[(\d{2}:\d{2}:\d{2})\](?: \[(.+?)\])? (.+?) (.+?) → (.+?) (.+?) \((.+?)\)', entry)
                            if match:
                                timestamp, label, input_val, from_unit, result, to_unit, category = match.groups()
                                label = label if label else ""
                                f.write(f'"{timestamp}","{label}","{input_val}","{from_unit}","{result}","{to_unit}","{category}"\n')
                            else:
                                # Fallback: write the whole entry
                                f.write(f'"{entry}"\n')
                    else:
                        # Write plain text format
                        f.write("Pytrics Conversion History\n")
                        f.write("=" * 60 + "\n\n")
                        for entry in self.conversion_history:
                            f.write(entry + "\n")
                
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Conversion history exported successfully to:\n{file_path}"
                )
            except IOError as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to export history:\n\n{str(e)}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"An unexpected error occurred:\n\n{str(e)}"
                )
    
    def on_input_changed(self):
        """Handle input field or unit changes - clear output."""
        self.output_field.clear()
    
    def convert(self):
        """Perform the unit conversion."""
        try:
            # Get input value (take first line only for conversion)
            input_text = self.input_field.toPlainText().strip()
            if not input_text:
                self.output_field.clear()
                return
            
            # Take only the first line if multiple lines entered
            first_line = input_text.split('\n')[0].strip()
            if not first_line:
                self.output_field.clear()
                return
            
            value = float(first_line)
            
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
            
            # Format result with better handling for large numbers
            if abs(result) >= 1e6 or (abs(result) < 1e-3 and result != 0):
                # Use scientific notation for very large or very small numbers
                formatted_result = f"{result:.6e}".rstrip('0').rstrip('.')
            else:
                # Use regular decimal notation
                formatted_result = f"{result:.6f}".rstrip('0').rstrip('.')
            
            # Display result
            self.output_field.setPlainText(formatted_result)
            
            # Get label if provided
            label = self.label_field.text().strip()
            
            # Add to history
            self.add_to_history(value, from_unit_str, to_unit_str, result, self.current_category.value, label)
            
        except ValueError as e:
            error_msg = str(e)
            if "invalid" in error_msg.lower() or "overflow" in error_msg.lower():
                QMessageBox.warning(
                    self,
                    "Invalid Conversion",
                    f"Conversion error: {error_msg}\n\n"
                    "This may be due to:\n"
                    "- Number too large or too small\n"
                    "- Invalid unit selection\n"
                    "Please try a different value or check your unit selections."
                )
            else:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
        except KeyError as e:
            QMessageBox.critical(
                self,
                "Conversion Error",
                f"Conversion factor missing: {str(e)}\n\n"
                "This is a programming error. Please report this issue."
            )
        except ZeroDivisionError as e:
            QMessageBox.critical(
                self,
                "Conversion Error",
                f"Division by zero error: {str(e)}\n\n"
                "This is a programming error. Please report this issue."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    
    window = UnitConverterApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

