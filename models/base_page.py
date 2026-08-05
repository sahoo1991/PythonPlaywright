from abc import ABC
from urllib.parse import urljoin

from playwright.sync_api import Page


class BasePage(ABC):

    def __init__(self, page: Page, host: str, path: str):
        self.page = page
        self._host = host
        self._path = path

    @property
    def viewport(self) -> dict:
        return self.page.viewport_size

    @property
    def is_mobile(self) -> bool:
        if self.viewport.get('width') <= 767:
            return True
        return False

    @property
    def is_tablet(self) -> bool:
        if self.viewport.get('width') >= 768:
            return True
        return False

    @property
    def is_desktop(self) -> bool:
        if self.viewport.get('width') >= 1024:
            return True
        return False

    @property
    def url(self) -> str:
        return urljoin(self._host, self._path)

    def open(self):
        self.page.goto(self.url, timeout=180000, wait_until="domcontentloaded")

    def close(self):
        self.page.close()

    def refresh(self):
        self.page.reload(timeout=90000, wait_until="domcontentloaded")
