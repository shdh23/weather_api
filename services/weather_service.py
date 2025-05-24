import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
api_key = os.getenv("WEATHER_API_KEY")

def fetch_weather_from_api(city):
    try:
        url = f"{BASE_URL}/{city}?key={api_key}&unitGroup=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        today = data["days"][0]

        return {
            "city": city,
            "date": today["datetime"],
            "temp": today["temp"],
            "description": today["description"],
            "humidity": today["humidity"],
            "precip": today["precip"],
            "wind": today["windspeed"]
        }

    except requests.RequestException as e:
        logging.error(f"[Weather API error] Request failed: {e}")
        raise Exception("Weather service unavailable")

    except (KeyError, IndexError, ValueError) as e:
        logging.error(f"[Weather API error] Bad response format: {e}")
        raise Exception("Invalid response format from weather API")