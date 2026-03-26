"""
Weather Info Agent — returns mock weather data for destinations.

To upgrade: replace `_get_weather()` with an OpenWeatherMap or WeatherAPI call.
Free tier: https://openweathermap.org/api
"""

_MOCK_WEATHER: dict[str, dict] = {
    "Thailand": {
        "temp": "32°C", "condition": "☀️ Sunny & Humid",
        "best_season": "Nov – Feb (cool & dry)",
        "tip": "Avoid Jun-Oct monsoon season unless you love rain discounts!",
    },
    "Japan": {
        "temp": "18°C", "condition": "🌸 Pleasant, Cherry Blossom Season",
        "best_season": "Mar – May (spring) or Oct – Nov (autumn)",
        "tip": "Book early for cherry blossom season — hotels sell out months ahead.",
    },
    "Maldives": {
        "temp": "30°C", "condition": "☀️ Tropical & Warm",
        "best_season": "Dec – Apr (dry season)",
        "tip": "Wet season (May-Nov) has 30-50% lower resort prices.",
    },
    "France": {
        "temp": "15°C", "condition": "🌤️ Mild & Partly Cloudy",
        "best_season": "Jun – Sep (summer)",
        "tip": "Paris in spring (Apr-May) is magical and less crowded.",
    },
    "Dubai": {
        "temp": "38°C", "condition": "🔥 Hot & Dry",
        "best_season": "Nov – Mar (cooler months)",
        "tip": "Summer (Jun-Sep) is extremely hot but you'll find amazing hotel deals.",
    },
    "Nepal": {
        "temp": "22°C", "condition": "⛰️ Clear Mountain Views",
        "best_season": "Oct – Nov (post-monsoon, best trekking)",
        "tip": "Everest Base Camp trek is best attempted in October or April.",
    },
    "Singapore": {
        "temp": "31°C", "condition": "🌧️ Warm & Occasional Showers",
        "best_season": "Feb – Apr (least rainfall)",
        "tip": "It rains year-round but only in short bursts. Always carry an umbrella!",
    },
    "Turkey": {
        "temp": "24°C", "condition": "🌤️ Warm Mediterranean",
        "best_season": "Apr – Jun or Sep – Nov",
        "tip": "Cappadocia hot air balloons fly best in calm morning weather (May-Oct).",
    },
    "United States": {
        "temp": "22°C", "condition": "🌤️ Varies by Region",
        "best_season": "Depends on destination",
        "tip": "The US spans multiple climate zones — research your specific city!",
    },
    "South Korea": {
        "temp": "20°C", "condition": "🍂 Cool & Crisp",
        "best_season": "Sep – Nov (autumn foliage)",
        "tip": "Cherry blossoms in April, colorful autumn leaves in October.",
    },
}

_DEFAULT_WEATHER = {
    "temp": "25°C", "condition": "🌤️ Moderate",
    "best_season": "Check local climate guides",
    "tip": "Research the specific region's weather before booking!",
}


def weather_node(state: dict) -> dict:
    """LangGraph node: fetches weather info for the destination."""
    dest = state.get("destination", "").strip().title()
    weather = _MOCK_WEATHER.get(dest, _DEFAULT_WEATHER)

    return {
        "weather_result": {
            "destination": dest,
            **weather,
            "agent": "Weather Intel Agent",
        }
    }
