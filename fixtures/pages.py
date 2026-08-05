import pytest
from playwright.sync_api import Page

from models.pages.home.home_page import HomePage


@pytest.fixture()
def home_page(page: Page, hrms_host: str) -> HomePage:
    home_page = HomePage(page, hrms_host)
    return home_page