from playwright.sync_api import Page

from models.base_page import BasePage


class LandingPage(BasePage):
    def __init__(self, page: Page, host: str, path: str = "/web/index.php/dashboard/index"):
        super().__init__(page, host, path)
        self.landing_heading = self.page.locator(".oxd-topbar-header-title")
