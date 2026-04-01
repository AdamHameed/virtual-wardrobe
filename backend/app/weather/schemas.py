from enum import Enum

from pydantic import BaseModel


class WindLevel(str, Enum):
    CALM = "calm"
    BREEZY = "breezy"
    WINDY = "windy"


class WeatherInput(BaseModel):
    temperature_c: float | None = None
    condition: str | None = None
    precipitation: bool = False
    wind_level: WindLevel | None = None


class WeatherContext(BaseModel):
    temperature_c: float | None = None
    condition: str | None = None
    precipitation: bool = False
    wind_level: WindLevel = WindLevel.CALM
