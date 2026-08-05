from playwright.sync_api import Page

from models.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page, host: str, path: str = "/web/index.php/auth/login"):
        super().__init__(page, host, path)
        self.company_branding = self.page.get_by_role("img", name="company-branding")
        self.login_heading = self.page.get_by_role("heading", name="Login")
        self.username_field = self.page.get_by_role("textbox", name="Username")
        self.password_field = self.page.get_by_role("textbox", name="Password")
        self.company_logo = self.page.get_by_role("img", name="orangehrm-logo")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.forget_password_link = self.page.get_by_text("Forgot your password?")
        self.footer = self.page.locator(".orangehrm-login-footer-sm")