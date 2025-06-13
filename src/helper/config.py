"""
Configuration constants for the microwave control system.

This module defines various constants used throughout the application to control
logging, environment parameters, hardware timing, and operational limits.
"""

DEFAULT_LOG_LEVEL: str = "INFO"
"""str: The default logging level for the application."""

AMBIENT_TEMPERATURE_IN_CELSIUS: float = 22.0
"""float: The default ambient temperature in degrees Celsius."""

AMBIENT_HUMIDITY_IN_PERCENT: float = 40.0
"""float: The default ambient humidity as a percentage."""

MAIN_LOOP_TIMEOUT_IN_SECONDS: float = 0.01
"""float: Timeout interval for the main control loop in seconds."""

MAGNETRON_ON_OFF_INTERVAL_IN_SECONDS: float = 0.1
"""float: Interval in seconds for toggling the magnetron on and off."""

MAGNETRON_MAX_POWER_SHARE_PER_MINUTE: float = 0.8
"""float: Maximum allowed power share for the magnetron per minute."""

MAGNETRON_MAX_TEMP_IN_CELSIUS: float = 200.0
"""float: Maximum allowed temperature for the magnetron in degrees Celsius."""

COOLING_FAN_STEP_IN_PERCENT: float = 0.1
"""float: Step size for adjusting the cooling fan speed as a percentage."""

COOLING_FAN_UPDATE_INTERVAL_IN_SECONDS: float = 0.1
"""float: Interval in seconds for updating the cooling fan speed."""

TURNTABLE_WEIGHT_IN_GRAMS: int = 420
"""int: Weight of the turntable in grams."""

TURNTABLE_MAX_ROTATIONS_PER_MINUTE: int = 5
"""int: Maximum allowed rotations per minute for the turntable."""

TURNTABLE_MIN_ROTATIONS_PER_MINUTE: int = -5
"""int: Minimum allowed rotations per minute for the turntable."""

TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE: float = 0.1
"""float: Step size for adjusting the turntable speed in rotations per minute."""

REFLECTOR_MAX_ANGLE_IN_DEGREES: float = 90.0
"""float: Maximum allowed angle for the reflector in degrees."""

REFLECTOR_MIN_ANGLE_IN_DEGREES: float = -90.0
"""float: Minimum allowed angle for the reflector in degrees."""

REFLECTOR_STEP_IN_DEGREES: float = 0.1
"""float: Step size for adjusting the reflector angle in degrees."""

LIGHT_UPDATE_INTERVAL_IN_SECONDS: float = 0.1
"""float: Interval in seconds for updating the light status."""

PROGRAM_UPDATE_INTERVAL_IN_SECONDS: float = 0.01
"""float: Interval in seconds for updating the program state."""

PROGRAM_DEFROSTING_TARGET_TEMP: int = 60
"""int: Target temperature in degrees Celsius for the defrosting program."""
