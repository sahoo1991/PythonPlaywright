OPENWEATHER_ENDPOINTS = {
    "CURRENT_WEATHER": "/data/2.5/weather",
    "FORECAST": "/data/2.5/forecast",
    "WEATHER_BY_CITY": "/data/2.5/weather",
    "WEATHER_BY_COORDS": "/data/2.5/weather",
}

CURRENT_WEATHER_FIELDS = [
    "coord",
    "weather",
    "main",
    "visibility",
    "wind",
    "clouds",
    "dt",
    "sys",
    "timezone",
    "id",
    "name",
    "cod",
]

HTTP_STATUSES = {
    "OK": 200,
    "UNAUTHORIZED": 401,
    "NOT_FOUND": 404,
    "TOO_MANY_REQUESTS": 429,
    "INTERNAL_SERVER_ERROR": 500,
}

QUERY_PARAMS = {
    "CITY": "q",
    "LATITUDE": "lat",
    "LONGITUDE": "lon",
    "API_KEY": "appid",
    "UNITS": "units",
    "LANGUAGE": "lang",
}

TEST_CITIES = {
    "LONDON": "London",
    "NEW_YORK": "New York",
    "TOKYO": "Tokyo",
    "SYDNEY": "Sydney",
    "PARIS": "Paris",
}

TEST_COORDINATES = {
    "LONDON": (51.5074, -0.1278),
    "NEW_YORK": (40.7128, -74.0060),
    "TOKYO": (35.6762, 139.6503),
}

UNIT_SYSTEMS = {
    "METRIC": "metric",      # Celsius
    "IMPERIAL": "imperial",  # Fahrenheit
    "STANDARD": "standard",  # Kelvin
}
