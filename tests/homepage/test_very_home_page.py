from playwright.sync_api import expect

from models.pages.home.home_page import HomePage


class TestHomepage:

    def test_verify_home_page(self, home_page: HomePage) -> None:
        home_page.open()
        expect(home_page.company_branding).to_be_visible()
        expect(home_page.company_logo).to_be_visible()
        expect(home_page.username_field).to_be_visible()
        expect(home_page.password_field).to_be_visible()
        expect(home_page.login_button).to_be_visible()
        expect(home_page.forget_password_link).to_be_visible()
        expect(home_page.footer).to_be_visible()
        home_page.close()
