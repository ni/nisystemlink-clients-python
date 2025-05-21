from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class CalibrationStatus(Enum):
    """Calibration category the asset belongs to based on the next due calibration date."""

    OK = "OK"
    APPROACHING_RECOMMENDED_DUE_DATE = "APPROACHING_RECOMMENDED_DUE_DATE"
    PAST_RECOMMENDED_DUE_DATE = "PAST_RECOMMENDED_DUE_DATE"
    OUT_FOR_CALIBRATION = "OUT_FOR_CALIBRATION"


class TemperatureSensor(JsonModel):
    """Temperature sensor information."""

    name: Optional[str] = None
    """Gets or sets sensor name."""

    reading: float
    """Gets or sets sensor reading."""


class SelfCalibration(JsonModel):
    temperature_sensors: Optional[List[TemperatureSensor]] = None
    """Gets or sets an array of temperature sensor information."""

    is_limited: Optional[bool] = None
    """Gets or sets whether the last self-calibration of the asset was a limited calibration."""

    date: datetime
    """Gets or sets ISO-8601 formatted timestamp specifying the last date the asset was self-calibrated."""


class CalibrationMode(Enum):
    """Whether SystemLink automatically discovered the calibration data for an asset or if it was manually entered."""

    AUTOMATIC = "AUTOMATIC"
    MANUAL = "MANUAL"


class ExternalCalibration(JsonModel):
    temperature_sensors: Optional[List[TemperatureSensor]] = None
    """Gets or sets an array of temperature sensor information."""

    is_limited: Optional[bool] = None
    """Gets or sets whether the last external calibration of the asset was a limited calibration."""

    date: datetime
    """Gets or sets ISO-8601 formatted timestamp specifying the last date the asset was externally calibrated."""

    recommended_interval: int
    """Gets or sets the manufacturer's recommended calibration interval in months."""

    next_recommended_date: datetime
    """Gets or sets ISO-8601 formatted timestamp specifying the recommended date for the next external calibration."""

    next_custom_due_date: Optional[datetime] = None
    """Gets or sets ISO-8601 formatted timestamp specifying the date for the next external calibration."""

    resolved_due_date: Optional[datetime] = None
    """Gets ISO-8601 formatted timestamp specifying the resolved due date for external calibration."""

    comments: Optional[str] = None
    """Gets or sets calibration comments provided by an operator."""

    entry_type: Optional[CalibrationMode] = None
    """Gets or sets whether automatically discovered the calibration data for an asset or manually entered."""
