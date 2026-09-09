import os
from typing import Generator

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, BrowserType, Browser, BrowserContext, ViewportSize, Page, APIRequestContext

from helpers.config import ConfigParser
from helpers.constant import PROJECT_PATH
from helpers.api_client import APIClient

pytest_plugins = ["fixtures.pages", "fixtures.data"]


def pytest_addoption(parser) -> None:
    parser.addoption("--env", required=False, action="store", default="opensource-demo",
                     help="Environment value to tweak the environment")
    parser.addoption("--resolution", required=False, action="store", default="desktop",
                     help="Browser resolution (desktop, mobile, tablet)")
    parser.addoption("--headless", required=False, action="store", type=bool, default=True,
                     help="Run tests in headed or headless mode (True/False)")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)
        if page:
            try:
                screenshot = page.screenshot(timeout=5000)
                allure.attach(screenshot, name="failure-screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"Failed to take screenshot: {e}")


@pytest.fixture(scope="session")
def env(request: FixtureRequest) -> str:
    environment = request.config.getoption("--env")
    if environment not in ("opensource-demo", "opensource-demo-stage"):
        raise EnvironmentError(f"Invalid environment name provided: {environment}")
    return environment


@pytest.fixture(scope="session", autouse=True)
def env_vars_setup() -> None:
    if os.path.exists(os.path.join(PROJECT_PATH, ".env")):
        load_dotenv(dotenv_path=os.path.join(PROJECT_PATH, ".env"), verbose=True)


@pytest.fixture(scope="session")
def env_vars() -> dict:
    env_vars = dict(os.environ)
    return env_vars


@pytest.fixture(scope="session")
def config(env) -> dict:
    config = ConfigParser("app.yml", env)
    return config


@pytest.fixture(scope="session")
def hrms_host(config: dict) -> str:
    host = config.get("host")
    if not isinstance(host, str) or not host.strip():
        raise ValueError("host is not configured in app.yml")
    return host


@pytest.fixture(scope="session")
def viewport(request: FixtureRequest, config: dict) -> dict:
    resolution = request.config.getoption("--resolution")
    if resolution.lower().strip() in ['desktop', 'mobile', 'tablet']:
        width = config.get('resolution').get(resolution.lower().strip()).get("width")
        height = config.get('resolution').get(resolution.lower().strip()).get("height")
        viewport = {"width": width, "height": height}
    else:
        raise ValueError(f"Invalid resolution provided: {resolution}")
    return viewport


@pytest.fixture(scope="session")
def playwright() -> Generator[Playwright, None, None]:
    play_wright = sync_playwright().start()
    yield play_wright
    play_wright.stop()


@pytest.fixture(scope="session")
def browser_type(playwright: Playwright, browser_name: str) -> BrowserType:
    return getattr(playwright, browser_name)


@pytest.fixture(scope="session")
def is_chromium(browser_name: str) -> bool:
    return browser_name == "chromium"


@pytest.fixture(scope="session")
def browser(is_chromium: bool, browser_type: BrowserType, request: FixtureRequest) -> Generator[Browser, None, None]:
    headless_flag = request.config.getoption("--headless")
    browser = browser_type.launch(executable_path=None, headless=headless_flag)
    yield browser
    browser.close()


@pytest.fixture(scope="class")
def browser_context(request: FixtureRequest, browser: Browser, viewport: dict) -> Generator[BrowserContext, None, None]:
    viewport = ViewportSize(width=viewport['width'], height=viewport['height'])
    new_browser_context = browser.new_context(viewport=viewport, bypass_csp=True)
    new_browser_context.set_default_timeout(15000)
    yield new_browser_context
    new_browser_context.close()


@pytest.fixture()
def page(browser_context: BrowserContext) -> Generator[Page, None, None]:
    browser_page = browser_context.new_page()
    yield browser_page


@pytest.fixture(scope="session")
def api_base_url(config: dict) -> str:
    api_base_url = config.get("api_base_url")
    if not isinstance(api_base_url, str) or not api_base_url.strip():
        raise ValueError("api_base_url is not configured in app.yml")
    return api_base_url


@pytest.fixture(scope="session")
def api_key(env_vars: dict) -> str:
    api_key = env_vars.get("OPENWEATHER_API_KEY")
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("OPENWEATHER_API_KEY environment variable is not set. Please add it to .env")
    return api_key


@pytest.fixture()
def api_request_context(playwright: Playwright, api_base_url: str) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(base_url=api_base_url)
    yield request_context
    request_context.dispose()


@pytest.fixture()
def api_client(api_request_context: APIRequestContext, api_key: str) -> APIClient:
    return APIClient(api_request_context, api_key)
