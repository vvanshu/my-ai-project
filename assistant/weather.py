"""
weather.py — Fetch current weather from the free wttr.in API.
"""

import requests


WTTR_URL = "https://wttr.in/{city}?format=j1"

# Map wttr.in weather codes to emoji
_WEATHER_EMOJI = {
    "113": "☀️",   # Clear/Sunny
    "116": "⛅",   # Partly cloudy
    "119": "☁️",   # Cloudy
    "122": "☁️",   # Overcast
    "143": "🌫️",  # Mist
    "176": "🌦️",  # Patchy rain
    "179": "🌨️",  # Patchy snow
    "182": "🌧️",  # Patchy sleet
    "185": "🌧️",  # Patchy freezing drizzle
    "200": "⛈️",   # Thundery outbreaks
    "227": "🌨️",  # Blowing snow
    "230": "❄️",   # Blizzard
    "248": "🌫️",  # Fog
    "260": "🌫️",  # Freezing fog
    "263": "🌦️",  # Patchy light drizzle
    "266": "🌧️",  # Light drizzle
    "281": "🌧️",  # Freezing drizzle
    "284": "🌧️",  # Heavy freezing drizzle
    "293": "🌦️",  # Patchy light rain
    "296": "🌧️",  # Light rain
    "299": "🌧️",  # Moderate rain at times
    "302": "🌧️",  # Moderate rain
    "305": "🌧️",  # Heavy rain at times
    "308": "🌧️",  # Heavy rain
    "311": "🌧️",  # Light freezing rain
    "314": "🌧️",  # Moderate/heavy freezing rain
    "317": "🌨️",  # Light sleet
    "320": "🌨️",  # Moderate/heavy sleet
    "323": "🌨️",  # Patchy light snow
    "326": "🌨️",  # Light snow
    "329": "🌨️",  # Patchy moderate snow
    "332": "🌨️",  # Moderate snow
    "335": "❄️",   # Patchy heavy snow
    "338": "❄️",   # Heavy snow
    "350": "🌧️",  # Ice pellets
    "353": "🌦️",  # Light rain shower
    "356": "🌧️",  # Moderate/heavy rain shower
    "359": "🌧️",  # Torrential rain shower
    "362": "🌨️",  # Light sleet showers
    "365": "🌨️",  # Moderate/heavy sleet showers
    "368": "🌨️",  # Light snow showers
    "371": "❄️",   # Moderate/heavy snow showers
    "374": "🌧️",  # Light showers of ice pellets
    "377": "🌧️",  # Moderate/heavy ice pellet showers
    "386": "⛈️",   # Patchy light rain with thunder
    "389": "⛈️",   # Moderate/heavy rain with thunder
    "392": "⛈️",   # Patchy light snow with thunder
    "395": "⛈️",   # Moderate/heavy snow with thunder
}


def get_weather(city: str) -> dict:
    """
    Fetch current weather for the given city.

    Returns a dict with keys:
        city, temp_c, temp_f, description, humidity, wind_kph,
        feels_like_c, emoji, uv_index, visibility_km

    Raises ValueError on failure.
    """
    city = city.strip()
    if not city:
        raise ValueError("City name cannot be empty.")

    try:
        url = WTTR_URL.format(city=requests.utils.quote(city))
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.ConnectionError:
        raise ValueError("No internet connection. Please check your network.")
    except requests.Timeout:
        raise ValueError("Request timed out. Please try again.")
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch weather: {e}")
    except (ValueError, KeyError):
        raise ValueError("Received invalid data from the weather service.")

    try:
        current = data["current_condition"][0]
        area = data["nearest_area"][0]

        city_name = area.get("areaName", [{}])[0].get("value", city)
        country = area.get("country", [{}])[0].get("value", "")
        weather_code = current.get("weatherCode", "")

        return {
            "city": f"{city_name}, {country}" if country else city_name,
            "temp_c": current.get("temp_C", "N/A"),
            "temp_f": current.get("temp_F", "N/A"),
            "description": current.get("weatherDesc", [{}])[0].get("value", "Unknown"),
            "humidity": current.get("humidity", "N/A"),
            "wind_kph": current.get("windspeedKmph", "N/A"),
            "wind_dir": current.get("winddir16Point", ""),
            "feels_like_c": current.get("FeelsLikeC", "N/A"),
            "emoji": _WEATHER_EMOJI.get(weather_code, "🌡️"),
            "uv_index": current.get("uvIndex", "N/A"),
            "visibility_km": current.get("visibility", "N/A"),
        }
    except (KeyError, IndexError, TypeError):
        raise ValueError(f"Could not parse weather data for '{city}'.")
