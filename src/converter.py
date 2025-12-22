"""Unit conversion logic for the Pytrics application."""

from enum import Enum
from typing import Dict


class UnitCategory(Enum):
    """Categories of units that can be converted."""
    LENGTH = "Length"
    WEIGHT = "Weight"
    TEMPERATURE = "Temperature"
    VOLUME = "Volume"


class LengthUnit(Enum):
    """Length units."""
    METERS = "meters"
    KILOMETERS = "kilometers"
    CENTIMETERS = "centimeters"
    MILLIMETERS = "millimeters"
    MILES = "miles"
    YARDS = "yards"
    FEET = "feet"
    INCHES = "inches"


class WeightUnit(Enum):
    """Weight units."""
    KILOGRAMS = "kilograms"
    GRAMS = "grams"
    POUNDS = "pounds"
    OUNCES = "ounces"
    TONS = "tons"
    METRIC_TONS = "metric_tons"


class TemperatureUnit(Enum):
    """Temperature units."""
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KELVIN = "kelvin"


class VolumeUnit(Enum):
    """Volume units."""
    LITERS = "liters"
    MILLILITERS = "milliliters"
    GALLONS = "gallons"
    QUARTS = "quarts"
    PINTS = "pints"
    CUPS = "cups"
    FLUID_OUNCES = "fluid_ounces"


class UnitConverter:
    """Handles unit conversions between different measurement systems."""
    
    # Conversion factors to base unit (meters for length, kg for weight, etc.)
    LENGTH_TO_METERS: Dict[LengthUnit, float] = {
        LengthUnit.METERS: 1.0,
        LengthUnit.KILOMETERS: 1000.0,
        LengthUnit.CENTIMETERS: 0.01,
        LengthUnit.MILLIMETERS: 0.001,
        LengthUnit.MILES: 1609.344,
        LengthUnit.YARDS: 0.9144,
        LengthUnit.FEET: 0.3048,
        LengthUnit.INCHES: 0.0254,
    }
    
    WEIGHT_TO_KILOGRAMS: Dict[WeightUnit, float] = {
        WeightUnit.KILOGRAMS: 1.0,
        WeightUnit.GRAMS: 0.001,
        WeightUnit.POUNDS: 0.453592,
        WeightUnit.OUNCES: 0.0283495,
        WeightUnit.TONS: 907.185,
        WeightUnit.METRIC_TONS: 1000.0,
    }
    
    VOLUME_TO_LITERS: Dict[VolumeUnit, float] = {
        VolumeUnit.LITERS: 1.0,
        VolumeUnit.MILLILITERS: 0.001,
        VolumeUnit.GALLONS: 3.78541,
        VolumeUnit.QUARTS: 0.946353,
        VolumeUnit.PINTS: 0.473176,
        VolumeUnit.CUPS: 0.236588,
        VolumeUnit.FLUID_OUNCES: 0.0295735,
    }
    
    @staticmethod
    def convert_length(value: float, from_unit: LengthUnit, to_unit: LengthUnit) -> float:
        """Convert length from one unit to another."""
        if from_unit == to_unit:
            return value
        
        # Convert to meters first, then to target unit
        meters = value * UnitConverter.LENGTH_TO_METERS[from_unit]
        return meters / UnitConverter.LENGTH_TO_METERS[to_unit]
    
    @staticmethod
    def convert_weight(value: float, from_unit: WeightUnit, to_unit: WeightUnit) -> float:
        """Convert weight from one unit to another."""
        if from_unit == to_unit:
            return value
        
        # Convert to kilograms first, then to target unit
        kilograms = value * UnitConverter.WEIGHT_TO_KILOGRAMS[from_unit]
        return kilograms / UnitConverter.WEIGHT_TO_KILOGRAMS[to_unit]
    
    @staticmethod
    def convert_temperature(value: float, from_unit: TemperatureUnit, to_unit: TemperatureUnit) -> float:
        """Convert temperature from one unit to another."""
        if from_unit == to_unit:
            return value
        
        # Convert to Celsius first
        if from_unit == TemperatureUnit.CELSIUS:
            celsius = value
        elif from_unit == TemperatureUnit.FAHRENHEIT:
            celsius = (value - 32) * 5 / 9
        elif from_unit == TemperatureUnit.KELVIN:
            celsius = value - 273.15
        else:
            celsius = value
        
        # Convert from Celsius to target unit
        if to_unit == TemperatureUnit.CELSIUS:
            return celsius
        elif to_unit == TemperatureUnit.FAHRENHEIT:
            return (celsius * 9 / 5) + 32
        elif to_unit == TemperatureUnit.KELVIN:
            return celsius + 273.15
        else:
            return celsius
    
    @staticmethod
    def convert_volume(value: float, from_unit: VolumeUnit, to_unit: VolumeUnit) -> float:
        """Convert volume from one unit to another."""
        if from_unit == to_unit:
            return value
        
        # Convert to liters first, then to target unit
        liters = value * UnitConverter.VOLUME_TO_LITERS[from_unit]
        return liters / UnitConverter.VOLUME_TO_LITERS[to_unit]

