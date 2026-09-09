# PythonPlaywright
Production level python + pytest + playwright framework.

## API Testing with Playwright

This framework now includes comprehensive REST API testing capabilities using Playwright's `APIRequestContext`. 

### Setup

1. **Get an OpenWeatherMap API Key** (Free)
   - Visit https://openweathermap.org/api
   - Sign up for a free account
   - Generate an API key from your account dashboard

2. **Configure Environment Variables**
   - Copy `.env.template` to `.env` (if not already done)
   - Add your OpenWeatherMap API key:
     ```
     OPENWEATHER_API_KEY=your_api_key_here
     ```

### Running API Tests

Run all API tests:
```bash
pytest tests/api -v
```

Run specific test class:
```bash
pytest tests/api/test_weather_api.py::TestWeatherAPIBasic -v
```

Run specific test:
```bash
pytest tests/api/test_weather_api.py::TestWeatherAPIBasic::test_get_current_weather_by_city -v
```

### Test Coverage

The API test suite includes:

- **Basic Tests**: Query weather by city and coordinates, validate response schema
- **Error Handling**: Invalid API keys (401), non-existent cities (404), missing parameters
- **Authentication**: Verify API key requirements and token validation
- **Rate Limiting**: Monitor and validate rate limit headers and behavior
- **Data Validation**: Ensure temperature, humidity, coordinates are within valid ranges
- **Unit Systems**: Test metric (Celsius), imperial (Fahrenheit), and standard (Kelvin) units

### Available Fixtures

- `api_client`: Initialized APIClient with request context and API key
- `api_request_context`: Raw Playwright APIRequestContext
- `api_key`: OpenWeatherMap API key from environment
- `api_base_url`: Base URL for OpenWeatherMap API

### API Client Helper

The `APIClient` helper class (`helpers/api_client.py`) provides:

- **Request Methods**: `get()`, `post()`, `put()`, `delete()`
- **Response Assertions**: 
  - `assert_status_ok(expected_status)`
  - `assert_response_contains_key(key)`
  - `assert_field_value(key, expected_value)`
  - `assert_field_type(key, expected_type)`
- **Response Parsing**:
  - `get_json_response()`: Get parsed JSON response
  - `get_status_code()`: Get HTTP status
  - `get_response_headers()`: Get response headers
  - `check_rate_limit_headers()`: Extract rate limit info

### Example Test

```python
def test_get_weather_by_city(api_client: APIClient):
    """Query current weather for a city."""
    from helpers.api_config import OPENWEATHER_ENDPOINTS, TEST_CITIES
    
    endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]
    city = TEST_CITIES["LONDON"]
    
    api_client.get(endpoint, params={"q": city})
    
    api_client.assert_status_ok()
    api_client.assert_response_contains_keys(["main", "weather"])
    
    response = api_client.get_json_response()
    assert response["name"].lower() == city.lower()
```

### Free API Tier Limits

- **OpenWeatherMap Free**: 60 calls/minute, 1,000,000 calls/month
- Tests are designed to respect rate limits and include validation checks

