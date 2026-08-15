import pytest
from playwright.sync_api import Page

from models.pages.home.home_page import HomePage
from models.pages.landing.landing_page import LandingPage


@pytest.fixture()
def home_page(page: Page, hrms_host: str) -> HomePage:
    home_page = HomePage(page, hrms_host)
    return home_page

@pytest.fixture()
def landing_page(page: Page, hrms_host: str) -> LandingPage:
    landing_page = LandingPage(page, hrms_host)
    return landing_page