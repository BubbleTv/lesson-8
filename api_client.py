"""Базовый клиент для работы с Yougile API"""

import json
import requests


class YougileAPIClient:
    """Базовый клиент для работы с Yougile API"""

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        })

    def _make_request(self, method, endpoint, data=None, expected_status=None):
        """Внутренний метод для выполнения запросов"""
        url = f"{self.base_url}/{endpoint}"

        response = self.session.request(
            method=method,
            url=url,
            json=data
        )

        if expected_status and response.status_code != expected_status:
            raise AssertionError(
                f"Expected status {expected_status}, got {response.status_code}. "
                f"Response: {response.text}"
            )

        try:
            return response.json() if response.text else {}
        except json.JSONDecodeError:
            return {"raw_response": response.text, "status_code": response.status_code}

    def get(self, endpoint, expected_status=200):
        """GET запрос"""
        return self._make_request("GET", endpoint, expected_status=expected_status)

    def post(self, endpoint, data, expected_status=201):
        """POST запрос"""
        return self._make_request("POST", endpoint, data, expected_status)

    def put(self, endpoint, data, expected_status=200):
        """PUT запрос"""
        return self._make_request("PUT", endpoint, data, expected_status)