from app.weather.schemas import WeatherContext, WeatherInput, WindLevel
from app.weather.service import WeatherService


class ManualWeatherService(WeatherService):
    def resolve_weather(self, weather_input: WeatherInput | None) -> WeatherContext | None:
        if weather_input is None:
            return None

        return WeatherContext(
            temperature_c=weather_input.temperature_c,
            condition=weather_input.condition,
            precipitation=weather_input.precipitation,
            wind_level=weather_input.wind_level or WindLevel.CALM,
        )
