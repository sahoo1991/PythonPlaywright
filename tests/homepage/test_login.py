import allure
from playwright.sync_api import expect

from models.pages.home.home_page import HomePage
from models.pages.landing.landing_page import LandingPage

@allure.suite("Login Test")
@allure.sub_suite("valid login")
class TestLogin:


    @allure.title("Test Login for HRMS")
    def test_verify_login_page(self, home_page: HomePage, test_username: str, test_password: str,
                               landing_page: LandingPage ) -> None:
        home_page.open()
        home_page.username_field.fill(test_username)
        home_page.password_field.fill(test_password)
        home_page.login_button.click()
        expect(landing_page.landing_heading).to_be_visible()
