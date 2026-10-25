from openai import AsyncOpenAI

from app.config import settings

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    async def generate_weather_response(self, user_message: str, weather: dict, forecast: list | None = None):
        if not self.client:
            return self._fallback_response(weather)

        forecast_text = ""
        if forecast:
            forecast_text = "\n".join(
                f"- {item['date']}: {item['temperature']}°C, {item['description']}"
                for item in forecast[:5]
            )

        prompt = f"""
You are a professional weather assistant.
User question: {user_message}
Current weather: {weather}
5-day forecast: {forecast_text}

Respond in a friendly but concise style in English or Urdu/Hindi, with practical advice.
"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    def _fallback_response(self, weather: dict):
        return (
            f"{weather['city']} ka mausam {weather['description']} hai. "
            f"Temperature {weather['temperature']}°C, feels like {weather['feels_like']}°C. "
            f"Humidity {weather['humidity']}% aur wind speed {weather['wind_speed']} m/s."
        )
