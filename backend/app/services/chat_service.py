import re

from app.services.weather_service import WeatherService
from app.services.llm_service import LLMService

class ChatService:
    def __init__(self):
        self.weather_service = WeatherService()
        self.llm_service = LLMService()

    def extract_city(self, message: str) -> str | None:
        text = message.strip().lower()

        patterns = [
            r"weather\s+(?:in|at|for)\s+([a-zA-Z\s-]+)",
            r"([a-zA-Z\s-]+)\s+weather",
            r"weather\s+([a-zA-Z\s-]+)",
            r"in\s+([a-zA-Z\s-]+)\s+what's the weather",
            r"forecast\s+(?:in|for)\s+([a-zA-Z\s-]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                city = match.group(1).strip()
                if city:
                    return city.title()

        return None

    async def handle_message(self, message: str):
        city = self.extract_city(message)
        if not city:
            return {
                "response": "Main weather check kar sakta hoon. Bas city ka naam bata dijiye, jaise: 'Weather in Lahore' ya 'Karachi weather'.",
                "city": None,
                "temperature": None,
                "feels_like": None,
                "description": None,
                "forecast": [],
            }

        weather = await self.weather_service.get_current_weather(city)
        forecast = await self.weather_service.get_forecast(city)
        response = await self.llm_service.generate_weather_response(message, weather, forecast)

        return {
            "response": response,
            "city": weather["city"],
            "temperature": weather["temperature"],
            "feels_like": weather["feels_like"],
            "description": weather["description"],
            "forecast": forecast,
        }
