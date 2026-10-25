import httpx

from app.config import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.OPENWEATHER_BASE_URL

    async def get_current_weather(self, city: str):
        if not self.api_key:
            raise ValueError("OpenWeather API key missing")

        url = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, params=params)

        if response.status_code != 200:
            raise ValueError(f"City not found or API error: {city}")

        data = response.json()
        return {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }

    async def get_forecast(self, city: str):
        if not self.api_key:
            raise ValueError("OpenWeather API key missing")

        url = f"{self.base_url}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "cnt": 40,
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, params=params)

        if response.status_code != 200:
            raise ValueError(f"Forecast unavailable for city: {city}")

        data = response.json()
        list_data = data.get("list", [])

        daily = {}
        for item in list_data:
            date = item["dt_txt"].split(" ")[0]
            if date not in daily:
                daily[date] = {
                    "temp": item["main"]["temp"],
                    "description": item["weather"][0]["description"].capitalize(),
                }
            else:
                daily[date]["temp"] = (daily[date]["temp"] + item["main"]["temp"]) / 2

        result = []
        for date, value in list(daily.items())[:5]:
            result.append({
                "date": date,
                "temperature": round(value["temp"], 1),
                "description": value["description"],
            })

        return result
