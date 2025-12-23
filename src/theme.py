"""Theme management for the Pytrics unit converter."""

import json
import os
from typing import Dict, Optional, Tuple


class ThemeManager:
    """Manages dark, light, and custom themes for the application."""
    
    # Default color palette (for custom themes)
    DEFAULT_COLORS = {
        'primary': '#667eea',
        'secondary': '#764ba2',
        'neutral': '#4a5568',
        'accent': '#48bb78',
        'status': '#ffffff'
    }
    
    # Dark mode color palette
    DARK_COLORS = {
        'primary': '#1a202c',  # Very dark gray-blue
        'secondary': '#2d3748',  # Dark gray-blue
        'neutral': '#718096',  # Medium gray for borders/text
        'accent': '#48bb78',  # Green accent
        'status': '#e2e8f0'  # Light gray for text
    }
    
    @staticmethod
    def _adjust_brightness(color: str, factor: float) -> str:
        """Adjust brightness of a hex color.
        
        Raises:
            ValueError: If color format is invalid
        """
        if not color or not isinstance(color, str):
            raise ValueError(f"Invalid color: must be a non-empty string, got {type(color).__name__}")
        
        if not color.startswith('#'):
            raise ValueError(f"Invalid color format: must start with #, got '{color}'")
        
        # Remove # and validate length
        color_hex = color.lstrip('#')
        if len(color_hex) != 6:
            raise ValueError(f"Invalid color format: must be 6 hex digits, got '{color}' (length: {len(color_hex)})")
        
        try:
            # Convert to RGB
            r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        except ValueError as e:
            raise ValueError(f"Invalid hex color: '{color}' contains non-hexadecimal characters") from e
        
        # Adjust brightness
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def _get_text_color(bg_color: str) -> str:
        """Determine appropriate text color based on background.
        
        Returns:
            '#ffffff' for dark backgrounds, '#000000' for light backgrounds
            Defaults to '#000000' if color format is invalid
        """
        if not bg_color or not isinstance(bg_color, str) or not bg_color.startswith('#'):
            return '#000000'
        
        try:
            color = bg_color.lstrip('#')
            if len(color) != 6:
                return '#000000'
            
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            
            # Calculate luminance
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            
            return '#ffffff' if luminance < 0.5 else '#000000'
        except (ValueError, IndexError):
            return '#000000'
    
    @staticmethod
    def load_custom_theme(file_path: str) -> Optional[Dict[str, str]]:
        """Load a custom theme from a JSON file.
        
        Returns:
            Dictionary of colors if valid, None if invalid or file error
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
            
            # Validate required colors exist
            required_colors = ['primary', 'secondary', 'neutral', 'accent', 'status']
            if not all(color in theme_data for color in required_colors):
                return None
            
            # Validate color formats
            for color_name, color_value in theme_data.items():
                if color_name in required_colors:
                    if not color_value or not isinstance(color_value, str):
                        return None
                    # Validate hex format
                    if not color_value.startswith('#'):
                        return None
                    if len(color_value) != 7:  # # + 6 hex digits
                        return None
                    # Validate hex characters
                    try:
                        int(color_value[1:], 16)
                    except ValueError:
                        return None
            
            return theme_data
        except (json.JSONDecodeError, IOError, OSError):
            return None
    
    @staticmethod
    def get_custom_stylesheet(colors: Dict[str, str], is_dark: bool = True) -> str:
        """Generate a stylesheet from custom colors.
        
        Raises:
            ValueError: If any color format is invalid
        """
        primary = colors.get('primary', ThemeManager.DEFAULT_COLORS['primary'])
        secondary = colors.get('secondary', ThemeManager.DEFAULT_COLORS['secondary'])
        neutral = colors.get('neutral', ThemeManager.DEFAULT_COLORS['neutral'])
        accent = colors.get('accent', ThemeManager.DEFAULT_COLORS['accent'])
        status = colors.get('status', ThemeManager.DEFAULT_COLORS['status'])
        
        # Validate and calculate variations with error handling
        try:
            accent_hover = ThemeManager._adjust_brightness(accent, 0.9)
            accent_pressed = ThemeManager._adjust_brightness(accent, 0.8)
            primary_hover = ThemeManager._adjust_brightness(primary, 0.9)
        except ValueError as e:
            # If color adjustment fails, use defaults
            raise ValueError(f"Invalid color format in theme: {str(e)}") from e
        
        # Determine text colors
        label_color = status if is_dark else neutral
        input_bg = '#ffffff'
        input_text = '#2d3748'
        input_border = neutral if is_dark else '#cbd5e0'
        if is_dark:
            list_bg = "rgba(255, 255, 255, 0.1)"
            list_border = "rgba(255, 255, 255, 0.2)"
            list_text = status
            # Calculate list_selected from primary color
            try:
                p_r = int(primary[1:3], 16)
                p_g = int(primary[3:5], 16)
                p_b = int(primary[5:7], 16)
                list_selected = f"rgba({p_r}, {p_g}, {p_b}, 0.5)"
            except (ValueError, IndexError):
                list_selected = "rgba(102, 126, 234, 0.5)"
        else:
            list_bg = "#ffffff"
            list_border = input_border
            list_text = input_text
            list_selected = "#edf2f7"
        
        return f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {primary}, stop:1 {secondary});
            }}
            QWidget {{
                background: transparent;
            }}
            QLabel {{
                color: {label_color};
                font-weight: bold;
            }}
            QComboBox {{
                background-color: {input_bg};
                border: 2px solid {input_border};
                border-radius: 10px;
                padding: 10px 12px;
                font-size: 14px;
                color: {input_text};
                min-width: 100px;
                min-height: 20px;
            }}
            QComboBox:hover {{
                border: 2px solid {primary};
                background-color: #f7fafc;
            }}
            QComboBox:focus {{
                border: 3px solid {primary};
                background-color: #f7fafc;
                outline: none;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 35px;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }}
            QComboBox::drop-down:hover {{
                background-color: rgba(102, 126, 234, 0.1);
            }}
            QTextEdit {{
                background-color: {input_bg};
                border: 2px solid {input_border};
                border-radius: 15px;
                padding: 12px;
                font-size: 15px;
                color: {input_text};
                selection-background-color: {primary};
                selection-color: {ThemeManager._get_text_color(primary)};
            }}
            QTextEdit QAbstractScrollArea::viewport {{
                background-color: transparent;
                border: none;
                border-radius: 15px;
            }}
            QTextEdit:focus {{
                border: 3px solid {primary};
                background-color: #f7fafc;
                outline: none;
                border-radius: 15px;
            }}
            QTextEdit:focus QAbstractScrollArea::viewport {{
                background-color: transparent;
                border-radius: 15px;
            }}
            QTextEdit:hover {{
                border: 2px solid {primary_hover};
                border-radius: 15px;
            }}
            QTextEdit:hover QAbstractScrollArea::viewport {{
                background-color: transparent;
                border-radius: 15px;
            }}
            QLineEdit {{
                background-color: {input_bg};
                border: 2px solid {input_border};
                border-radius: 10px;
                padding: 10px 12px;
                font-size: 14px;
                color: {input_text};
                selection-background-color: {primary};
                selection-color: {ThemeManager._get_text_color(primary)};
            }}
            QLineEdit:focus {{
                border: 3px solid {primary};
                background-color: #f7fafc;
                outline: none;
            }}
            QLineEdit:hover {{
                border: 2px solid {primary_hover};
            }}
            QPushButton {{
                background-color: {accent};
                color: {ThemeManager._get_text_color(accent)};
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 60px;
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: {accent_hover};
            }}
            QPushButton:pressed {{
                background-color: {accent_pressed};
            }}
            QListWidget {{
                background-color: {list_bg};
                border: 2px solid {list_border};
                border-radius: 8px;
                color: {list_text};
                font-size: 12px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {list_border};
                min-height: 40px;
            }}
            QListWidget::item:selected {{
                background-color: {list_selected};
            }}
            QListWidget::item:hover {{
                background-color: {list_selected};
            }}
            QMenuBar {{
                background-color: {'rgba(255, 255, 255, 0.15)' if is_dark else 'rgba(255, 255, 255, 0.8)'};
                color: {label_color};
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                spacing: 10px;
                border-bottom: {'none' if is_dark else '1px solid rgba(0, 0, 0, 0.1)'};
            }}
            QMenuBar::item {{
                background-color: {'rgba(255, 255, 255, 0.2)' if is_dark else 'transparent'};
                padding: 10px 20px;
                border-radius: 6px;
                spacing: 5px;
            }}
            QMenuBar::item:selected {{
                background-color: {'rgba(255, 255, 255, 0.35)' if is_dark else 'rgba(0, 0, 0, 0.1)'};
            }}
            QMenuBar::item:pressed {{
                background-color: {'rgba(255, 255, 255, 0.45)' if is_dark else 'rgba(0, 0, 0, 0.15)'};
            }}
            QMenu {{
                background-color: {input_bg};
                border: 2px solid {input_border};
                border-radius: 8px;
                padding: 8px;
                font-size: 15px;
                color: {input_text};
            }}
            QMenu::item {{
                background-color: rgba(102, 126, 234, 0.1);
                padding: 12px 24px;
                border-radius: 6px;
                min-width: 200px;
            }}
            QMenu::item:selected {{
                background-color: {primary};
                color: {ThemeManager._get_text_color(primary)};
            }}
            QMenu::item:pressed {{
                background-color: {primary_hover};
                color: {ThemeManager._get_text_color(primary)};
            }}
        """
    
    @staticmethod
    def get_dark_stylesheet() -> str:
        """Get the dark theme stylesheet."""
        return ThemeManager.get_custom_stylesheet(ThemeManager.DARK_COLORS, is_dark=True)
    
    @staticmethod
    def get_light_stylesheet() -> str:
        """Get the light theme stylesheet."""
        # Light theme uses bright, light colors for background
        light_colors = {
            'primary': '#ffffff',  # White/very light for top of gradient
            'secondary': '#f7fafc',  # Very light gray for bottom of gradient
            'neutral': '#2d3748',  # Dark text color
            'accent': '#48bb78',  # Green accent
            'status': '#2d3748'  # Dark text for labels
        }
        return ThemeManager.get_custom_stylesheet(light_colors, is_dark=False)
    
    @staticmethod
    def get_output_field_style(accent_color: str = None) -> str:
        """Get the output field stylesheet."""
        if accent_color is None:
            accent_color = ThemeManager.DEFAULT_COLORS['accent']
        
        return f"""
            QTextEdit {{
                background-color: #ffffff;
                border: 3px solid {accent_color};
                border-radius: 18px;
                padding: 20px;
                font-size: 20px;
                font-weight: bold;
                color: #2d3748;
                min-height: 100px;
                selection-background-color: {accent_color};
                selection-color: #ffffff;
            }}
            QTextEdit QAbstractScrollArea::viewport {{
                background-color: transparent;
                border: none;
                border-radius: 18px;
            }}
            QTextEdit:hover {{
                border: 3px solid {ThemeManager._adjust_brightness(accent_color, 0.9)};
                border-radius: 18px;
            }}
            QTextEdit:hover QAbstractScrollArea::viewport {{
                background-color: transparent;
                border-radius: 18px;
            }}
        """
    
    @staticmethod
    def get_stylesheet(dark_mode: bool, custom_theme_path: Optional[str] = None) -> Tuple[str, str]:
        """Get the appropriate stylesheet based on theme mode.
        
        Returns:
            Tuple of (main_stylesheet, output_field_style)
        """
        custom_colors = None
        accent_color = ThemeManager.DEFAULT_COLORS['accent']
        
        if custom_theme_path:
            custom_colors = ThemeManager.load_custom_theme(custom_theme_path)
            if custom_colors:
                accent_color = custom_colors.get('accent', accent_color)
        
        if custom_colors:
            stylesheet = ThemeManager.get_custom_stylesheet(custom_colors, is_dark=dark_mode)
        elif dark_mode:
            stylesheet = ThemeManager.get_dark_stylesheet()
        else:
            stylesheet = ThemeManager.get_light_stylesheet()
        
        output_style = ThemeManager.get_output_field_style(accent_color)
        
        return stylesheet, output_style
