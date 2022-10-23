import allure
import pytest
import requests


class ApiClient:
    def __init__(self, base_address):
        self.base_address = base_address

    def get(self, path="/", params=None, headers=None):
        url = f"{self.base_address}{path}"
        with allure.step(f'GET request to: {url}'):
            return requests.get(url=url, params=params, headers=headers)

    def post(self, path="/", params=None, data=None, cookies=None, headers=None):
        url = f"{self.base_address}{path}"
        with allure.step(f'POST request to: {url}'):
            return requests.post(url=url, params=params, data=data, cookies=cookies, headers=headers)


@pytest.fixture
def test_main():
    return ApiClient(base_address='http://127.0.0.1:8000/')


@pytest.fixture
def get_db(db):
    return db
