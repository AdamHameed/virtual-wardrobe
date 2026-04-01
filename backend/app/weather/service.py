from abc import ABC, abstractmethod

from app.weather.schemas import WeatherContext, WeatherInput


class WeatherService(ABC):
    @abstractmethod
    def resolve_weather(self, weather_input: WeatherInput | None) -> WeatherContext | None:
        raise NotImplementedError
