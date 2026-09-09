import json
from typing import Any, Dict, Optional, Union
from playwright.sync_api import APIRequestContext, APIResponse


class APIClient:

    def __init__(self, request_context: APIRequestContext, api_key: str):
        self.request_context = request_context
        self.api_key = api_key
        self.last_response: Optional[APIResponse] = None

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> APIResponse:
        if params is None:
            params = {}
        params["appid"] = self.api_key

        self.last_response = self.request_context.get(endpoint, params=params, **kwargs)
        return self.last_response

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> APIResponse:
        self.last_response = self.request_context.post(endpoint, data=json.dumps(data), **kwargs)
        return self.last_response

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> APIResponse:
        self.last_response = self.request_context.put(endpoint, data=json.dumps(data), **kwargs)
        return self.last_response

    def delete(self, endpoint: str, **kwargs) -> APIResponse:
        self.last_response = self.request_context.delete(endpoint, **kwargs)
        return self.last_response

    def get_json_response(self) -> Dict[str, Any]:
        assert self.last_response, "No response available. Make a request first."
        return self.last_response.json()

    def get_status_code(self) -> int:
        assert self.last_response, "No response available. Make a request first."
        return self.last_response.status

    def assert_status_ok(self, expected_status: int = 200) -> "APIClient":
        assert self.last_response, "No response available. Make a request first."
        actual_status = self.last_response.status
        assert actual_status == expected_status, (
            f"Expected status {expected_status}, but got {actual_status}. "
            f"Response: {self.last_response.text()}"
        )
        return self

    def assert_status_in(self, expected_statuses: list) -> "APIClient":
        assert self.last_response, "No response available. Make a request first."
        actual_status = self.last_response.status
        assert actual_status in expected_statuses, (
            f"Expected status in {expected_statuses}, but got {actual_status}"
        )
        return self

    def assert_response_contains_key(self, key: str) -> "APIClient":
        response_json = self.get_json_response()
        assert key in response_json, f"Key '{key}' not found in response. Keys: {list(response_json.keys())}"
        return self

    def assert_response_contains_keys(self, keys: list) -> "APIClient":
        response_json = self.get_json_response()
        for key in keys:
            assert key in response_json, f"Key '{key}' not found in response. Keys: {list(response_json.keys())}"
        return self

    def assert_field_value(self, key: str, expected_value: Any) -> "APIClient":
        response_json = self.get_json_response()
        actual_value = response_json.get(key)
        assert actual_value == expected_value, (
            f"Expected '{key}' to be {expected_value}, but got {actual_value}"
        )
        return self

    def assert_field_type(self, key: str, expected_type: type) -> "APIClient":
        response_json = self.get_json_response()
        assert key in response_json, f"Key '{key}' not found in response"
        actual_value = response_json.get(key)
        assert isinstance(actual_value, expected_type), (
            f"Expected '{key}' to be {expected_type}, but got {type(actual_value)}"
        )
        return self

    def get_response_text(self) -> str:
        assert self.last_response, "No response available. Make a request first."
        return self.last_response.text()

    def get_response_headers(self) -> Dict[str, str]:
        assert self.last_response, "No response available. Make a request first."
        return self.last_response.headers

    def check_rate_limit_headers(self) -> Dict[str, Union[int, str]]:
        headers = self.get_response_headers()
        rate_limit_info = {
            "limit": headers.get("X-RateLimit-Limit", "N/A"),
            "remaining": headers.get("X-RateLimit-Remaining", "N/A"),
            "reset": headers.get("X-RateLimit-Reset", "N/A"),
        }
        return rate_limit_info
