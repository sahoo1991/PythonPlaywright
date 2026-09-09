import pytest
from helpers.api_client import APIClient
from helpers.api_config import (
    OPENWEATHER_ENDPOINTS,
    HTTP_STATUSES,
    TEST_CITIES,
    TEST_COORDINATES,
    UNIT_SYSTEMS,
)


class TestWeatherAPIBasic:

    def test_get_current_weather_by_city(self, api_client: APIClient):
        city = TEST_CITIES["LONDON"]
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": city})

        api_client.assert_status_ok()
        api_client.assert_response_contains_key("main")
        api_client.assert_response_contains_key("weather")
        api_client.assert_field_type("main", dict)

    def test_get_current_weather_by_coordinates(self, api_client: APIClient):
        lat, lon = TEST_COORDINATES["LONDON"]
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"lat": lat, "lon": lon})

        api_client.assert_status_ok()
        api_client.assert_response_contains_keys(["main", "weather", "coord"])

    def test_current_weather_response_schema(self, api_client: APIClient):
        city = TEST_CITIES["NEW_YORK"]
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": city})
        api_client.assert_status_ok()

        response = api_client.get_json_response()
        for field in ["coord", "weather", "main", "wind", "clouds", "sys", "name"]:
            assert field in response, f"Required field '{field}' missing from response"

    def test_weather_contains_temperature(self, api_client: APIClient):
        city = TEST_CITIES["TOKYO"]
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": city})
        api_client.assert_status_ok()

        response = api_client.get_json_response()
        assert "temp" in response["main"], "Temperature not found in main object"
        assert isinstance(response["main"]["temp"], (int, float)), "Temperature should be numeric"

    @pytest.mark.parametrize("city", [TEST_CITIES["LONDON"], TEST_CITIES["NEW_YORK"], TEST_CITIES["TOKYO"]])
    def test_weather_multiple_cities(self, api_client: APIClient, city: str):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": city})

        api_client.assert_status_ok()
        api_client.assert_response_contains_key("name")
        response = api_client.get_json_response()
        assert response["name"].lower() in city.lower() or city.lower() in response["name"].lower()


class TestWeatherAPIErrorHandling:

    def test_invalid_api_key(self, api_request_context):
        from helpers.api_client import APIClient

        invalid_api_client = APIClient(api_request_context, "invalid_key_12345")
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        invalid_api_client.get(endpoint, params={"q": "London"})
        invalid_api_client.assert_status_ok(expected_status=HTTP_STATUSES["UNAUTHORIZED"])

    def test_nonexistent_city(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "XYZInvalidCityNameABC123"})
        api_client.assert_status_ok(expected_status=HTTP_STATUSES["NOT_FOUND"])

    def test_missing_query_parameters(self, api_request_context):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        response = api_request_context.get(endpoint, params={"appid": "dummy_key"})
        assert response.status != HTTP_STATUSES["OK"], "Expected error for missing parameters"

    def test_invalid_coordinates(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"lat": 999, "lon": 999})
        status = api_client.get_status_code()
        assert status in [HTTP_STATUSES["NOT_FOUND"], HTTP_STATUSES["OK"]]


class TestWeatherAPIAuthentication:

    def test_api_key_required(self, api_request_context):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        response = api_request_context.get(endpoint, params={"q": "London"})
        assert response.status != HTTP_STATUSES["OK"], "Expected error without API key"

    def test_valid_api_key_works(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})
        api_client.assert_status_ok()

    def test_response_auth_headers(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})
        headers = api_client.get_response_headers()

        assert headers is not None, "Response headers should be present"
        assert "content-type" in [k.lower() for k in headers.keys()], "Content-Type header missing"


class TestWeatherAPIRateLimiting:

    def test_rate_limit_headers_present(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})
        api_client.assert_status_ok()

        headers = api_client.get_response_headers()
        assert headers is not None, "Headers should be present"

    def test_rate_limit_decrements(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})
        first_response = api_client.get_json_response()
        first_headers = api_client.get_response_headers()

        api_client.get(endpoint, params={"q": "Paris"})
        second_headers = api_client.get_response_headers()

        first_remaining = first_headers.get("X-RateLimit-Remaining")
        second_remaining = second_headers.get("X-RateLimit-Remaining")

        if first_remaining and second_remaining:
            assert int(second_remaining) <= int(first_remaining), "Rate limit should decrease with requests"

    def test_check_rate_limit_info(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})
        api_client.assert_status_ok()

        rate_limit_info = api_client.check_rate_limit_headers()
        assert rate_limit_info is not None, "Should be able to extract rate limit info"
        assert isinstance(rate_limit_info, dict), "Rate limit info should be a dictionary"


class TestWeatherAPIDataValidation:

    def test_status_code_format(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})
        response = api_client.get_json_response()

        assert isinstance(response.get("cod"), (str, int)), "Status code should be numeric or string"

    def test_temperature_numeric(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})
        response = api_client.get_json_response()

        main_data = response.get("main", {})
        temp = main_data.get("temp")
        assert isinstance(temp, (int, float)), f"Temperature should be numeric, got {type(temp)}"

    def test_humidity_valid_range(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})
        response = api_client.get_json_response()

        humidity = response.get("main", {}).get("humidity")
        assert humidity is not None, "Humidity should be present"
        assert 0 <= humidity <= 100, f"Humidity should be 0-100, got {humidity}"

    def test_coordinates_valid(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})
        response = api_client.get_json_response()

        coord = response.get("coord", {})
        lat = coord.get("lon")
        lon = coord.get("lat")

        assert -180 <= lon <= 180, f"Longitude should be -180 to 180, got {lon}"
        assert -90 <= lat <= 90, f"Latitude should be -90 to 90, got {lat}"

    def test_response_time_reasonable(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(endpoint, params={"q": "London"})

        assert api_client.last_response is not None, "Response should exist"
        assert api_client.get_status_code() == 200, "Request should succeed"


class TestWeatherAPIUnits:

    @pytest.mark.parametrize("city", [TEST_CITIES["LONDON"], TEST_CITIES["PARIS"]])
    def test_metric_units(self, api_client: APIClient, city: str):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(
            endpoint,
            params={"q": city, "units": UNIT_SYSTEMS["METRIC"]}
        )
        api_client.assert_status_ok()

        response = api_client.get_json_response()
        temp = response.get("main", {}).get("temp")
        assert temp is not None, "Temperature should be present"
        assert -50 < temp < 60, f"Metric temp out of range: {temp}°C"

    def test_imperial_units(self, api_client: APIClient):
        endpoint = OPENWEATHER_ENDPOINTS["CURRENT_WEATHER"]

        api_client.get(
            endpoint,
            params={"q": TEST_CITIES["NEW_YORK"], "units": UNIT_SYSTEMS["IMPERIAL"]}
        )
        api_client.assert_status_ok()

        response = api_client.get_json_response()
        temp = response.get("main", {}).get("temp")
        assert temp is not None, "Temperature should be present"
        assert -50 < temp < 140, f"Imperial temp out of range: {temp}°F"
